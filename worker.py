import os
import random
import string
import qrcode
from io import BytesIO
import sys
import datetime
import logging
import queue as queuem
import re
import threading
import traceback
import uuid
from html import escape
from typing import *
from sqlalchemy import func

import requests
from blockonomics import Blockonomics
import sqlalchemy
import telegram
from telegram.error import BadRequest

import database as db
import localization
import nuconfig

log = logging.getLogger(__name__)


class StopSignal:
    """A data class that should be sent to the worker when the conversation has to be stopped abnormally."""

    def __init__(self, reason: str = ""):
        self.reason = reason


class CancelSignal:
    """An empty class that is added to the queue whenever the user presses a cancel inline button."""
    pass


class Worker(threading.Thread):
    """A worker for a single conversation. A new one is created every time the /start command is sent."""

    def __init__(self,
                 bot,
                 chat: telegram.Chat,
                 telegram_user: telegram.User,
                 cfg: nuconfig.NuConfig,
                 engine,
                 *args,
                 **kwargs):
        # Initialize the thread
        super().__init__(name=f"Worker {chat.id}", *args, **kwargs)
        # Store the bot, chat info and config inside the class
        self.bot = bot
        self.chat: telegram.Chat = chat
        self.telegram_user: telegram.User = telegram_user
        self.cfg = cfg
        self.loc = None
        # Open a new database session
        log.debug(f"Opening new database session for {self.name}")
        self.session = sqlalchemy.orm.sessionmaker(bind=engine)()
        # Get the user db data from the users and admin tables
        self.user: Optional[db.User] = None
        self.admin: Optional[db.Admin] = None
        # The sending pipe is stored in the Worker class, allowing the forwarding of messages to the chat process
        self.queue = queuem.Queue()
        # The current active invoice payload; reject all invoices with a different payload
        self.invoice_payload = None
        # The price class of this worker.
        self.Price = self.price_factory()
        db.DeliveryMethod.initialize_default_methods(self.session)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.chat.id}>"

    # noinspection PyMethodParameters
    def price_factory(worker):
        class Price:
            """The base class for the prices in greed.
            Its int value is in minimum units, while its float and str values are in decimal format."""

            def __init__(self, value: Union[int, float, str, "Price"]):
                if isinstance(value, int):
                    # Keep the value as it is
                    self.value = int(value)
                elif isinstance(value, float):
                    # Convert the value to minimum units
                    self.value = int(value * (10 ** worker.cfg["Payments"]["currency_exp"]))
                elif isinstance(value, str):
                    # Remove decimal points, then cast to int
                    self.value = int(float(value.replace(",", ".")) * (10 ** worker.cfg["Payments"]["currency_exp"]))
                elif isinstance(value, Price):
                    # Copy self
                    self.value = value.value

            def __repr__(self):
                return f"<{self.__class__.__qualname__} of value {self.value}>"

            def __str__(self):
                return worker.loc.get(
                    "currency_format_string",
                    symbol=worker.cfg["Payments"]["currency_symbol"],
                    value="{0:.2f}".format(self.value / (10 ** worker.cfg["Payments"]["currency_exp"]))
                )

            def __int__(self):
                return self.value

            def __float__(self):
                return self.value / (10 ** worker.cfg["Payments"]["currency_exp"])

            def __ge__(self, other):
                return self.value >= Price(other).value

            def __le__(self, other):
                return self.value <= Price(other).value

            def __eq__(self, other):
                return self.value == Price(other).value

            def __gt__(self, other):
                return self.value > Price(other).value

            def __lt__(self, other):
                return self.value < Price(other).value

            def __add__(self, other):
                return Price(self.value + Price(other).value)

            def __sub__(self, other):
                return Price(self.value - Price(other).value)

            def __mul__(self, other):
                return Price(int(self.value * other))

            def __floordiv__(self, other):
                return Price(int(self.value // other))

            def __radd__(self, other):
                return self.__add__(other)

            def __rsub__(self, other):
                return Price(Price(other).value - self.value)

            def __rmul__(self, other):
                return self.__mul__(other)

            def __iadd__(self, other):
                self.value += Price(other).value
                return self

            def __isub__(self, other):
                self.value -= Price(other).value
                return self

            def __imul__(self, other):
                self.value *= other
                self.value = int(self.value)
                return self

            def __ifloordiv__(self, other):
                self.value //= other
                return self

        return Price

    def run(self):
        """The conversation code."""
        log.debug("Starting conversation")
        # Get the user db data from the users and admin tables
        self.user = self.session.query(db.User).filter(db.User.user_id == self.chat.id).one_or_none()
        self.admin = self.session.query(db.Admin).filter(db.Admin.user_id == self.chat.id).one_or_none()

        # Flag to check if this is a new user
        is_new_user = False

        # If the user isn't registered, create a new record and add it to the db
        if self.user is None:
            is_new_user = True
            # Check if there are other registered users: if there aren't any, the first user will be owner of the bot
            will_be_owner = (self.session.query(db.Admin).first() is None)
            # Create the new record
            self.user = db.User(w=self)
            # Add the new record to the db
            self.session.add(self.user)
            # If the will be owner flag is set
            if will_be_owner:
                # Become owner
                self.admin = db.Admin(user=self.user,
                                      edit_products=True,
                                      edit_categories=True,
                                      receive_orders=True,
                                      create_transactions=True,
                                      display_on_help=True,
                                      is_owner=True,
                                      live_mode=False)
                # Add the admin to the transaction
                self.session.add(self.admin)
            # Commit the transaction
            self.session.commit()
            log.info(f"Created new user: {self.user}")
            if will_be_owner:
                log.warning(f"User was auto-promoted to Admin as no other admins existed: {self.user}")

        # Create the localization object
        self.__create_localization()

        # Capture exceptions that occur during the conversation
        try:
            # Welcome the user to the bot if it's a new user or if display_welcome_message is set to "yes"
            if is_new_user or self.cfg["Appearance"]["display_welcome_message"] == "yes":
                self.bot.send_message(self.chat.id, self.loc.get("conversation_after_start"))

            # If the user is not an admin, send him to the user menu
            if self.admin is None:
                self.__user_menu()
            # If the user is an admin, send him to the admin menu
            else:
                # Clear the live orders flag
                self.admin.live_mode = False
                # Commit the change
                self.session.commit()
                # Open the admin menu
                self.__admin_menu()
        except Exception as e:
            # Try to notify the user of the exception
            try:
                self.bot.send_message(self.chat.id, self.loc.get("fatal_conversation_exception"))
            except Exception as ne:
                log.error(f"Failed to notify the user of a conversation exception: {ne}")
            log.error(f"Exception in {self}: {e}")
            traceback.print_exception(*sys.exc_info())

    def is_ready(self):
        # Change this if more parameters are added!
        return self.loc is not None

    def stop(self, reason: str = ""):
        """Gracefully stop the worker process"""
        # Send a stop message to the thread
        self.queue.put(StopSignal(reason))
        # Wait for the thread to stop
        self.join()

    def update_user(self) -> db.User:
        """Update the user data."""
        log.debug("Fetching updated user data from the database")
        self.user = self.session.query(db.User).filter(db.User.user_id == self.chat.id).one_or_none()
        return self.user

    # noinspection PyUnboundLocalVariable
    def __receive_next_update(self) -> telegram.Update:
        """Get the next update from the queue.
        If no update is found, block the process until one is received.
        If a stop signal is sent, try to gracefully stop the thread."""
        # Pop data from the queue
        try:
            data = self.queue.get(timeout=self.cfg["Telegram"]["conversation_timeout"])
        except queuem.Empty:
            # If the conversation times out, gracefully stop the thread
            self.__graceful_stop(StopSignal("timeout"))
        # Check if the data is a stop signal instance
        if isinstance(data, StopSignal):
            # Gracefully stop the process
            self.__graceful_stop(data)
        # Return the received update
        return data

    def check_description_length(self, text, max_length):
        return len(text) <= max_length

    def __wait_for_regex_or_back(self, regex):
        keyboard = [[telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")]]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        self.bot.send_message(self.chat.id, self.loc.get("or_press_back"), reply_markup=reply_markup)

        while True:
            update = self.__receive_next_update()
            if isinstance(update, telegram.Update):
                if update.callback_query and update.callback_query.data == "back":
                    return "back"
                elif update.message and update.message.text:
                    match = re.match(regex, update.message.text)
                    if match:
                        return match.group(0)
            elif isinstance(update, CancelSignal):
                return "back"

    def __wait_for_specific_message(self,
                                    items: List[str],
                                    cancellable: bool = False) -> Union[str, CancelSignal]:
        """Continue getting updates until until one of the strings contained in the list is received as a message."""
        log.debug("Waiting for a specific message...")
        while True:
            # Get the next update
            update = self.__receive_next_update()
            # If a CancelSignal is received...
            if isinstance(update, CancelSignal):
                # And the wait is cancellable...
                if cancellable:
                    # Return the CancelSignal
                    return update
                else:
                    # Ignore the signal
                    continue
            if isinstance(update, tuple):
                log.debug(f"Received tuple update: {update}")
                # Якщо це кортеж з двох елементів і другий елемент - рядок
                if len(update) == 2 and isinstance(update[1], str):
                    # Перевіряємо, чи це промокод
                    promo_code = update[1]
                    if promo_code in items:
                        # Якщо це промокод, який ми очікуємо, повертаємо його
                        return promo_code
                    else:
                        # Якщо це не очікуваний промокод, обробляємо його
                        self.__enter_promocode(promo_code)
                continue
            # Ensure the update contains a message
            if not hasattr(update, 'message') or update.message is None:
                continue
            # Ensure the message contains text
            if update.message.text is None:
                continue
            # Check if the message is contained in the list
            if update.message.text not in items:
                continue
            # Return the message text
            return update.message.text

    def __wait_for_regex_or_callback_2(self, regex, cancellable=False):
        """Wait for a regex match in a message or a callback query."""
        while True:
            update = self.__receive_next_update()
            if isinstance(update, CancelSignal):
                if cancellable:
                    return update
                else:
                    continue
            if isinstance(update, telegram.Update):
                if update.callback_query:
                    return update.callback_query
                elif update.message and update.message.text:
                    match = re.search(regex, update.message.text, re.DOTALL)
                    if match:
                        return update.message.text
            log.debug(f"Received update: {update}")
        return None

    def __wait_for_regex_or_callback(self, regex, cancellable=False):
        """Wait for a regex match in a message or a callback query."""
        while True:
            update = self.__receive_next_update()
            if isinstance(update, CancelSignal):
                if cancellable:
                    return update
                else:
                    continue
            if isinstance(update, telegram.Update):
                if update.callback_query:
                    return update.callback_query
                elif update.message and update.message.text:
                    match = re.search(regex, update.message.text, re.DOTALL)
                    if match:
                        return match.group(1)

    def __wait_for_photo_or_callback(self, cancellable=False):
        """Wait for a photo or a callback query."""
        while True:
            update = self.__receive_next_update()
            if isinstance(update, CancelSignal):
                if cancellable:
                    return update
                else:
                    continue
            if isinstance(update, telegram.Update):
                if update.callback_query:
                    return update.callback_query
                elif update.message and update.message.photo:
                    return update.message.photo

    def __wait_for_regex_update(self, regex: str, cancellable: bool = False) -> Union[str, CancelSignal]:
        """Continue getting updates until the regex finds a match in a message, then return the first object message."""
        log.debug("Waiting for a regex...")
        while True:
            # Get the next update
            update = self.__receive_next_update()
            # If a CancelSignal is received...
            if isinstance(update, CancelSignal):
                # And the wait is cancellable...
                if cancellable:
                    # Return the CancelSignal
                    return update
                else:
                    # Ignore the signal
                    continue
            # Ensure the update contains a message
            if update.message is None:
                continue
            # Ensure the message contains text
            if update.message.text is None:
                continue
            # Try to match the regex with the received message
            match = re.search(regex, update.message.text, re.DOTALL)
            # Ensure there is a match
            if match is None:
                continue
            # Return the first capture group
            return update.message.text

    def __wait_for_regex(self, regex: str, cancellable: bool = False) -> Union[str, CancelSignal]:
        """Continue getting updates until the regex finds a match in a message, then return the first capture group."""
        log.debug("Waiting for a regex...")
        while True:
            # Get the next update
            update = self.__receive_next_update()
            # If a CancelSignal is received...
            if isinstance(update, CancelSignal):
                # And the wait is cancellable...
                if cancellable:
                    # Return the CancelSignal
                    return update
                else:
                    # Ignore the signal
                    continue
            # Ensure the update contains a message
            if update.message is None:
                continue
            # Ensure the message contains text
            if update.message.text is None:
                continue
            # Try to match the regex with the received message
            match = re.search(regex, update.message.text, re.DOTALL)
            # Ensure there is a match
            if match is None:
                continue
            # Return the first capture group
            return match.group(1)

    def __wait_for_precheckoutquery(self,
                                    cancellable: bool = False) -> Union[telegram.PreCheckoutQuery, CancelSignal]:
        """Continue getting updates until a precheckoutquery is received.
        The payload is checked by the core before forwarding the message."""
        log.debug("Waiting for a PreCheckoutQuery...")
        while True:
            # Get the next update
            update = self.__receive_next_update()
            # If a CancelSignal is received...
            if isinstance(update, CancelSignal):
                # And the wait is cancellable...
                if cancellable:
                    # Return the CancelSignal
                    return update
                else:
                    # Ignore the signal
                    continue
            # Ensure the update contains a precheckoutquery
            if update.pre_checkout_query is None:
                continue
            # Return the precheckoutquery
            return update.pre_checkout_query

    def __wait_for_successfulpayment(self,
                                     cancellable: bool = False) -> Union[telegram.SuccessfulPayment, CancelSignal]:
        """Continue getting updates until a successfulpayment is received."""
        log.debug("Waiting for a SuccessfulPayment...")
        while True:
            # Get the next update
            update = self.__receive_next_update()
            # If a CancelSignal is received...
            if isinstance(update, CancelSignal):
                # And the wait is cancellable...
                if cancellable:
                    # Return the CancelSignal
                    return update
                else:
                    # Ignore the signal
                    continue
            # Ensure the update contains a message
            if update.message is None:
                continue
            # Ensure the message is a successfulpayment
            if update.message.successful_payment is None:
                continue
            # Return the successfulpayment
            return update.message.successful_payment

    def __send_btc_payment_info(self, address, amount):
        # Send a message containing the btc pay info
        self.bot.send_message_markdown(
            self.chat.id,
            "To pay, send this amount:\n`{}`\nto this bitcoin address:\n`{}`".format(str(amount), address)
        )

    def __wait_for_photo(self, cancellable: bool = False) -> Union[List[telegram.PhotoSize], CancelSignal]:
        """Continue getting updates until a photo is received, then return it."""
        log.debug("Waiting for a photo...")
        while True:
            # Get the next update
            update = self.__receive_next_update()
            # If a CancelSignal is received...
            if isinstance(update, CancelSignal):
                # And the wait is cancellable...
                if cancellable:
                    # Return the CancelSignal
                    return update
                else:
                    # Ignore the signal
                    continue
            # Ensure the update contains a message
            if update.message is None:
                continue
            # Ensure the message contains a photo
            if update.message.photo is None:
                continue
            # Return the photo array
            return update.message.photo

    def __wait_for_inlinekeyboard_callback(self, cancellable: bool = False) \
            -> Union[telegram.CallbackQuery, CancelSignal]:
        """Continue getting updates until an inline keyboard callback is received, then return it."""
        log.debug("Waiting for a CallbackQuery...")
        while True:
            # Get the next update
            update = self.__receive_next_update()
            # If a CancelSignal is received...
            if isinstance(update, CancelSignal):
                # And the wait is cancellable...
                if cancellable:
                    # Return the CancelSignal
                    return update
                else:
                    # Ignore the signal
                    continue
            # Ensure the update is a CallbackQuery
            if update.callback_query is None:
                continue
            # Answer the callbackquery
            self.bot.answer_callback_query(update.callback_query.id)
            # Return the callbackquery
            return update.callback_query

    def __user_select(self) -> Union[db.User, CancelSignal]:
        """Select an user from the ones in the database."""
        log.debug("Waiting for a user selection...")
        # Find all the users in the database
        users = self.session.query(db.User).order_by(db.User.user_id).all()
        # Create a list containing all the keyboard button strings
        keyboard_buttons = [[self.loc.get("menu_cancel")]]
        # Add to the list all the users
        for user in users:
            keyboard_buttons.append([user.identifiable_str()])
        # Create the keyboard
        keyboard = telegram.ReplyKeyboardMarkup(keyboard_buttons, one_time_keyboard=True)
        # Keep asking until a result is returned
        while True:
            # Send the keyboard
            self.bot.send_message(self.chat.id, self.loc.get("conversation_admin_select_user"), reply_markup=keyboard)
            # Wait for a reply
            reply = self.__wait_for_regex("user_([0-9]+)", cancellable=True)
            # Propagate CancelSignals
            if isinstance(reply, CancelSignal):
                return reply
            # Find the user in the database
            user = self.session.query(db.User).filter_by(user_id=int(reply)).one_or_none()
            # Ensure the user exists
            if not user:
                self.bot.send_message(self.chat.id, self.loc.get("error_user_does_not_exist"))
                continue
            return user

    def __user_menu(self):
        log.debug("Displaying __user_menu")
        while True:
            keyboard = [
                [telegram.KeyboardButton(self.loc.get("menu_profile"))],
                [telegram.KeyboardButton(self.loc.get("menu_order")),
                 telegram.KeyboardButton(self.loc.get("menu_cart"))],
                [telegram.KeyboardButton(self.loc.get("menu_help")),
                 telegram.KeyboardButton(self.loc.get("menu_language"))]
            ]

            self.bot.send_message(self.chat.id,
                                  self.loc.get("conversation_open_user_menu",
                                               credit=self.Price(self.user.credit)),
                                  reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

            log.debug("Waiting for user selection in main menu")
            selection = self.__wait_for_specific_message([
                self.loc.get("menu_profile"),
                self.loc.get("menu_order"),
                self.loc.get("menu_cart"),
                self.loc.get("menu_language"),
                self.loc.get("menu_help"),
            ])
            log.debug(f"User selected: {selection}")

            self.update_user()

            if isinstance(selection, tuple):
                # Якщо отримано кортеж, це може бути промокод з QR-коду
                promo_code = selection[1]
                self.__enter_promocode(promo_code)
                continue

            if selection == self.loc.get("menu_profile"):
                log.debug("Opening profile menu")
                self.__profile_menu()
            elif selection == self.loc.get("menu_order"):
                log.debug("Opening order menu")
                self.__order_menu()
            elif selection == self.loc.get("menu_cart"):
                log.debug("Opening cart menu")
                self.__cart_menu()
            elif selection == self.loc.get("menu_language"):
                log.debug("Opening language menu")
                self.__language_menu()
            elif selection == self.loc.get("menu_help"):
                log.debug("Opening help menu")
                self.__help_menu()

            log.debug("Returned to main menu")

    def __cart_menu(self):
        log.debug("Entering __cart_menu")
        try:
            # Спробуємо видалити попереднє повідомлення кошика, якщо воно існує
            if hasattr(self, 'cart_message_id'):
                try:
                    self.bot.delete_message(chat_id=self.chat.id, message_id=self.cart_message_id)
                    log.debug("Previous cart message deleted")
                except telegram.error.BadRequest as e:
                    if "Message to delete not found" in str(e):
                        log.debug("Previous cart message not found, skipping deletion")
                    else:
                        log.warning(f"Failed to delete previous cart message: {e}")
                finally:
                    # Видаляємо атрибут cart_message_id незалежно від результату видалення
                    delattr(self, 'cart_message_id')

            if not hasattr(self, 'cart') or not self.cart:
                self.bot.send_message(self.chat.id, self.loc.get("cart_empty"))
                return

            while True:
                message = self.loc.get("cart_contents") + "\n\n"
                total = 0
                for product_id, item in self.cart.items():
                    product = item['product']
                    quantity = item['quantity']
                    subtotal = product.price * quantity
                    total += subtotal
                    message += f"{product.name} x{quantity}: {self.Price(subtotal)}\n"

                message += f"\n{self.loc.get('cart_total')}: {self.Price(total)}"

                keyboard = [
                    [telegram.InlineKeyboardButton(self.loc.get("menu_edit_cart"), callback_data="cart_edit")],
                    [telegram.InlineKeyboardButton(self.loc.get("menu_checkout"), callback_data="cart_checkout")],
                    [telegram.InlineKeyboardButton(self.loc.get("menu_clear_cart"), callback_data="cart_clear")],
                    [telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="cart_back")]
                ]

                reply_markup = telegram.InlineKeyboardMarkup(keyboard)

                new_message = self.bot.send_message(self.chat.id, message, reply_markup=reply_markup)
                self.cart_message_id = new_message.message_id
                log.debug("New cart message sent")

                callback = self.__wait_for_inlinekeyboard_callback()
                action = callback.data.split('_')[1]

                if action == "edit":
                    edit_result = self.__edit_cart()
                    if edit_result == "back_to_cart":
                        continue
                elif action == "checkout":
                    return self.__checkout()
                elif action == "clear":
                    self.cart = {}
                    self.bot.answer_callback_query(callback.id, text=self.loc.get("cart_cleared"))
                    return self.__cart_menu()
                elif action == "back":
                    return

                if not self.cart:
                    self.bot.edit_message_text(chat_id=self.chat.id, message_id=self.cart_message_id,
                                               text=self.loc.get("cart_empty"))
                    return

        except Exception as e:
            log.error(f"Error in __cart_menu: {e}")
            self.bot.send_message(self.chat.id, self.loc.get("error_cart_menu"))

    def __edit_cart(self):
        log.debug("Editing cart")
        edit_message_id = None

        while True:
            message = self.loc.get("cart_edit_header") + "\n\n"
            total = 0
            keyboard = []

            for product_id, item in self.cart.items():
                product = item['product']
                quantity = item['quantity']
                subtotal = product.price * quantity
                total += subtotal
                message += f"{product.name} x{quantity}: {self.Price(subtotal)}\n"

                keyboard.append([
                    telegram.InlineKeyboardButton(f"➖ {product.name}", callback_data=f"cart_decrease_{product_id}"),
                    telegram.InlineKeyboardButton(f"➕ {product.name}", callback_data=f"cart_increase_{product_id}"),
                    telegram.InlineKeyboardButton(f"🗑 {product.name}", callback_data=f"cart_remove_{product_id}")
                ])

            message += f"\n{self.loc.get('cart_total')}: {self.Price(total)}"

            keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="cart_back")])

            reply_markup = telegram.InlineKeyboardMarkup(keyboard)

            try:
                if edit_message_id:
                    self.bot.edit_message_text(chat_id=self.chat.id, message_id=edit_message_id,
                                               text=message, reply_markup=reply_markup)
                else:
                    new_message = self.bot.send_message(self.chat.id, message, reply_markup=reply_markup)
                    edit_message_id = new_message.message_id
            except telegram.error.BadRequest as e:
                log.warning(f"Failed to edit cart message: {e}")
                new_message = self.bot.send_message(self.chat.id, message, reply_markup=reply_markup)
                edit_message_id = new_message.message_id

            callback = self.__wait_for_inlinekeyboard_callback()
            action, *args = callback.data.split('_')

            if action == "cart":
                if args[0] == "decrease":
                    product_id = int(args[1])
                    if self.cart[product_id]['quantity'] > 1:
                        self.cart[product_id]['quantity'] -= 1
                    else:
                        del self.cart[product_id]
                elif args[0] == "increase":
                    product_id = int(args[1])
                    self.cart[product_id]['quantity'] += 1
                elif args[0] == "remove":
                    product_id = int(args[1])
                    del self.cart[product_id]
                elif args[0] == "back":
                    if edit_message_id:
                        self.bot.delete_message(chat_id=self.chat.id, message_id=edit_message_id)
                    return "back_to_cart"

            if not self.cart:
                self.bot.send_message(self.chat.id, self.loc.get("cart_empty"))
                return "back_to_cart"

    def __get_time_with_us_string(self, days):
        if days % 10 == 1 and days % 100 != 11:
            return f"{days} {self.loc.get('day')}"
        elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
            return f"{days} {self.loc.get('days_2_4')}"
        else:
            return f"{days} {self.loc.get('days_many')}"

    def __get_user_info(self):
        user_data = self.session.query(db.User).filter_by(user_id=self.chat.id).one()

        current_time = datetime.datetime.now()
        time_difference = current_time - user_data.connect_date
        days_with_us = time_difference.days + 1

        time_with_us_string = self.__get_time_with_us_string(days_with_us)

        return {
            'id': user_data.user_id,
            'name': user_data.first_name,
            'balance': str(user_data.credit / 100),
            'time_with_us': time_with_us_string
        }

    def __profile_menu(self):
        """Display user profile menu with multiple tabs."""
        log.debug("Displaying __profile_menu")
        # Create a keyboard with profile menu options

        user_info = self.__get_user_info()
        message = self.loc.get("profile_info").format(
            id=user_info['id'],
            name=user_info['name'],
            balance=user_info['balance'] + f' {self.cfg["Payments"]["currency"]}',
            time_with_us=user_info['time_with_us']
        )

        keyboard = [
            [telegram.KeyboardButton(self.loc.get("menu_add_credit")),
             telegram.KeyboardButton(self.loc.get("menu_credit_history"))],
            [telegram.KeyboardButton(self.loc.get("menu_promocode"))],
            [telegram.KeyboardButton(self.loc.get("menu_order_status"))],
            [telegram.KeyboardButton(self.loc.get("menu_cancel"))]
        ]

        # Send the profile menu keyboard to the user
        self.bot.send_message(self.chat.id, message,
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        # Wait for a reply from the user
        selection = self.__wait_for_specific_message([
            self.loc.get("menu_add_credit"),
            self.loc.get("menu_credit_history"),
            self.loc.get("menu_promocode"),
            self.loc.get("menu_order_status")
        ], cancellable=True)

        if isinstance(selection, CancelSignal):
            # Повертаємо користувача до головного меню
            return

        # Handle the user's selection
        if selection == self.loc.get("menu_add_credit"):
            self.__add_credit_menu()
        elif selection == self.loc.get("menu_credit_history"):
            self.__credit_history()
        elif selection == self.loc.get("menu_promocode"):
            self.__enter_promocode()
        elif selection == self.loc.get("menu_order_status"):
            self.__order_status()

    def __credit_history(self):
        """Display user's credit history."""
        log.debug("Displaying __credit_history")
        # Fetch credit history from the database
        transactions = self.session.query(db.Transaction).filter_by(user_id=self.user.user_id).all()
        # Create a summary of transactions
        history = "\n".join([f"{str(t.date)[:19]} - <b>{t.value / 100}</b>" + f' {self.cfg["Payments"]["currency"]}'
                             for t in transactions])
        if history:
            # Send the history to the user
            self.bot.send_message(self.chat.id, self.loc.get("credit_history") + f"\n{history}")
            # Return to the profile menu
            self.__profile_menu()
        else:
            self.bot.send_message(self.chat.id, self.loc.get("credit_history_null"))
            # Return to the profile menu
            self.__profile_menu()

    def __enter_promocode(self, code=None):
        """Apply a promocode."""
        log.debug("Displaying __apply_promocode")

        if code is None:
            self.bot.send_message(self.chat.id, self.loc.get("ask_promocode"))
            code = self.__wait_for_regex_update(r"\S+")

        # Перевірка на наявність попередніх поповнень
        has_previous_deposits = self.session.query(db.Transaction).filter(
            db.Transaction.user_id == self.user.user_id,
            db.Transaction.value > 0
        ).first() is not None

        if not has_previous_deposits:
            self.bot.send_message(self.chat.id, self.loc.get("error_no_deposits_for_promocode"))
            return

        promocode = self.session.query(db.Promocode).filter_by(code=code).first()
        if promocode is None:
            self.bot.send_message(self.chat.id, self.loc.get("invalid_promocode"))
            return

        existing_usage = self.session.query(db.PromocodeUsage).filter_by(
            user_id=self.user.user_id,
            promocode_id=promocode.id
        ).first()

        if existing_usage:
            self.bot.send_message(self.chat.id, self.loc.get("promocode_already_used"))
            return

        if promocode.uses_left <= 0:
            self.bot.send_message(self.chat.id, self.loc.get("promocode_expired"))
            return

        if promocode.fixed_amount:
            amount = promocode.fixed_amount
        else:
            amount = random.randint(promocode.min_amount, promocode.max_amount)

        self.user.credit += amount * 100

        promocode.uses_left -= 1

        new_usage = db.PromocodeUsage(
            user_id=self.user.user_id,
            promocode_id=promocode.id
        )
        self.session.add(new_usage)

        # Створюємо нову транзакцію
        transaction = db.Transaction(
            user=self.user,
            value=int(amount * 100),
            provider=f"Promo {code}",
            promocode_usage=new_usage
        )
        self.session.add(transaction)

        try:
            self.session.commit()
            self.bot.send_message(self.chat.id, self.loc.get("promocode_applied", amount=amount))
        except Exception as e:
            self.session.rollback()
            log.error(f"Error applying promocode: {str(e)}")
            self.bot.send_message(self.chat.id, self.loc.get("error_applying_promocode"))

        self.__profile_menu()

    def __list_promocodes(self):
        """List all promocodes with statistics."""
        log.debug("Displaying __list_promocodes")

        try:
            promocodes = self.session.query(db.Promocode).all()
            if promocodes:
                for promo in promocodes:
                    try:
                        creator = self.session.query(db.Admin).filter_by(user_id=promo.created_by).first()
                        used_count = promo.total_uses - promo.uses_left

                        total_amount = self.session.query(db.Transaction) \
                            .join(db.PromocodeUsage) \
                            .filter(db.PromocodeUsage.promocode_id == promo.id) \
                            .with_entities(db.Transaction.value) \
                            .all()
                        total_amount = sum([t.value for t in total_amount]) if total_amount else 0

                        amount_str = f"{promo.fixed_amount}" if promo.fixed_amount is not None else f"{promo.min_amount} - {promo.max_amount}"

                        message = self.loc.get("promocode_info",
                                               code=promo.code,
                                               type="QR" if promo.is_qr else self.loc.get("text_promocode"),
                                               amount=amount_str,
                                               uses_left=promo.uses_left,
                                               total_uses=promo.total_uses,
                                               creator=creator.user.first_name if creator and creator.user else self.loc.get(
                                                   "unknown"),
                                               used_count=used_count,
                                               total_amount=self.Price(total_amount))
                        self.bot.send_message(self.chat.id, message)
                    except Exception as e:
                        log.error(f"Error processing promocode {promo.code}: {str(e)}")
                        self.bot.send_message(self.chat.id, f"Error processing promocode {promo.code}")
            else:
                self.bot.send_message(self.chat.id, self.loc.get("no_active_promocodes"))
        except Exception as e:
            log.error(f"Error in __list_promocodes: {str(e)}")
            self.bot.send_message(self.chat.id, self.loc.get("error_listing_promocodes"))

    def __send_message_with_photo(self, chat_id, text, photo, reply_markup=None):
        """Send a message with photo, splitting it if the text is too long."""
        try:
            if len(text) > 1024 and photo:
                self.bot.send_photo(chat_id, photo)
                return self.bot.send_message(chat_id, text, reply_markup=reply_markup)
            elif photo:
                return self.bot.send_photo(chat_id, photo, caption=text, reply_markup=reply_markup)
            else:
                return self.bot.send_message(chat_id, text, reply_markup=reply_markup)
        except Exception as e:
            log.error(f"Error in __send_message_with_photo: {e}")
            return None

    def __edit_message_with_photo(self, chat_id, message_id, text, photo, reply_markup=None):
        """Edit a message with photo, splitting it if the text is too long."""
        try:
            if len(text) > 1024 and photo:
                self.bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=telegram.InputMediaPhoto(photo)
                )
                return self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id + 1,
                    text=text,
                    reply_markup=reply_markup
                )
            elif photo:
                return self.bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=telegram.InputMediaPhoto(photo, caption=text),
                    reply_markup=reply_markup
                )
            else:
                return self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=text,
                    reply_markup=reply_markup
                )
        except Exception as e:
            log.error(f"Error in __edit_message_with_photo: {e}")
            return None

    def __create_promocode(self):
        """Create a new promocode."""
        log.debug("Displaying __create_promocode")

        # Ask for promocode type
        keyboard = [[self.loc.get('menu_promo_text')], [self.loc.get('menu_promo_qr')]]
        self.bot.send_message(self.chat.id, self.loc.get("choose_promocode_type"), reply_markup=
        telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

        promocode_type = self.__wait_for_specific_message([self.loc.get('menu_promo_text'),
                                                           self.loc.get('menu_promo_qr')])

        # Generate unique code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))

        # Ask for amount type
        keyboard = [[self.loc.get('menu_promo_fixed')], [self.loc.get('menu_promo_range')]]
        self.bot.send_message(self.chat.id, self.loc.get("choose_amount_type"), reply_markup=
        telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
        amount_type = self.__wait_for_specific_message([self.loc.get('menu_promo_fixed'),
                                                        self.loc.get('menu_promo_range')])

        if amount_type == self.loc.get('menu_promo_fixed'):
            self.bot.send_message(self.chat.id, self.loc.get("ask_fixed_amount"))
            fixed_amount = int(self.__wait_for_regex_update(r"\d+"))
            min_amount = max_amount = fixed_amount
        else:
            self.bot.send_message(self.chat.id, self.loc.get("ask_min_amount"))
            min_amount = int(self.__wait_for_regex_update(r"\d+"))
            self.bot.send_message(self.chat.id, self.loc.get("ask_max_amount"))
            max_amount = int(self.__wait_for_regex_update(r"\d+"))
            fixed_amount = None

        # Ask for number of uses
        self.bot.send_message(self.chat.id, self.loc.get("ask_uses_number"))
        uses = int(self.__wait_for_regex_update(r"\d+"))

        # Create promocode
        promocode = db.Promocode(
            code=code,
            is_qr=(promocode_type == self.loc.get('menu_promo_qr')),
            min_amount=min_amount,
            max_amount=max_amount,
            fixed_amount=fixed_amount,
            uses_left=uses,
            total_uses=uses,
            created_by=self.admin.user_id
        )
        self.session.add(promocode)
        self.session.commit()

        # Send confirmation
        if promocode_type == self.loc.get('menu_promo_qr'):
            # Create the bot link with the promocode as a parameter
            bot_username = self.bot.get_me().username
            qr_data = f"https://t.me/{bot_username}?start={code}"

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            bio = BytesIO()
            img.save(bio, 'PNG')
            bio.seek(0)
            self.bot.send_photo(self.chat.id, photo=bio,
                                caption=self.loc.get("promocode_created_qr", code=code, link=qr_data))
        else:
            self.bot.send_message(self.chat.id, self.loc.get("promocode_created_text", code=code))

    def __delete_promocode(self):
        """Delete an existing promocode."""
        log.debug("Displaying __delete_promocode")

        promocodes = self.session.query(db.Promocode).all()
        if not promocodes:
            self.bot.send_message(self.chat.id, self.loc.get("no_promocodes_to_delete"))
            return

        keyboard = [[promo.code] for promo in promocodes]
        keyboard.append([self.loc.get("menu_cancel")])
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        self.bot.send_message(self.chat.id, self.loc.get("choose_promocode_to_delete"), reply_markup=reply_markup)

        selection = self.__wait_for_specific_message(
            [promo.code for promo in promocodes] + [self.loc.get("menu_cancel")])

        if selection == self.loc.get("menu_cancel"):
            return

        promocode = self.session.query(db.Promocode).filter_by(code=selection).first()
        if promocode:
            self.session.delete(promocode)
            self.session.commit()
            self.bot.send_message(self.chat.id, self.loc.get("promocode_deleted", code=selection))
        else:
            self.bot.send_message(self.chat.id, self.loc.get("promocode_not_found"))

    # def __order_menu(self):
    #     # Create a dict to be used as 'cart'
    #     # The key is the message id of the product list
    #     cart: Dict[List[db.Product, int]] = {}
    #     category_mode = self.cfg["Mode"]["category_mode"]
    #     final_step = False
    #
    #     while True:
    #         if category_mode:
    #             # Get the categories list from the db
    #             categories = self.session.query(db.Category).filter_by(deleted=False).all()
    #             category_names = [category.name for category in categories]
    #
    #             # Remove categories with no products assigned
    #             for category in categories:
    #                 p = self.session.query(db.Product).filter_by(deleted=False).filter_by(category_id=category.id).all()
    #                 if not p:
    #                     category_names.remove(category.name)
    #
    #             # Insert at the start of the list the Cancel and the All products options
    #             category_names.insert(0, self.loc.get("menu_cancel"))
    #             category_names.insert(1, self.loc.get("menu_all_products"))
    #
    #             # Insert at the start of the list the Uncategozied option (if they exist)
    #             # Uncategorized products could happen if admin deletes a category with existing products in it
    #             products_with_no_category = self.session.query(db.Product).filter_by(deleted=False).filter_by(
    #                 category_id=None).all()
    #             if products_with_no_category:
    #                 category_names.insert(2, self.loc.get("menu_uncategorized"))
    #
    #             # Create a keyboard using the category names
    #             keyboard = [[telegram.KeyboardButton(category_name)] for category_name in category_names]
    #             # Send the previously created keyboard to the user (ensuring it can be clicked only 1 time)
    #             self.bot.send_message(self.chat.id, self.loc.get("conversation_select_category"),
    #                                   reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    #             # Wait for a reply from the user
    #             selection = self.__wait_for_specific_message(category_names, cancellable=True)
    #
    #             # If the user has selected the Cancel option...
    #             if isinstance(selection, CancelSignal):
    #                 # Exit the menu
    #                 return
    #             # If the user has selected the All products option...
    #             elif selection == self.loc.get("menu_all_products"):
    #                 # Get all the products list from the db
    #                 products = self.session.query(db.Product).filter_by(deleted=False).all()
    #             # If the user has selected the Uncategorized option...
    #             elif selection == self.loc.get("menu_uncategorized"):
    #                 # Get only products where category_id is not set
    #                 products = products_with_no_category
    #             # If the user has selected a category
    #             else:
    #                 # Find the selected category
    #                 category = self.session.query(db.Category).filter_by(name=selection, deleted=False).one()
    #                 # Get only products where category_id is the selected category
    #                 products = self.session.query(db.Product).filter_by(deleted=False).filter_by(
    #                     category_id=category.id).all()
    #
    #                 # Hide the "Select category" keyboard from the user.
    #                 self.bot.send_message(self.chat.id, selection,
    #                                       reply_markup=telegram.ReplyKeyboardRemove())
    #         else:
    #             # Get the products list from the db
    #             products = self.session.query(db.Product).filter_by(deleted=False).all()
    #
    #         """User menu to order products from the shop."""
    #         log.debug("Displaying __order_menu")
    #         # Initialize the products list
    #         for product in products:
    #             # If the product is not for sale, don't display it
    #             if product.price is None:
    #                 continue
    #             # Send the message without the keyboard to get the message id
    #             message = product.send_as_message(w=self, chat_id=self.chat.id)
    #             # Add the product to the cart
    #             cart[message['message_id']] = [product, 0]
    #             # Update existing products in the cart
    #             # This allows the user to go back to category selection preserving cart values on the new message id and deleting the old one (Avoid duplication)
    #             old_message_ids = [k for k, v in cart.items() if v[0].id == product.id]
    #             if (len(old_message_ids) > 1):
    #                 cart[message['message_id']][1] = cart[old_message_ids[0]][1]
    #                 del cart[old_message_ids[0]]
    #
    #             # Create the inline keyboard to add the product to the cart
    #             inline_keyboard_list = [[telegram.InlineKeyboardButton(self.loc.get("menu_add_to_cart"),
    #                                                                    callback_data="cart_add")]]
    #             if cart[message['message_id']][1] > 0:
    #                 inline_keyboard_list[0].append(telegram.InlineKeyboardButton(self.loc.get("menu_remove_from_cart"),
    #                                                                              callback_data="cart_remove"))
    #             inline_keyboard = telegram.InlineKeyboardMarkup(inline_keyboard_list)
    #
    #             # Edit the sent message and add the inline keyboard
    #             if product.image is None:
    #                 self.bot.edit_message_text(chat_id=self.chat.id,
    #                                            message_id=message['message_id'],
    #                                            text=product.text(w=self,
    #                                                              cart_qty=cart[message['message_id']][1]),
    #                                            reply_markup=inline_keyboard)
    #             else:
    #                 self.bot.edit_message_caption(chat_id=self.chat.id,
    #                                               message_id=message['message_id'],
    #                                               caption=product.text(w=self,
    #                                                                    cart_qty=cart[message['message_id']][
    #                                                                        1]),
    #                                               reply_markup=inline_keyboard)
    #
    #         # Create the keyboard with the cancel/go back button
    #         if category_mode:
    #             inline_keyboard = telegram.InlineKeyboardMarkup(
    #                 [[telegram.InlineKeyboardButton(self.loc.get("menu_go_back"),
    #                                                 callback_data="cart_go_back")]])
    #         else:
    #             inline_keyboard = telegram.InlineKeyboardMarkup(
    #                 [[telegram.InlineKeyboardButton(self.loc.get("menu_cancel"),
    #                                                 callback_data="cart_cancel")]])
    #
    #         # Send a message containing the button to cancel or pay
    #         final_msg = self.bot.send_message(self.chat.id,
    #                                           self.loc.get("conversation_cart_actions"),
    #                                           reply_markup=inline_keyboard)
    #
    #         # If cart has products, edit final message to display cart summary (Applies only to Category Mode)
    #         if cart and category_mode:
    #             hasQty = [v for k, v in cart.items() if v[1] > 0]
    #             if len(hasQty) > 0:
    #                 # Create the final inline keyboard
    #                 final_inline_keyboard = telegram.InlineKeyboardMarkup(
    #                     [
    #                         [telegram.InlineKeyboardButton(self.loc.get("menu_go_back"), callback_data="cart_go_back")],
    #                         [telegram.InlineKeyboardButton(self.loc.get("menu_done"), callback_data="cart_done")]
    #                     ])
    #                 self.bot.edit_message_text(
    #                     chat_id=self.chat.id,
    #                     message_id=final_msg.message_id,
    #                     text=self.loc.get("conversation_confirm_cart",
    #                                       product_list=self.__get_cart_summary(cart),
    #                                       total_cost=str(self.__get_cart_value(cart))),
    #                     reply_markup=final_inline_keyboard)
    #         # Wait for user input
    #         while True:
    #             callback = self.__wait_for_inlinekeyboard_callback()
    #             # React to the user input
    #
    #             # If the cancel button has been pressed...
    #             if callback.data == "cart_go_back":
    #                 # Stop waiting for user input and go back to the previous menu (Category selection)
    #                 break
    #             elif callback.data == "cart_cancel":
    #                 # Stop waiting for user input and go back to the main menu
    #                 return
    #             # If a Add to Cart button has been pressed...
    #             elif callback.data == "cart_add":
    #                 # Get the selected product, ensuring it exists
    #                 p = cart.get(callback.message.message_id)
    #                 if p is None:
    #                     continue
    #                 product = p[0]
    #                 # Add 1 copy to the cart
    #                 cart[callback.message.message_id][1] += 1
    #                 # Create the product inline keyboard
    #                 product_inline_keyboard = telegram.InlineKeyboardMarkup(
    #                     [
    #                         [telegram.InlineKeyboardButton(self.loc.get("menu_add_to_cart"),
    #                                                        callback_data="cart_add"),
    #                          telegram.InlineKeyboardButton(self.loc.get("menu_remove_from_cart"),
    #                                                        callback_data="cart_remove")]
    #                     ])
    #                 # Create the final inline keyboard
    #                 final_inline_keyboard_list = [[telegram.InlineKeyboardButton(self.loc.get("menu_done"),
    #                                                                              callback_data="cart_done")]]
    #                 if category_mode:
    #                     final_inline_keyboard_list.insert(0,
    #                                                       [telegram.InlineKeyboardButton(self.loc.get("menu_go_back"),
    #                                                                                      callback_data="cart_go_back")])
    #                 else:
    #                     final_inline_keyboard_list.insert(0, [telegram.InlineKeyboardButton(self.loc.get("menu_cancel"),
    #                                                                                         callback_data="cart_cancel")])
    #
    #                 final_inline_keyboard = telegram.InlineKeyboardMarkup(final_inline_keyboard_list)
    #
    #                 # Edit both the product and the final message
    #                 if product.image is None:
    #                     self.bot.edit_message_text(chat_id=self.chat.id,
    #                                                message_id=callback.message.message_id,
    #                                                text=product.text(w=self,
    #                                                                  cart_qty=cart[callback.message.message_id][1]),
    #                                                reply_markup=product_inline_keyboard)
    #                 else:
    #                     self.bot.edit_message_caption(chat_id=self.chat.id,
    #                                                   message_id=callback.message.message_id,
    #                                                   caption=product.text(w=self,
    #                                                                        cart_qty=cart[callback.message.message_id][
    #                                                                            1]),
    #                                                   reply_markup=product_inline_keyboard)
    #
    #                 self.bot.edit_message_text(
    #                     chat_id=self.chat.id,
    #                     message_id=final_msg.message_id,
    #                     text=self.loc.get("conversation_confirm_cart",
    #                                       product_list=self.__get_cart_summary(cart),
    #                                       total_cost=str(self.__get_cart_value(cart))),
    #                     reply_markup=final_inline_keyboard)
    #             # If the Remove from cart button has been pressed...
    #             elif callback.data == "cart_remove":
    #                 # Get the selected product, ensuring it exists
    #                 p = cart.get(callback.message.message_id)
    #                 if p is None:
    #                     continue
    #                 product = p[0]
    #                 # Remove 1 copy from the cart
    #                 if cart[callback.message.message_id][1] > 0:
    #                     cart[callback.message.message_id][1] -= 1
    #                 else:
    #                     continue
    #                 # Create the product inline keyboard
    #                 product_inline_list = [[telegram.InlineKeyboardButton(self.loc.get("menu_add_to_cart"),
    #                                                                       callback_data="cart_add")]]
    #                 if cart[callback.message.message_id][1] > 0:
    #                     product_inline_list[0].append(
    #                         telegram.InlineKeyboardButton(self.loc.get("menu_remove_from_cart"),
    #                                                       callback_data="cart_remove"))
    #                 product_inline_keyboard = telegram.InlineKeyboardMarkup(product_inline_list)
    #
    #                 # Create the final inline keyboard
    #                 final_inline_keyboard_list = [[telegram.InlineKeyboardButton(self.loc.get("menu_done"),
    #                                                                              callback_data="cart_done")]]
    #                 if category_mode:
    #                     final_inline_keyboard_list.insert(0,
    #                                                       [telegram.InlineKeyboardButton(self.loc.get("menu_go_back"),
    #                                                                                      callback_data="cart_go_back")])
    #                 else:
    #                     final_inline_keyboard_list.insert(0, [telegram.InlineKeyboardButton(self.loc.get("menu_cancel"),
    #                                                                                         callback_data="cart_cancel")])
    #
    #                 final_inline_keyboard = telegram.InlineKeyboardMarkup(final_inline_keyboard_list)
    #
    #                 # Edit the product message
    #                 if product.image is None:
    #                     self.bot.edit_message_text(chat_id=self.chat.id, message_id=callback.message.message_id,
    #                                                text=product.text(w=self,
    #                                                                  cart_qty=cart[callback.message.message_id][1]),
    #                                                reply_markup=product_inline_keyboard)
    #                 else:
    #                     self.bot.edit_message_caption(chat_id=self.chat.id,
    #                                                   message_id=callback.message.message_id,
    #                                                   caption=product.text(w=self,
    #                                                                        cart_qty=cart[callback.message.message_id][
    #                                                                            1]),
    #                                                   reply_markup=product_inline_keyboard)
    #
    #                 self.bot.edit_message_text(
    #                     chat_id=self.chat.id,
    #                     message_id=final_msg.message_id,
    #                     text=self.loc.get("conversation_confirm_cart",
    #                                       product_list=self.__get_cart_summary(cart),
    #                                       total_cost=str(self.__get_cart_value(cart))),
    #                     reply_markup=final_inline_keyboard)
    #             # If the done button has been pressed...
    #             elif callback.data == "cart_done":
    #                 # FinalStep being True will take us to the checkout in the next iteration instead of taking us back to category selection.
    #                 final_step = True
    #                 # End the loop
    #                 break
    #
    #         # if final_step and not category_mode:
    #         if final_step:
    #             # Create an inline keyboard with a single skip button
    #             cancel = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_skip"),
    #                                                                                    callback_data="cmd_cancel")]])
    #             # Ask if the user wants to add notes to the order
    #             self.bot.send_message(self.chat.id, self.loc.get("ask_order_notes"), reply_markup=cancel)
    #             # Wait for user input
    #             notes = self.__wait_for_regex(r"(.*)", cancellable=True)
    #             # Create a new Order
    #             order = db.Order(user=self.user,
    #                              creation_date=datetime.datetime.now(),
    #                              notes=notes if not isinstance(notes, CancelSignal) else "")
    #             # Add the record to the session and get an ID
    #             self.session.add(order)
    #             self.session.flush()
    #             # For each product added to the cart, create a new OrderItem
    #             for product in cart:
    #                 # Create {quantity} new OrderItems
    #                 for i in range(0, cart[product][1]):
    #                     order_item = db.OrderItem(product=cart[product][0],
    #                                               order_id=order.order_id)
    #                     self.session.add(order_item)
    #             # Ensure the user has enough credit to make the purchase
    #             credit_required = self.__get_cart_value(cart) - self.user.credit
    #             # Notify user in case of insufficient credit
    #             if credit_required > 0:
    #                 self.bot.send_message(self.chat.id, self.loc.get("error_not_enough_credit"))
    #                 # Suggest payment for missing credit value if configuration allows refill
    #                 if self.cfg["Payments"]["CreditCard"]["credit_card_token"] != "" \
    #                         and self.cfg["Appearance"]["refill_on_checkout"] \
    #                         and self.Price(self.cfg["Payments"]["CreditCard"]["min_amount"]) <= \
    #                         credit_required <= \
    #                         self.Price(self.cfg["Payments"]["CreditCard"]["max_amount"]):
    #                     self.__make_payment(self.Price(credit_required))
    #             # If afer requested payment credit is still insufficient (either payment failure or cancel)
    #             if self.user.credit < self.__get_cart_value(cart):
    #                 # Rollback all the changes
    #                 self.session.rollback()
    #                 # Take the user back to the main menu
    #                 return
    #             else:
    #                 # User has credit and valid order, perform transaction now
    #                 self.__order_transaction(order=order, value=-int(self.__get_cart_value(cart)))
    #                 # Take the user back to the main menu
    #                 return

    def __order_menu(self):
        """Display the order menu to the user."""
        log.debug("Displaying __order_menu")
        try:
            state = {"level": "main", "category": None, "subcategory": None}

            while True:
                if state["level"] == "main":
                    # Display main categories
                    categories = self.session.query(db.Category).filter_by(parent_id=None, deleted=False).all()
                    keyboard = []
                    for category in categories:
                        keyboard.append(
                            [telegram.InlineKeyboardButton(category.name, callback_data=f"cat_{category.id}")])
                    keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_cart"), callback_data="cart")])
                    keyboard.append(
                        [telegram.InlineKeyboardButton(self.loc.get("menu_main_menu"), callback_data="main_menu")])

                    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
                    self.bot.send_message(
                        chat_id=self.chat.id,
                        text=self.loc.get("conversation_order_category"),
                        reply_markup=reply_markup
                    )


                elif state["level"] == "category":

                    category = state["category"]

                    message = f"{category.name}\n\n"

                    if category.description:
                        message += f"{category.description}\n\n"

                    subcategories = self.session.query(db.Category).filter_by(parent_id=category.id,
                                                                              deleted=False).all()
                    keyboard = []
                    for subcategory in subcategories:
                        keyboard.append(
                            [telegram.InlineKeyboardButton(subcategory.name, callback_data=f"subcat_{subcategory.id}")])

                    if not subcategories:
                        # If no subcategories, show products
                        products = self.session.query(db.Product).filter_by(category_id=category.id,
                                                                            deleted=False).all()
                        for product in products:
                            keyboard.append([telegram.InlineKeyboardButton(
                                f"{product.name} - {self.Price(product.price)}", callback_data=f"prod_{product.id}")])

                    keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")])
                    keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_cart"), callback_data="cart")])
                    keyboard.append(
                        [telegram.InlineKeyboardButton(self.loc.get("menu_main_menu"), callback_data="main_menu")])

                    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

                    self.__send_message_with_photo(
                        chat_id=self.chat.id,
                        text=message,
                        photo=category.image,
                        reply_markup=reply_markup
                    )

                elif state["level"] == "subcategory":

                    subcategory = state["subcategory"]

                    message = f"{subcategory.name}\n\n"

                    if subcategory.description:
                        message += f"{subcategory.description}\n\n"

                    products = self.session.query(db.Product).filter_by(category_id=subcategory.id, deleted=False).all()
                    keyboard = []
                    for product in products:
                        keyboard.append([telegram.InlineKeyboardButton(f"{product.name} - {self.Price(product.price)}",
                                                                       callback_data=f"prod_{product.id}")])

                    keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")])
                    keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_cart"), callback_data="cart")])
                    keyboard.append(
                        [telegram.InlineKeyboardButton(self.loc.get("menu_main_menu"), callback_data="main_menu")])

                    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

                    self.__send_message_with_photo(
                        chat_id=self.chat.id,
                        text=message,
                        photo=subcategory.image,
                        reply_markup=reply_markup
                    )

                # Wait for user interaction
                callback_query = self.__wait_for_inlinekeyboard_callback()
                callback_data = callback_query.data

                if callback_data.startswith("cat_"):
                    category_id = int(callback_data.split("_")[1])
                    state["category"] = self.session.query(db.Category).get(category_id)
                    state["level"] = "category"
                elif callback_data.startswith("subcat_"):
                    subcategory_id = int(callback_data.split("_")[1])
                    state["subcategory"] = self.session.query(db.Category).get(subcategory_id)
                    state["level"] = "subcategory"
                elif callback_data.startswith("prod_"):
                    product_id = int(callback_data.split("_")[1])
                    result = self.__display_product(product_id, parent_level=state["level"])
                    if result == "category":
                        state["level"] = "category"
                        state["subcategory"] = None
                    elif result == "subcategory":
                        state["level"] = "subcategory"
                    elif result == "main":
                        state["level"] = "main"
                        state["category"] = None
                        state["subcategory"] = None
                elif callback_data == "back":
                    if state["level"] == "subcategory":
                        state["level"] = "category"
                        state["subcategory"] = None
                    elif state["level"] == "category":
                        state["level"] = "main"
                        state["category"] = None
                elif callback_data == "cart":
                    self.__display_cart()
                elif callback_data == "main_menu":
                    return


        except Exception as e:
            log.error(f"Error in __order_menu: {e}")
            self.bot.send_message(chat_id=self.chat.id, text=f"An error occurred: {e}")

    def __display_product(self, product_id, message_id=None, parent_level=None):
        """Display product information and allow adding/removing from cart."""
        product = self.session.query(db.Product).get(product_id)
        if not product or product.deleted:
            self.bot.send_message(chat_id=self.chat.id, text=self.loc.get("error_product_not_found"))
            return parent_level

        while True:
            cart_qty = 0
            if hasattr(self, 'cart') and product.id in self.cart:
                cart_qty = self.cart[product.id]['quantity']

            message = f"{product.name}\n\n"
            if product.description:
                message += f"{product.description}\n\n"
            message += f"{self.loc.get('product_price')}: {self.Price(product.price)}\n"
            if cart_qty > 0:
                message += f"{self.loc.get('product_in_cart')}: {cart_qty} {self.loc.get('product_pieces')}\n"
                message += f"{self.loc.get('product_subtotal')}: {self.Price(product.price * cart_qty)}\n"

            keyboard = [
                [telegram.InlineKeyboardButton(self.loc.get("menu_add_to_cart"), callback_data=f"add_{product.id}")]
            ]
            if cart_qty > 0:
                keyboard[0].append(telegram.InlineKeyboardButton(self.loc.get("menu_remove_from_cart"),
                                                                 callback_data=f"remove_{product.id}"))

            keyboard.append(
                [telegram.InlineKeyboardButton(self.loc.get("menu_go_to_cart"), callback_data="go_to_cart")])
            keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")])
            keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_main_menu"), callback_data="main_menu")])

            reply_markup = telegram.InlineKeyboardMarkup(keyboard)

            try:
                if message_id:
                    if product.image:
                        self.bot.edit_message_media(
                            chat_id=self.chat.id,
                            message_id=message_id,
                            media=telegram.InputMediaPhoto(product.image, caption=message),
                            reply_markup=reply_markup
                        )
                    else:
                        self.bot.edit_message_text(
                            chat_id=self.chat.id,
                            message_id=message_id,
                            text=message,
                            reply_markup=reply_markup
                        )
                else:
                    if product.image:
                        sent_message = self.bot.send_photo(
                            chat_id=self.chat.id,
                            photo=product.image,
                            caption=message,
                            reply_markup=reply_markup
                        )
                    else:
                        sent_message = self.bot.send_message(
                            chat_id=self.chat.id,
                            text=message,
                            reply_markup=reply_markup
                        )
                    message_id = sent_message.message_id
            except telegram.error.BadRequest as e:
                log.error(f"Error updating product message: {e}")
                # Якщо виникла помилка при оновленні, спробуємо надіслати нове повідомлення
                if product.image:
                    sent_message = self.bot.send_photo(
                        chat_id=self.chat.id,
                        photo=product.image,
                        caption=message,
                        reply_markup=reply_markup
                    )
                else:
                    sent_message = self.bot.send_message(
                        chat_id=self.chat.id,
                        text=message,
                        reply_markup=reply_markup
                    )
                message_id = sent_message.message_id

            callback = self.__wait_for_inlinekeyboard_callback()
            callback_data = callback.data

            if callback_data.startswith("add_"):
                self.__add_to_cart(product)
                self.bot.answer_callback_query(callback.id, text=self.loc.get("product_added_to_cart"))
            elif callback_data.startswith("remove_"):
                self.__remove_from_cart(product)
                self.bot.answer_callback_query(callback.id, text=self.loc.get("product_removed_from_cart"))
            elif callback_data == "go_to_cart":
                return self.__cart_menu()
            elif callback_data == "back":
                return parent_level
            elif callback_data == "main_menu":
                return self.__user_menu()

    def __edit_message_with_photo(self, chat_id, message_id, text, photo, reply_markup=None):
        """Edit a message with photo, splitting it if the text is too long."""
        if len(text) > 1024 and photo:
            self.bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=telegram.InputMediaPhoto(photo)
            )
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id + 1,
                text=text,
                reply_markup=reply_markup
            )
        elif photo:
            self.bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=telegram.InputMediaPhoto(photo, caption=text),
                reply_markup=reply_markup
            )
        else:
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup
            )

    def __add_to_cart(self, product):
        """Add a product to the cart."""
        if not hasattr(self, 'cart'):
            self.cart = {}

        if product.id in self.cart:
            self.cart[product.id]['quantity'] += 1
        else:
            self.cart[product.id] = {'product': product, 'quantity': 1}

    def __remove_from_cart(self, product):
        """Remove a product from the cart."""
        if hasattr(self, 'cart') and product.id in self.cart:
            self.cart[product.id]['quantity'] -= 1
            if self.cart[product.id]['quantity'] <= 0:
                del self.cart[product.id]

    def __display_cart(self):
        """Display the contents of the cart."""
        while True:
            if not hasattr(self, 'cart') or not self.cart:
                self.bot.send_message(self.chat.id, self.loc.get("cart_empty"))
                return

            message = self.loc.get("cart_contents") + "\n\n"
            total = 0
            for product_id, item in self.cart.items():
                product = item['product']
                quantity = item['quantity']
                subtotal = product.price * quantity
                total += subtotal
                message += f"{product.name} x{quantity}: {self.Price(subtotal)}\n"

            message += f"\n{self.loc.get('cart_total')}: {self.Price(total)}"

            keyboard = [
                [telegram.InlineKeyboardButton(self.loc.get("menu_checkout"), callback_data="checkout")],
                [telegram.InlineKeyboardButton(self.loc.get("menu_clear_cart"), callback_data="clear_cart")],
                [telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")]
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)

            self.bot.send_message(self.chat.id, message, reply_markup=reply_markup)

            callback_query = self.__wait_for_inlinekeyboard_callback()
            callback_data = callback_query.data

            if callback_data == "checkout":
                self.__checkout()
            elif callback_data == "clear_cart":
                self.cart = {}
                self.bot.answer_callback_query(callback_query.id, text=self.loc.get("cart_cleared"))
                return
            elif callback_data == "back":
                return

    def __checkout(self):
        """Process the checkout."""
        log.debug("Processing checkout")

        if not hasattr(self, 'cart') or not self.cart:
            self.bot.send_message(self.chat.id, self.loc.get("cart_empty"))
            return

        # Обчислюємо загальну вартість замовлення
        total = sum(item['product'].price * item['quantity'] for item in self.cart.values())

        # Перевіряємо, чи достатньо коштів
        if self.user.credit < total:
            shortage = total - self.user.credit
            message = self.loc.get("insufficient_funds",
                                   total=self.Price(total),
                                   balance=self.Price(self.user.credit),
                                   shortage=self.Price(shortage))

            # Створюємо інлайн клавіатуру з двома кнопками
            keyboard = [
                [telegram.InlineKeyboardButton(self.loc.get("add_funds"), callback_data="add_funds")],
                [telegram.InlineKeyboardButton(self.loc.get("return_to_main_menu"), callback_data="main_menu")]
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)

            # Відправляємо повідомлення з кнопками
            self.bot.send_message(self.chat.id, message, reply_markup=reply_markup)

            # Очікуємо відповідь користувача
            callback = self.__wait_for_inlinekeyboard_callback()
            if callback.data == "add_funds":
                self.__add_credit_menu()
                # Після поповнення повертаємось до головного меню
                return self.__user_menu()
            elif callback.data == "main_menu":
                return self.__user_menu()

            return

        # Вибір способу доставки
        delivery_result = self.__choose_delivery_method()

        if delivery_result[0] == "back_to_cart":
            return self.__cart_menu()
        elif delivery_result[0] == "cancel_order":
            self.bot.send_message(self.chat.id, self.loc.get("order_canceled"))
            self.cart = {}  # Очищаємо кошик
            return self.__user_menu()
        elif delivery_result[0] is None or delivery_result == (None, None):
            self.bot.send_message(self.chat.id, self.loc.get("error_checkout_canceled"))
            return
        else:
            delivery_method, delivery_info = delivery_result
            total += delivery_method.price

        # Запитуємо додаткові примітки
        skip_button = telegram.InlineKeyboardMarkup([[
            telegram.InlineKeyboardButton(self.loc.get("menu_skip"), callback_data="skip_notes")
        ]])
        self.bot.send_message(self.chat.id, self.loc.get("ask_order_notes"), reply_markup=skip_button)

        notes_response = self.__wait_for_regex_or_callback_2(r".*", cancellable=True)
        if isinstance(notes_response, CancelSignal):
            self.bot.send_message(self.chat.id, self.loc.get("checkout_canceled"))
            return
        elif isinstance(notes_response, str):
            notes = notes_response
        else:  # skip_notes callback
            notes = None

        # Створюємо замовлення
        order = db.Order(
            user=self.user,
            delivery_method=delivery_method,
            creation_date=datetime.datetime.now(),
            notes=f"{notes}\n\n{delivery_info}" if notes else delivery_info
        )
        self.session.add(order)

        # Додаємо товари до замовлення
        for product_id, item in self.cart.items():
            order_item = db.OrderItem(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            self.session.add(order_item)

        # Створюємо транзакцію
        transaction = db.Transaction(
            user=self.user,
            value=-total,
            order=order,
            notes=f"Оплата замовлення"
        )
        self.session.add(transaction)

        # Оновлюємо баланс користувача
        self.user.credit -= total

        # Очищуємо кошик
        self.cart = {}

        # Зберігаємо зміни
        try:
            self.session.commit()
            # Тепер, після commit(), замовлення має id
            order_id = order.order_id

            # Відправляємо підтвердження
            confirmation_message = self.loc.get("order_confirmation",
                                                order_id=order_id,
                                                total=self.Price(total),
                                                delivery_method=delivery_method.name)
            self.bot.send_message(self.chat.id, confirmation_message)

            # Повідомляємо адміністраторів
            self.__order_notify_admins(order=order)

            log.info(f"Order {order_id} has been successfully created for user {self.user.user_id}")

            self.cart = {}
            if hasattr(self, 'cart_message_id'):
                try:
                    self.bot.delete_message(chat_id=self.chat.id, message_id=self.cart_message_id)
                except Exception as e:
                    log.error(f"Error deleting cart message: {e}")
                delattr(self, 'cart_message_id')

            # Викликаємо функцію для вибору подальших дій
            self.__post_order_options()

        except Exception as e:
            log.error(f"Error during checkout: {e}")
            self.session.rollback()
            self.bot.send_message(self.chat.id, self.loc.get("error_during_checkout"))
            return

    def __get_order_notes(self):
        skip_button = telegram.InlineKeyboardMarkup([[
            telegram.InlineKeyboardButton(self.loc.get("menu_skip"), callback_data="skip_notes"),
            telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")
        ]])
        self.bot.send_message(self.chat.id, self.loc.get("ask_order_notes"), reply_markup=skip_button)

        response = self.__wait_for_regex_or_callback(r".*", cancellable=True)
        if isinstance(response, telegram.CallbackQuery):
            if response.data == "skip_notes":
                return None
            elif response.data == "back":
                return "back"
        else:
            return response

    def __create_order(self, delivery_method, delivery_info, notes, total):
        order = db.Order(
            user=self.user,
            delivery_method=delivery_method,
            creation_date=datetime.datetime.now(),
            notes=f"{notes}\n\n{delivery_info}" if notes else delivery_info
        )
        self.session.add(order)

        for product_id, item in self.cart.items():
            order_item = db.OrderItem(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            self.session.add(order_item)

        transaction = db.Transaction(
            user=self.user,
            value=-total,
            order=order,
            notes="Оплата замовлення"
        )
        self.session.add(transaction)

        self.user.credit -= total
        self.cart = {}

        self.session.commit()
        return order

    def __send_order_confirmation(self, order):
        confirmation_message = self.loc.get("order_confirmation",
                                            order_id=order.order_id,
                                            total=self.Price(order.transaction.value),
                                            delivery_method=order.delivery_method.name)
        self.bot.send_message(self.chat.id, confirmation_message)

    def __ask_order_notes(self):
        """Ask for additional order notes."""
        skip_button = telegram.InlineKeyboardMarkup([[
            telegram.InlineKeyboardButton(self.loc.get("menu_skip"), callback_data="skip_notes"),
            telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")
        ]])
        self.bot.send_message(self.chat.id, self.loc.get("ask_order_notes"), reply_markup=skip_button)

        response = self.__wait_for_regex_or_callback(r".*", cancellable=True)
        if isinstance(response, CancelSignal):
            return None
        elif isinstance(response, telegram.CallbackQuery):
            if response.data == "skip_notes":
                return None
            elif response.data == "back":
                return "back"
        else:
            return response

    def __post_order_options(self):
        """Provide options to the user after completing an order."""
        keyboard = [
            [telegram.InlineKeyboardButton(self.loc.get("continue_shopping"), callback_data="continue_shopping")],
            [telegram.InlineKeyboardButton(self.loc.get("return_to_main_menu"), callback_data="main_menu")]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)

        self.bot.send_message(
            chat_id=self.chat.id,
            text=self.loc.get("post_order_options"),
            reply_markup=reply_markup
        )

        while True:
            callback = self.__wait_for_inlinekeyboard_callback()
            if callback.data == "continue_shopping":
                self.__order_menu()
                break
            elif callback.data == "main_menu":
                self.__user_menu()
                break

    def __choose_delivery_method(self):
        """Allow user to choose a delivery method and provide necessary information."""
        log.debug("Entering __choose_delivery_method")
        while True:
            delivery_methods = self.session.query(db.DeliveryMethod).filter_by(is_active=True).all()

            if not delivery_methods:
                self.bot.send_message(self.chat.id, self.loc.get("error_no_delivery_methods"))
                return None, None

            keyboard = []
            for method in delivery_methods:
                if method.name == "Самовивіз":
                    pickup_points = self.session.query(db.PickupPoint).filter_by(is_active=True).all()
                    if not pickup_points:
                        continue
                keyboard.append([telegram.InlineKeyboardButton(method.name, callback_data=f"delivery_{method.id}")])

            keyboard.append([
                telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back_to_cart"),
                telegram.InlineKeyboardButton(self.loc.get("cancel_order"), callback_data="cancel_order")
            ])

            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            self.bot.send_message(
                chat_id=self.chat.id,
                text=self.loc.get("choose_delivery_method"),
                reply_markup=reply_markup
            )

            callback = self.__wait_for_inlinekeyboard_callback()
            if callback.data == "back_to_cart":
                log.info("User chose to go back to cart")
                return "back_to_cart", None
            elif callback.data == "cancel_order":
                log.info("User chose to cancel the order")
                return "cancel_order", None
            elif callback.data.startswith("delivery_"):
                delivery_id = int(callback.data.split("_")[1])
                delivery_method = self.session.query(db.DeliveryMethod).get(delivery_id)
                log.info(f"User chose delivery method: {delivery_method.name}")

                delivery_info = self.__get_delivery_info(delivery_method)
                if delivery_info == "back":
                    log.info("User chose to go back from delivery info")
                    continue  # Повертаємося до вибору способу доставки
                elif delivery_info is None:
                    log.info("Delivery info is None, returning to delivery method selection")
                    continue  # Повертаємося до вибору способу доставки

                # Підтвердження вибору способу доставки
                confirm = self.__confirm_delivery_method(delivery_method, delivery_info)
                if confirm == "back":
                    log.info("User chose to go back from delivery confirmation")
                    continue  # Повертаємося до вибору способу доставки
                elif confirm == "cancel":
                    log.info("User chose to cancel from delivery confirmation")
                    return "cancel_order", None  # Скасовуємо замовлення
                elif confirm:
                    log.info(f"User confirmed delivery method: {delivery_method.name}")
                    return delivery_method, delivery_info

        log.debug("Exiting __choose_delivery_method")

    def __get_delivery_info(self, delivery_method):
        if delivery_method.name == "Самовивіз":
            return self.__choose_pickup_point()
        elif delivery_method.name == "Нова пошта":
            return self.__get_nova_poshta_info()
        elif delivery_method.name == "По Києву":
            return self.__get_kyiv_delivery_info()

    def __confirm_delivery_method(self, delivery_method, delivery_info):
        confirm_keyboard = [
            [telegram.InlineKeyboardButton(self.loc.get("confirm"), callback_data="confirm")],
            [telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")],
            [telegram.InlineKeyboardButton(self.loc.get("cancel_order"), callback_data="cancel")]
        ]
        confirm_markup = telegram.InlineKeyboardMarkup(confirm_keyboard)

        confirm_message = self.loc.get("confirm_delivery_method",
                                       method=delivery_method.name,
                                       price=self.Price(delivery_method.price),
                                       info=delivery_info)

        self.bot.send_message(self.chat.id, confirm_message, reply_markup=confirm_markup)

        confirm_callback = self.__wait_for_inlinekeyboard_callback()
        return confirm_callback.data

    def __choose_pickup_point(self):
        """Allow user to choose a pickup point."""
        pickup_points = self.session.query(db.PickupPoint).filter_by(is_active=True).all()

        if not pickup_points:
            self.bot.send_message(self.chat.id, self.loc.get("error_no_pickup_points"))
            return None

        keyboard = []
        for point in pickup_points:
            keyboard.append([telegram.InlineKeyboardButton(point.address, callback_data=f"pickup_{point.id}")])

        keyboard.append([telegram.InlineKeyboardButton(self.loc.get("menu_back"), callback_data="back")])

        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        self.bot.send_message(
            chat_id=self.chat.id,
            text=self.loc.get("choose_pickup_point"),
            reply_markup=reply_markup
        )

        while True:
            callback = self.__wait_for_inlinekeyboard_callback()
            if callback.data.startswith("pickup_"):
                pickup_id = int(callback.data.split("_")[1])
                pickup_point = self.session.query(db.PickupPoint).get(pickup_id)
                # Повертаємо рядок з інформацією про точку самовивозу, а не об'єкт
                return f"Адреса: {pickup_point.address}" + (
                    f", {pickup_point.description}" if pickup_point.description else "")
            elif callback.data == "back":
                return None

    def __get_nova_poshta_info(self):
        """Get Nova Poshta delivery information from the user."""
        nova_poshta_info = {}

        while True:
            self.bot.send_message(self.chat.id, self.loc.get("ask_nova_poshta_city"))
            city = self.__wait_for_regex_or_back(r".*")
            if city == "back":
                return "back"
            nova_poshta_info['city'] = city

            self.bot.send_message(self.chat.id, self.loc.get("ask_nova_poshta_office"))
            office = self.__wait_for_regex_or_back(r"\d+")
            if office == "back":
                continue
            nova_poshta_info['office'] = office

            self.bot.send_message(self.chat.id, self.loc.get("ask_nova_poshta_phone"))
            phone = self.__wait_for_regex_or_back(r"\+?\d+")
            if phone == "back":
                continue
            nova_poshta_info['phone'] = phone

            self.bot.send_message(self.chat.id, self.loc.get("ask_nova_poshta_name"))
            name = self.__wait_for_regex_or_back(r".*")
            if name == "back":
                continue
            nova_poshta_info['name'] = name

            return f"Місто: {nova_poshta_info['city']}, Відділення: {nova_poshta_info['office']}, Телефон: {nova_poshta_info['phone']}, ПІБ: {nova_poshta_info['name']}"

    def __get_kyiv_delivery_info(self):
        """Get Kyiv delivery information from the user."""
        self.bot.send_message(self.chat.id, self.loc.get("ask_kyiv_address"))
        address = self.__wait_for_regex_or_back(r".*")
        if isinstance(address, CancelSignal) or address == "back":
            return None

        self.bot.send_message(self.chat.id, self.loc.get("ask_kyiv_phone"))
        phone = self.__wait_for_regex_or_back(r"\+?\d+")
        if isinstance(phone, CancelSignal) or phone == "back":
            return None

        return f"Адреса: {address}, Телефон: {phone}"

    def __get_cart_value(self, cart):
        # Calculate total items value in cart
        value = self.Price(0)
        for product in cart:
            value += cart[product][0].price * cart[product][1]
        return value

    def __get_cart_summary(self, cart):
        # Create the cart summary
        product_list = ""
        for product_id in cart:
            if cart[product_id][1] > 0:
                product_list += cart[product_id][0].text(w=self,
                                                         style="short",
                                                         cart_qty=cart[product_id][1]) + "\n"
        return product_list

    def __order_transaction(self, order, value):
        # Create a new transaction and add it to the session
        transaction = db.Transaction(user=self.user,
                                     value=value,
                                     order=order)
        self.session.add(transaction)
        # Commit all the changes
        self.session.commit()
        # Update the user's credit
        self.user.recalculate_credit()
        # Commit all the changes
        self.session.commit()
        # Notify admins about new transation
        self.__order_notify_admins(order=order)

    def __order_notify_admins(self, order):
        # Notify the user of the order result
        self.bot.send_message(self.chat.id, self.loc.get("success_order_created", order=order.text(w=self,
                                                                                                   user=True)))
        # Notify the admins (in Live Orders mode) of the new order
        admins = self.session.query(db.Admin).filter_by(live_mode=True).all()
        # Create the order keyboard
        order_keyboard = telegram.InlineKeyboardMarkup(
            [
                [telegram.InlineKeyboardButton(self.loc.get("menu_complete"), callback_data="order_complete")],
                [telegram.InlineKeyboardButton(self.loc.get("menu_refund"), callback_data="order_refund")]
            ])
        # Notify them of the new placed order
        for admin in admins:
            self.bot.send_message(admin.user_id,
                                  self.loc.get('notification_order_placed',
                                               order=order.text(w=self)),
                                  reply_markup=order_keyboard)

    def __order_status(self):
        """Display the status of the sent orders."""
        log.debug("Displaying __order_status")
        # Find the latest orders
        orders = self.session.query(db.Order) \
            .filter(db.Order.user == self.user) \
            .order_by(db.Order.creation_date.desc()) \
            .limit(20) \
            .all()
        # Ensure there is at least one order to display
        if len(orders) == 0:
            self.bot.send_message(self.chat.id, self.loc.get("error_no_orders"))
        # Display the order status to the user
        for order in orders:
            self.bot.send_message(self.chat.id, order.text(w=self, user=True))
        # TODO: maybe add a page displayer instead of showing the latest 5 orders

    def __add_credit_menu(self):
        """Add more credit to the account."""
        log.debug("Displaying __add_credit_menu")
        # Create a payment methods keyboard
        keyboard = list()
        # Add the supported payment methods to the keyboard
        # Cash
        if self.cfg["Payments"]["Cash"]["enable_pay_with_cash"]:
            keyboard.append([telegram.KeyboardButton(self.loc.get("menu_cash"))])
        # Telegram Payments
        if self.cfg["Payments"]["CreditCard"]["credit_card_token"] != "":
            keyboard.append([telegram.KeyboardButton(self.loc.get("menu_credit_card"))])
        # Bitcoin Payments
        if self.cfg["Bitcoin"]["api_key"] != "":
            keyboard.append([telegram.KeyboardButton("🛡 Bitcoin")])
        # Keyboard: go back to the previous menu
        keyboard.append([telegram.KeyboardButton(self.loc.get("menu_cancel"))])
        # Send the keyboard to the user
        self.bot.send_message(self.chat.id, self.loc.get("conversation_payment_method"),
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        # Wait for a reply from the user
        selection = self.__wait_for_specific_message(
            [self.loc.get("menu_cash"), self.loc.get("menu_credit_card"), "🛡 Bitcoin", self.loc.get("menu_cancel")],
            cancellable=True)

        # If the user has selected the Cash option...
        if selection == self.loc.get("menu_cash") and self.cfg["Payments"]["Cash"]["enable_pay_with_cash"]:
            # Go to the pay with cash function
            self.bot.send_message(self.chat.id,
                                  self.loc.get("payment_cash", user_cash_id=self.user.identifiable_str()))
            # Повертаємось до головного меню після показу інформації про оплату готівкою
            return self.__user_menu()
        # If the user has selected the Credit Card option...
        elif selection == self.loc.get("menu_credit_card") and self.cfg["Payments"]["CreditCard"]["credit_card_token"]:
            # Go to the pay with credit card function
            self.__add_credit_cc()
            # Повертаємось до головного меню після завершення оплати карткою
            return self.__user_menu()
        # If the user has selected the Bitcoin option...
        elif selection == "🛡 Bitcoin":
            # Go to the pay with bitcoin function
            self.__add_credit_btc()
            # Повертаємось до головного меню після завершення оплати біткоїном
            return self.__user_menu()
        # If the user has selected the Cancel option...
        elif isinstance(selection, CancelSignal):
            # Send him back to the previous menu
            return self.__user_menu()

    def __add_credit_cc(self):
        """Add money to the wallet through a credit card payment."""
        log.debug("Displaying __add_credit_cc")
        # Create a keyboard to be sent later
        presets = self.cfg["Payments"]["CreditCard"]["payment_presets"]
        keyboard = [[telegram.KeyboardButton(str(self.Price(preset)))] for preset in presets]
        keyboard.append([telegram.KeyboardButton(self.loc.get("menu_cancel"))])
        # Boolean variable to check if the user has cancelled the action
        cancelled = False
        # Loop used to continue asking if there's an error during the input
        while not cancelled:
            # Send the message and the keyboard
            self.bot.send_message(self.chat.id, self.loc.get("payment_cc_amount"),
                                  reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            # Wait until a valid amount is sent
            selection = self.__wait_for_regex(r"([0-9]+(?:[.,][0-9]+)?|" + self.loc.get("menu_cancel") + r")",
                                              cancellable=True)
            # If the user cancelled the action
            if isinstance(selection, CancelSignal):
                # Exit the loop
                cancelled = True
                continue
            # Convert the amount to an integer
            value = self.Price(selection)
            # Ensure the amount is within the range
            if value > self.Price(self.cfg["Payments"]["CreditCard"]["max_amount"]):
                self.bot.send_message(self.chat.id,
                                      self.loc.get("error_payment_amount_over_max",
                                                   max_amount=self.Price(self.cfg["CreditCard"]["max_amount"])))
                continue
            elif value < self.Price(self.cfg["Payments"]["CreditCard"]["min_amount"]):
                self.bot.send_message(self.chat.id,
                                      self.loc.get("error_payment_amount_under_min",
                                                   min_amount=self.Price(self.cfg["CreditCard"]["min_amount"])))
                continue
            break
        # If the user cancelled the action...
        else:
            # Exit the function
            return
        # Issue the payment invoice
        self.__make_payment(amount=value)

    def __make_payment(self, amount):
        # Set the invoice active invoice payload
        self.invoice_payload = str(uuid.uuid4())
        # Create the price array
        prices = [telegram.LabeledPrice(label=self.loc.get("payment_invoice_label"), amount=int(amount))]
        # If the user has to pay a fee when using the credit card, add it to the prices list
        fee = int(self.__get_total_fee(amount))
        if fee > 0:
            prices.append(telegram.LabeledPrice(label=self.loc.get("payment_invoice_fee_label"),
                                                amount=fee))
        # Create the invoice keyboard
        inline_keyboard = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_pay"),
                                                                                        pay=True)],
                                                         [telegram.InlineKeyboardButton(self.loc.get("menu_cancel"),
                                                                                        callback_data="cmd_cancel")]])
        # The amount is valid, send the invoice
        self.bot.send_invoice(self.chat.id,
                              title=self.loc.get("payment_invoice_title"),
                              description=self.loc.get("payment_invoice_description", amount=str(amount)),
                              payload=self.invoice_payload,
                              provider_token=self.cfg["Payments"]["CreditCard"]["credit_card_token"],
                              start_parameter="tempdeeplink",
                              currency=self.cfg["Payments"]["currency"],
                              prices=prices,
                              need_name=self.cfg["Payments"]["CreditCard"]["name_required"],
                              need_email=self.cfg["Payments"]["CreditCard"]["email_required"],
                              need_phone_number=self.cfg["Payments"]["CreditCard"]["phone_required"],
                              reply_markup=inline_keyboard,
                              max_tip_amount=self.cfg["Payments"]["CreditCard"]["max_tip_amount"],
                              suggested_tip_amounts=self.cfg["Payments"]["CreditCard"]["tip_presets"],
                              )
        # Wait for the precheckout query
        precheckoutquery = self.__wait_for_precheckoutquery(cancellable=True)
        # Check if the user has cancelled the invoice
        if isinstance(precheckoutquery, CancelSignal):
            # Exit the function
            return
        # Accept the checkout
        self.bot.answer_pre_checkout_query(precheckoutquery.id, ok=True)
        # Wait for the payment
        successfulpayment = self.__wait_for_successfulpayment(cancellable=False)
        # Create a new database transaction
        transaction = db.Transaction(user=self.user,
                                     value=int(amount),
                                     provider="Credit Card",
                                     telegram_charge_id=successfulpayment.telegram_payment_charge_id,
                                     provider_charge_id=successfulpayment.provider_payment_charge_id)

        if successfulpayment.order_info is not None:
            transaction.payment_name = successfulpayment.order_info.name
            transaction.payment_email = successfulpayment.order_info.email
            transaction.payment_phone = successfulpayment.order_info.phone_number
        # Update the user's credit
        self.user.recalculate_credit()
        # Commit all the changes
        self.session.commit()

    def __add_credit_btc(self):
        """Add money to the wallet through a bitcoin payment."""
        log.debug("Displaying __add_credit_btc")
        # Create a keyboard to be sent later
        presets = self.cfg["Payments"]["CreditCard"]["payment_presets"]
        keyboard = [[telegram.KeyboardButton(str(self.Price(preset)))] for preset in presets]
        keyboard.append([telegram.KeyboardButton(self.loc.get("menu_cancel"))])
        # Boolean variable to check if the user has cancelled the action
        cancelled = False
        raw_value = 0
        # Loop used to continue asking if there's an error during the input
        while not cancelled:
            # Send the message and the keyboard
            self.bot.send_message(self.chat.id, self.loc.get("payment_cc_amount"),
                                  reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            # Wait until a valid amount is sent
            selection = self.__wait_for_regex(r"([0-9]+(?:[.,][0-9]+)?|" + self.loc.get("menu_cancel") + r")",
                                              cancellable=True)
            # If the user cancelled the action
            if isinstance(selection, CancelSignal):
                # Exit the loop
                cancelled = True
                continue
            raw_value = selection
            # Convert the amount to an integer
            value = self.Price(selection)
            break
        # If the user cancelled the action...
        else:
            # Exit the function
            return
        # Set the invoice active invoice payload
        self.invoice_payload = str(uuid.uuid4())
        # The amount is valid, fetch btc amount and address
        btc_price = Blockonomics.fetch_new_btc_price()
        satoshi_amount = int(1.0e8 * float(raw_value) / float(btc_price))
        btc_amount = satoshi_amount / 1.0e8
        # Check to re-use address
        transaction = self.session.query(db.BtcTransaction).filter(
            db.BtcTransaction.user_id == self.user.user_id).filter(db.BtcTransaction.status == -1).one_or_none()
        if transaction:
            btc_address = transaction.address
            # Update btc_price, satoshi, currency, timestamp
            transaction.btc_price = btc_price
            transaction.currency = self.cfg["Payments"]["currency"]
            transaction.timestamp = datetime.datetime.now()
        else:
            btc_address = Blockonomics.new_address().json()["address"]
            # Create a new database btc transaction
            new_transaction = db.BtcTransaction(user=self.user,
                                                price=btc_price,
                                                value=0,
                                                currency=self.cfg["Payments"]["currency"],
                                                status=-1,
                                                timestamp=datetime.datetime.now(),
                                                address=btc_address,
                                                txid='')
            #Add and commit the btc transaction
            self.session.add(new_transaction)
        self.session.commit()
        # Send a message containing the btc pay info
        self.__send_btc_payment_info(btc_address, btc_amount)

    def __get_total_fee(self, amount):
        # Calculate a fee for the required amount
        fee_percentage = self.cfg["Payments"]["CreditCard"]["fee_percentage"] / 100
        fee_fixed = self.cfg["Payments"]["CreditCard"]["fee_fixed"]
        total_fee = amount * fee_percentage + fee_fixed
        if total_fee > 0:
            return total_fee
        # Set the fee to 0 to ensure no accidental discounts are applied
        return 0

    def __bot_info(self):
        """Send information about the bot."""
        log.debug("Displaying __bot_info")
        self.bot.send_message(self.chat.id, self.loc.get("bot_info"))

    def __admin_menu(self):
        """Function called from the run method when the user is an administrator.
           Administrative bot actions should be placed here."""
        log.debug("Displaying __admin_menu")
        while True:
            # Create a keyboard with the admin main menu based on the admin permissions specified in the db
            keyboard = []
            if self.admin.edit_products:
                keyboard.append([self.loc.get("menu_products")])
            if self.admin.edit_categories or self.admin.edit_subcategories:
                keyboard.append([self.loc.get("menu_categories")])
            if self.admin.receive_orders:
                keyboard.append([self.loc.get("menu_orders")])
            if self.admin.create_transactions:
                keyboard.append([self.loc.get("menu_edit_credit")])
                keyboard.append([self.loc.get("menu_transactions"), self.loc.get("menu_csv")])
                keyboard.append([self.loc.get("menu_manage_promocodes")])
                keyboard.append([self.loc.get("menu_broadcast_message")])
            if self.admin.is_owner:
                keyboard.append([self.loc.get("menu_edit_admins")])
            keyboard.append([self.loc.get("menu_user_mode")])

            # Send the previously created keyboard to the user (ensuring it can be clicked only 1 time)
            self.bot.send_message(self.chat.id, self.loc.get("conversation_open_admin_menu"),
                                  reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

            # Wait for a reply from the user
            selection = self.__wait_for_specific_message([item for sublist in keyboard for item in sublist])

            # Handle user selection
            if selection == self.loc.get("menu_products"):
                self.__products_menu()
            elif selection == self.loc.get("menu_categories"):
                self.__categories_menu()
            elif selection == self.loc.get("menu_orders"):
                self.__orders_menu()
            elif selection == self.loc.get("menu_edit_credit"):
                self.__create_transaction()
            elif selection == self.loc.get("menu_user_mode"):
                self.bot.send_message(self.chat.id, self.loc.get("conversation_switch_to_user_mode"))
                self.__user_menu()
            elif selection == self.loc.get("menu_edit_admins"):
                self.__add_admin()
            elif selection == self.loc.get("menu_transactions"):
                self.__transaction_pages()
            elif selection == self.loc.get("menu_csv"):
                self.__transactions_file()
            elif selection == self.loc.get("menu_broadcast_message"):
                self.__broadcast_message()
            elif selection == self.loc.get("menu_manage_promocodes"):
                self.__manage_promocodes()

    def __manage_promocodes(self):
        """Manage promocodes: create, delete, view statistics."""
        while True:
            keyboard = [
                [self.loc.get("menu_create_promocode")],
                [self.loc.get("menu_list_promocodes")],
                [self.loc.get("menu_delete_promocode")],
                [self.loc.get("menu_back")]
            ]
            reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            self.bot.send_message(self.chat.id, self.loc.get("promocode_management_menu"), reply_markup=reply_markup)

            selection = self.__wait_for_specific_message(
                [self.loc.get("menu_create_promocode"),
                 self.loc.get("menu_list_promocodes"),
                 self.loc.get("menu_delete_promocode"),
                 self.loc.get("menu_back")],
                cancellable=True
            )

            if selection == self.loc.get("menu_create_promocode"):
                self.__create_promocode()
            elif selection == self.loc.get("menu_list_promocodes"):
                self.__list_promocodes()
            elif selection == self.loc.get("menu_delete_promocode"):
                self.__delete_promocode()
            else:  # Back or cancel
                return

    def __manage_delivery_methods(self):
        """Manage delivery methods and pickup points."""
        while True:
            keyboard = [
                [self.loc.get("menu_view_delivery_methods")],
                [self.loc.get("menu_add_delivery_method")],
                [self.loc.get("menu_view_pickup_points")],
                [self.loc.get("menu_add_pickup_point")],
                [self.loc.get("menu_back")]
            ]

            self.bot.send_message(
                self.chat.id,
                self.loc.get("manage_delivery_and_pickup"),
                reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )

            selection = self.__wait_for_specific_message(
                [item[0] for item in keyboard],
                cancellable=True
            )

            if isinstance(selection, CancelSignal) or selection == self.loc.get("menu_back"):
                return

            if selection == self.loc.get("menu_view_delivery_methods"):
                self.__view_delivery_methods()
            elif selection == self.loc.get("menu_add_delivery_method"):
                self.__add_delivery_method()
            elif selection == self.loc.get("menu_view_pickup_points"):
                self.__list_pickup_points()
            elif selection == self.loc.get("menu_add_pickup_point"):
                self.__add_pickup_point()

    def __add_delivery_method(self):
        """Add a new delivery method."""
        self.bot.send_message(self.chat.id, self.loc.get("ask_delivery_method_name"))
        name = self.__wait_for_regex(r"(.*)", cancellable=True)
        if isinstance(name, CancelSignal):
            return

        self.bot.send_message(self.chat.id, self.loc.get("ask_delivery_method_price"))
        price = self.__wait_for_regex(r"\d+", cancellable=True)
        if isinstance(price, CancelSignal):
            return

        new_method = db.DeliveryMethod(name=name, price=int(price))
        self.session.add(new_method)
        self.session.commit()
        self.bot.send_message(self.chat.id, self.loc.get("success_delivery_method_added"))

    def __edit_delivery_method(self, method_name):
        """Edit an existing delivery method."""
        method = self.session.query(db.DeliveryMethod).filter_by(name=method_name).first()
        if not method:
            self.bot.send_message(self.chat.id, self.loc.get("error_delivery_method_not_found"))
            return

        keyboard = [
            [self.loc.get("edit_delivery_method_name")],
            [self.loc.get("edit_delivery_method_price")],
            [self.loc.get("toggle_delivery_method_status")],
            [self.loc.get("menu_back")]
        ]

        self.bot.send_message(
            self.chat.id,
            self.loc.get("edit_delivery_method"),
            reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

        selection = self.__wait_for_specific_message([item[0] for item in keyboard], cancellable=True)

        if isinstance(selection, CancelSignal) or selection == self.loc.get("menu_back"):
            return

        if selection == self.loc.get("edit_delivery_method_name"):
            self.bot.send_message(self.chat.id, self.loc.get("ask_new_delivery_method_name"))
            new_name = self.__wait_for_regex(r"(.*)", cancellable=True)
            if not isinstance(new_name, CancelSignal):
                method.name = new_name
        elif selection == self.loc.get("edit_delivery_method_price"):
            self.bot.send_message(self.chat.id, self.loc.get("ask_new_delivery_method_price"))
            new_price = self.__wait_for_regex(r"\d+", cancellable=True)
            if not isinstance(new_price, CancelSignal):
                method.price = int(new_price)
        elif selection == self.loc.get("toggle_delivery_method_status"):
            method.is_active = not method.is_active

        self.session.commit()
        self.bot.send_message(self.chat.id, self.loc.get("success_delivery_method_updated"))

    def __view_delivery_methods(self):
        """View and edit delivery methods."""
        while True:
            methods = self.session.query(db.DeliveryMethod).all()
            keyboard = []
            for method in methods:
                status = "✅" if method.is_active else "❌"
                keyboard.append([f"{status} {method.name} - {self.Price(method.price)}"])
            keyboard.append([self.loc.get("menu_back")])

            self.bot.send_message(
                self.chat.id,
                self.loc.get("view_delivery_methods"),
                reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )

            selection = self.__wait_for_specific_message(
                [item[0] for item in keyboard],
                cancellable=True
            )

            if isinstance(selection, CancelSignal) or selection == self.loc.get("menu_back"):
                return

            method_name = selection[2:].split(" - ")[0]
            self.__edit_delivery_method(method_name)

    def __broadcast_message(self):
        """Broadcast a message to all users."""
        log.debug("Starting broadcast message function")

        # Запитуємо текст повідомлення
        self.bot.send_message(self.chat.id, self.loc.get("ask_broadcast_message"))
        message_text = self.__wait_for_regex(r"(.*)", cancellable=True)
        if isinstance(message_text, CancelSignal):
            self.bot.send_message(self.chat.id, self.loc.get("broadcast_canceled"))
            return

        # Запитуємо, чи потрібно додати зображення
        keyboard = [[
            telegram.InlineKeyboardButton(self.loc.get("yes"), callback_data="yes"),
            telegram.InlineKeyboardButton(self.loc.get("no"), callback_data="no")
        ]]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        self.bot.send_message(
            self.chat.id,
            self.loc.get("ask_broadcast_image"),
            reply_markup=reply_markup
        )

        callback = self.__wait_for_inlinekeyboard_callback()
        add_image = callback.data == "yes"

        image = None
        if add_image:
            self.bot.send_message(self.chat.id, self.loc.get("send_broadcast_image"))
            image = self.__wait_for_photo(cancellable=True)
            if isinstance(image, CancelSignal):
                self.bot.send_message(self.chat.id, self.loc.get("broadcast_canceled"))
                return

        # Запитуємо кількість кнопок
        while True:
            self.bot.send_message(self.chat.id, self.loc.get("ask_number_of_buttons"))
            number_of_buttons = self.__wait_for_regex_update(r"^\d+$", cancellable=True)
            if isinstance(number_of_buttons, CancelSignal):
                self.bot.send_message(self.chat.id, self.loc.get("broadcast_canceled"))
                return
            number_of_buttons = int(number_of_buttons)
            if 0 <= number_of_buttons <= 6:
                break
            else:
                self.bot.send_message(self.chat.id, self.loc.get("invalid_number_of_buttons"))

        buttons = []
        if number_of_buttons > 0:
            for i in range(number_of_buttons):
                # Запитуємо текст кнопки
                self.bot.send_message(self.chat.id, self.loc.get("ask_button_text", button_number=i + 1))
                button_text = self.__wait_for_regex_update(r".*", cancellable=True)
                if isinstance(button_text, CancelSignal):
                    self.bot.send_message(self.chat.id, self.loc.get("broadcast_canceled"))
                    return

                # Запитуємо URL кнопки
                self.bot.send_message(self.chat.id, self.loc.get("ask_button_url", button_number=i + 1))
                button_url = self.__wait_for_regex_update(r"https?://\S+", cancellable=True)
                if isinstance(button_url, CancelSignal):
                    self.bot.send_message(self.chat.id, self.loc.get("broadcast_canceled"))
                    return

                buttons.append(telegram.InlineKeyboardButton(button_text.strip(), url=button_url.strip()))
                log.debug(f"Button added: Text: {button_text.strip()}, URL: {button_url.strip()}")

        keyboard = [buttons[i:i + 2] for i in
                    range(0, len(buttons), 2)] if buttons else None  # Розміщуємо кнопки по 2 в ряд
        reply_markup = telegram.InlineKeyboardMarkup(keyboard) if keyboard else None

        # Підтвердження розсилки
        confirm_message = self.loc.get("confirm_broadcast")
        if image:
            if len(message_text) > 1024:
                self.bot.send_photo(self.chat.id, image[-1].file_id)
                self.bot.send_message(self.chat.id, message_text, reply_markup=reply_markup)
            else:
                self.bot.send_photo(self.chat.id, image[-1].file_id, caption=message_text, reply_markup=reply_markup)
        else:
            self.bot.send_message(self.chat.id, message_text, reply_markup=reply_markup)

        keyboard = [[
            telegram.InlineKeyboardButton(self.loc.get("yes"), callback_data="confirm"),
            telegram.InlineKeyboardButton(self.loc.get("no"), callback_data="cancel")
        ]]
        reply_markup_final = telegram.InlineKeyboardMarkup(keyboard)
        self.bot.send_message(self.chat.id, confirm_message, reply_markup=reply_markup_final)

        callback = self.__wait_for_inlinekeyboard_callback()
        if callback.data == "cancel":
            self.bot.send_message(self.chat.id, self.loc.get("broadcast_canceled"))
            return

        # Виконання розсилки
        users = self.session.query(db.User).all()
        success_count = 0
        failed_count = 0

        log.debug(f"Starting broadcast to {len(users)} users")
        log.debug(f"Message: {message_text}")
        log.debug(f"Image: {'Yes' if image else 'No'}")
        log.debug(f"Reply markup: {reply_markup}")

        for user in users:
            try:
                if image:
                    if len(message_text) > 1024:
                        sent_msg = self.bot.send_photo(user.user_id, image[-1].file_id)
                        log.debug(f"Sent photo to user {user.user_id}")
                        sent_msg = self.bot.send_message(user.user_id, message_text, reply_markup=reply_markup)
                        log.debug(f"Sent message to user {user.user_id}")
                    else:
                        sent_msg = self.bot.send_photo(user.user_id, image[-1].file_id, caption=message_text,
                                                       reply_markup=reply_markup)
                        log.debug(f"Sent photo with caption to user {user.user_id}")
                else:
                    sent_msg = self.bot.send_message(user.user_id, message_text, reply_markup=reply_markup)
                    log.debug(f"Sent message to user {user.user_id}")

                success_count += 1
                log.debug(f"Successfully sent message to user {user.user_id}")
            except Exception as e:
                failed_count += 1
                log.error(f"Failed to send broadcast to user {user.user_id}: {str(e)}")

        log.debug(f"Broadcast completed. Successes: {success_count}, Failures: {failed_count}")

        self.bot.send_message(
            self.chat.id,
            self.loc.get("broadcast_complete", success_count=success_count, total_count=len(users),
                         failed_count=failed_count)
        )

    def __products_menu(self):
        """Display the admin menu to select a product to edit or add a new one."""
        log.debug("Displaying __products_menu")

        while True:
            # Get the products list from the db
            products = self.session.query(db.Product).filter_by(deleted=False).all()

            # Create a list of options
            options = [self.loc.get("menu_cancel"), self.loc.get("menu_add_product")]
            if products:
                options.append(self.loc.get("menu_edit_product"))
                options.append(self.loc.get("menu_delete_product"))

            # Add product names to the options if there are any products
            options.extend([product.name for product in products])

            # Create a keyboard using the options
            keyboard = [[telegram.KeyboardButton(option)] for option in options]

            # Send the keyboard to the user
            self.bot.send_message(
                self.chat.id,
                self.loc.get("conversation_admin_product_menu"),
                reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )

            # Wait for a reply from the user
            selection = self.__wait_for_specific_message(options, cancellable=True)

            if isinstance(selection, CancelSignal):
                return

            if selection == self.loc.get("menu_add_product"):
                self.__add_product()
            elif selection == self.loc.get("menu_edit_product"):
                self.__select_product_to_edit()
            elif selection == self.loc.get("menu_delete_product"):
                self.__delete_product_menu()
            elif selection in [product.name for product in products]:
                product = next(p for p in products if p.name == selection)
                self.__edit_product(product)

    def __add_product(self):
        """Add a new product to the database."""
        log.debug("Adding new product")
        self.__edit_product_menu()

    def __edit_product(self, product):
        """Edit an existing product."""
        log.debug(f"Editing product: {product.name}")
        self.__edit_product_menu(product)

    def __select_product_to_edit(self):
        """Display a menu to select a product to edit."""
        log.debug("Selecting product to edit")
        products = self.session.query(db.Product).filter_by(deleted=False).all()
        options = [self.loc.get("menu_cancel")] + [product.name for product in products]

        keyboard = [[telegram.KeyboardButton(option)] for option in options]

        self.bot.send_message(
            self.chat.id,
            self.loc.get("conversation_admin_select_product_to_edit"),
            reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

        selection = self.__wait_for_specific_message(options, cancellable=True)

        if isinstance(selection, CancelSignal):
            return

        product = next(p for p in products if p.name == selection)
        self.__edit_product(product)

    def __edit_product_menu(self, product: Optional[db.Product] = None):
        """Add a product to the database or edit an existing one."""
        log.debug("Displaying __edit_product_menu")

        is_new_product = product is None
        if is_new_product:
            log.debug("Creating new product")
        else:
            log.debug(f"Editing product: {product.name}")

        # Create an inline keyboard with a single skip button
        cancel = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_skip"),
                                                                               callback_data="cmd_cancel")]])

        # Ask for the product name
        while True:
            self.bot.send_message(self.chat.id, self.loc.get("ask_product_name"))
            if not is_new_product:
                self.bot.send_message(self.chat.id, self.loc.get("edit_current_value", value=escape(product.name)),
                                      reply_markup=cancel)
            name = self.__wait_for_regex(r"(.*)", cancellable=not is_new_product)
            if (not is_new_product and isinstance(name, CancelSignal)) or \
                    self.session.query(db.Product).filter_by(name=name, deleted=False).one_or_none() in [None, product]:
                break
            self.bot.send_message(self.chat.id, self.loc.get("error_duplicate_name"))

        # Ask for the product category
        if is_new_product:
            category = self.__select_category()
            if isinstance(category, CancelSignal):
                return
        else:
            category = product.category

        # Ask for the product description
        self.bot.send_message(self.chat.id, self.loc.get("ask_product_description"))
        if not is_new_product:
            self.bot.send_message(self.chat.id, self.loc.get("edit_current_value", value=escape(product.description)),
                                  reply_markup=cancel)
        description = self.__wait_for_regex(r"(.*)", cancellable=not is_new_product)
        if isinstance(description, CancelSignal):
            description = product.description if not is_new_product else None

        # Ask for the product price
        self.bot.send_message(self.chat.id, self.loc.get("ask_product_price"))
        if not is_new_product:
            self.bot.send_message(self.chat.id,
                                  self.loc.get("edit_current_value",
                                               value=(str(self.Price(product.price))
                                                      if product.price is not None else self.loc.get(
                                                   "not_for_sale_yet"))),
                                  reply_markup=cancel)
        price = self.__wait_for_regex(r"([0-9]+(?:[.,][0-9]{1,2})?|[Xx])", cancellable=not is_new_product)
        if isinstance(price, CancelSignal):
            price = product.price if not is_new_product else None
        elif price.lower() == "x":
            price = None
        else:
            price = self.Price(price)

        # Ask for the product image
        self.bot.send_message(self.chat.id, self.loc.get("ask_product_image"), reply_markup=cancel)
        photo_list = self.__wait_for_photo(cancellable=True)

        if is_new_product:
            # Create the db record for the product
            product = db.Product(name=name,
                                 description=description,
                                 price=int(price) if price is not None else None,
                                 category=category,
                                 deleted=False)
            self.session.add(product)
        else:
            # Edit the record with the new values
            product.name = name if not isinstance(name, CancelSignal) else product.name
            product.description = description if not isinstance(description, CancelSignal) else product.description
            if price is not None and not isinstance(price, CancelSignal):
                product.price = int(price)
            product.category = category

        # If a photo has been sent...
        if isinstance(photo_list, list):
            # Find the largest photo id
            largest_photo = photo_list[0]
            for photo in photo_list[1:]:
                if photo.width > largest_photo.width:
                    largest_photo = photo
            # Get the file object associated with the photo
            photo_file = self.bot.get_file(largest_photo.file_id)
            # Notify the user that the bot is downloading the image and might be inactive for a while
            self.bot.send_message(self.chat.id, self.loc.get("downloading_image"))
            self.bot.send_chat_action(self.chat.id, action="upload_photo")
            # Set the image for that product
            product.set_image(photo_file)

        # Commit the session changes
        self.session.commit()
        # Notify the user
        self.bot.send_message(self.chat.id, self.loc.get("success_product_edited"))

    def __select_category(self):
        """Allow the user to select a category or subcategory."""
        log.debug("Selecting category for product")

        def display_categories(parent_id=None, level=0):
            categories = self.session.query(db.Category).filter_by(parent_id=parent_id, deleted=False).all()
            keyboard = []
            for category in categories:
                indent = "  " * level
                keyboard.append([f"{indent}{category.name}"])
            if parent_id is not None:
                keyboard.append([self.loc.get("menu_back")])
            keyboard.append([self.loc.get("menu_cancel")])
            return keyboard, categories

        stack = []
        current_parent_id = None

        while True:
            keyboard, categories = display_categories(current_parent_id, len(stack))

            self.bot.send_message(
                self.chat.id,
                self.loc.get("select_category_for_product"),
                reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )

            selection = self.__wait_for_specific_message([item[0].strip() for item in keyboard], cancellable=True)

            if isinstance(selection, CancelSignal) or selection == self.loc.get("menu_cancel"):
                return CancelSignal()
            elif selection == self.loc.get("menu_back"):
                if stack:
                    current_parent_id = stack.pop()
                else:
                    current_parent_id = None
                continue

            selected_category = next((cat for cat in categories if cat.name == selection.strip()), None)
            if selected_category:
                # Check if the selected category has subcategories
                subcategories = self.session.query(db.Category).filter_by(parent_id=selected_category.id,
                                                                          deleted=False).all()
                if subcategories:
                    stack.append(current_parent_id)
                    current_parent_id = selected_category.id
                else:
                    return selected_category
            else:
                self.bot.send_message(self.chat.id, self.loc.get("category_not_found"))

    def __delete_product_menu(self):
        log.debug("Displaying __delete_product_menu")
        # Get the products list from the db
        products = self.session.query(db.Product).filter_by(deleted=False).all()
        # Create a list of product names
        product_names = [product.name for product in products]
        # Insert at the start of the list the Cancel button
        product_names.insert(0, self.loc.get("menu_cancel"))
        # Create a keyboard using the product names
        keyboard = [[telegram.KeyboardButton(product_name)] for product_name in product_names]
        # Send the previously created keyboard to the user (ensuring it can be clicked only 1 time)
        self.bot.send_message(self.chat.id, self.loc.get("conversation_admin_select_product_to_delete"),
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        # Wait for a reply from the user
        selection = self.__wait_for_specific_message(product_names, cancellable=True)
        if isinstance(selection, CancelSignal):
            # Exit the menu
            return
        else:
            # Find the selected product
            product = self.session.query(db.Product).filter_by(name=selection, deleted=False).one()
            # "Delete" the product by setting the deleted flag to true
            product.deleted = True
            self.session.commit()
            # Notify the user
            self.bot.send_message(self.chat.id, self.loc.get("success_product_deleted"))

    def __orders_menu(self):
        """Display a live flow of orders."""
        log.debug("Displaying __orders_menu")
        # Create a cancel and a stop keyboard
        stop_keyboard = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_stop"),
                                                                                      callback_data="cmd_cancel")]])
        cancel_keyboard = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_cancel"),
                                                                                        callback_data="cmd_cancel")]])
        # Send a small intro message on the Live Orders mode
        # Remove the keyboard with the first message... (#39)
        self.bot.send_message(self.chat.id,
                              self.loc.get("conversation_live_orders_start"),
                              reply_markup=telegram.ReplyKeyboardRemove())
        # ...and display a small inline keyboard with the following one
        self.bot.send_message(self.chat.id,
                              self.loc.get("conversation_live_orders_stop"),
                              reply_markup=stop_keyboard)
        # Create the order keyboard
        order_keyboard = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_complete"),
                                                                                       callback_data="order_complete")],
                                                        [telegram.InlineKeyboardButton(self.loc.get("menu_refund"),
                                                                                       callback_data="order_refund")]])
        # Display the past pending orders
        orders = self.session.query(db.Order) \
            .filter_by(delivery_date=None, refund_date=None) \
            .join(db.Transaction) \
            .join(db.User) \
            .all()
        # Create a message for every one of them
        for order in orders:
            # Send the created message
            self.bot.send_message(self.chat.id, order.text(w=self),
                                  reply_markup=order_keyboard)
        # Set the Live mode flag to True
        self.admin.live_mode = True
        # Commit the change to the database
        self.session.commit()
        while True:
            # Wait for any message to stop the listening mode
            update = self.__wait_for_inlinekeyboard_callback(cancellable=True)
            # If the user pressed the stop button, exit listening mode
            if isinstance(update, CancelSignal):
                # Stop the listening mode
                self.admin.live_mode = False
                break
            # Find the order
            order_id = re.search(self.loc.get("order_number").replace("{id}", "([0-9]+)"), update.message.text).group(1)
            order = self.session.query(db.Order).get(order_id)
            # Check if the order hasn't been already cleared
            if order.delivery_date is not None or order.refund_date is not None:
                # Notify the admin and skip that order
                self.bot.edit_message_text(self.chat.id, self.loc.get("error_order_already_cleared"))
                break
            # If the user pressed the complete order button, complete the order
            if update.data == "order_complete":
                # Mark the order as complete
                order.delivery_date = datetime.datetime.now()
                # Commit the transaction
                self.session.commit()
                # Update order message
                self.bot.edit_message_text(order.text(w=self), chat_id=self.chat.id,
                                           message_id=update.message.message_id)
                # Notify the user of the completition
                self.bot.send_message(order.user_id,
                                      self.loc.get("notification_order_completed",
                                                   order=order.text(w=self, user=True)))
            # If the user pressed the refund order button, refund the order...
            elif update.data == "order_refund":
                # Ask for a refund reason
                reason_msg = self.bot.send_message(self.chat.id, self.loc.get("ask_refund_reason"),
                                                   reply_markup=cancel_keyboard)
                # Wait for a reply
                reply = self.__wait_for_regex("(.*)", cancellable=True)
                # If the user pressed the cancel button, cancel the refund
                if isinstance(reply, CancelSignal):
                    # Delete the message asking for the refund reason
                    self.bot.delete_message(self.chat.id, reason_msg.message_id)
                    continue
                # Mark the order as refunded
                order.refund_date = datetime.datetime.now()
                # Save the refund reason
                order.refund_reason = reply
                # Refund the credit, reverting the old transaction
                order.transaction.refunded = True
                # Update the user's credit
                order.user.recalculate_credit()
                # Commit the changes
                self.session.commit()
                # Update the order message
                self.bot.edit_message_text(order.text(w=self),
                                           chat_id=self.chat.id,
                                           message_id=update.message.message_id)
                # Notify the user of the refund
                self.bot.send_message(order.user_id,
                                      self.loc.get("notification_order_refunded", order=order.text(w=self,
                                                                                                   user=True)))
                # Notify the admin of the refund
                self.bot.send_message(self.chat.id, self.loc.get("success_order_refunded", order_id=order.order_id))

    def __create_transaction(self):
        """Edit manually the credit of an user."""
        log.debug("Displaying __create_transaction")
        # Make the admin select an user
        user = self.__user_select()
        # Allow the cancellation of the operation
        if isinstance(user, CancelSignal):
            return
        # Create an inline keyboard with a single cancel button
        cancel = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_cancel"),
                                                                               callback_data="cmd_cancel")]])
        # Request from the user the amount of money to be credited manually
        self.bot.send_message(self.chat.id, self.loc.get("ask_credit"), reply_markup=cancel)
        # Wait for an answer
        reply = self.__wait_for_regex(r"(-? ?[0-9]+(?:[.,][0-9]{1,2})?)", cancellable=True)
        # Allow the cancellation of the operation
        if isinstance(reply, CancelSignal):
            return
        # Convert the reply to a price object
        price = self.Price(reply)
        # Ask the user for notes
        self.bot.send_message(self.chat.id, self.loc.get("ask_transaction_notes"), reply_markup=cancel)
        # Wait for an answer
        reply = self.__wait_for_regex(r"(.*)", cancellable=True)
        # Allow the cancellation of the operation
        if isinstance(reply, CancelSignal):
            return
        # Create a new transaction
        transaction = db.Transaction(user=user,
                                     value=int(price),
                                     provider="Manual",
                                     date=datetime.datetime.now(),
                                     notes=reply)
        self.session.add(transaction)
        # Change the user credit
        user.recalculate_credit()
        # Commit the changes
        self.session.commit()
        # Notify the user of the credit/debit
        self.bot.send_message(user.user_id,
                              self.loc.get("notification_transaction_created",
                                           transaction=transaction.text(w=self)))
        # Notify the admin of the success
        self.bot.send_message(self.chat.id, self.loc.get("success_transaction_created",
                                                         transaction=transaction.text(w=self)))

    def __help_menu(self):
        """Help menu. Allows the user to ask for assistance, get a guide or see some info about the bot."""
        log.debug("Displaying __help_menu")
        # Create a keyboard with the user help menu
        keyboard = [[telegram.KeyboardButton(self.loc.get("menu_contact_shopkeeper"))],
                    [telegram.KeyboardButton(self.loc.get("menu_cancel"))]]
        # Send the previously created keyboard to the user (ensuring it can be clicked only 1 time)
        self.bot.send_message(self.chat.id,
                              self.loc.get("conversation_open_help_menu"),
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        # Wait for a reply from the user
        selection = self.__wait_for_specific_message([
            self.loc.get("menu_guide"),
            self.loc.get("menu_contact_shopkeeper")
        ], cancellable=True)
        # If the user has selected the Guide option...
        if selection == self.loc.get("menu_guide"):
            # Send them the bot guide
            self.bot.send_message(self.chat.id, self.loc.get("help_msg"))
        # If the user has selected the Order Status option...
        elif selection == self.loc.get("menu_contact_shopkeeper"):
            # Find the list of available shopkeepers
            shopkeepers = self.session.query(db.Admin).filter_by(display_on_help=True).join(db.User).all()
            # Create the string
            shopkeepers_string = "\n".join([admin.user.mention() for admin in shopkeepers])
            # Send the message to the user
            self.bot.send_message(self.chat.id, self.loc.get("contact_shopkeeper", shopkeepers=shopkeepers_string))
        # If the user has selected the Cancel option the function will return immediately

    def __transaction_pages(self):
        """Display the latest transactions, in pages."""
        log.debug("Displaying __transaction_pages")
        # Page number
        page = 0
        # Create and send a placeholder message to be populated
        message = self.bot.send_message(self.chat.id, self.loc.get("loading_transactions"))
        # Loop used to move between pages
        while True:
            # Retrieve the 10 transactions in that page
            transactions = self.session.query(db.Transaction) \
                .order_by(db.Transaction.transaction_id.desc()) \
                .limit(10) \
                .offset(10 * page) \
                .all()
            # Create a list to be converted in inline keyboard markup
            inline_keyboard_list = [[]]
            # Don't add a previous page button if this is the first page
            if page != 0:
                # Add a previous page button
                inline_keyboard_list[0].append(
                    telegram.InlineKeyboardButton(self.loc.get("menu_previous"), callback_data="cmd_previous")
                )
            # Don't add a next page button if this is the last page
            if len(transactions) == 10:
                # Add a next page button
                inline_keyboard_list[0].append(
                    telegram.InlineKeyboardButton(self.loc.get("menu_next"), callback_data="cmd_next")
                )
            # Add a Done button
            inline_keyboard_list.append(
                [telegram.InlineKeyboardButton(self.loc.get("menu_done"), callback_data="cmd_done")])
            # Create the inline keyboard markup
            inline_keyboard = telegram.InlineKeyboardMarkup(inline_keyboard_list)
            # Create the message text
            transactions_string = "\n".join([transaction.text(w=self) for transaction in transactions])
            text = self.loc.get("transactions_page", page=page + 1, transactions=transactions_string)
            # Update the previously sent message
            self.bot.edit_message_text(chat_id=self.chat.id, message_id=message.message_id, text=text,
                                       reply_markup=inline_keyboard)
            # Wait for user input
            selection = self.__wait_for_inlinekeyboard_callback()
            # If Previous was selected...
            if selection.data == "cmd_previous" and page != 0:
                # Go back one page
                page -= 1
            # If Next was selected...
            elif selection.data == "cmd_next" and len(transactions) == 10:
                # Go to the next page
                page += 1
            # If Done was selected...
            elif selection.data == "cmd_done":
                # Break the loop
                break

    def __transactions_file(self):
        """Generate a .csv file containing the list of all transactions."""
        log.debug("Generating __transaction_file")
        # Retrieve all the transactions
        transactions = self.session.query(db.Transaction).order_by(db.Transaction.transaction_id).all()
        # Write on the previously created file
        with open(f"transactions_{self.chat.id}.csv", "w") as file:
            # Write an header line
            file.write(f"UserID;"
                       f"TransactionValue;"
                       f"TransactionNotes;"
                       f"Provider;"
                       f"ChargeID;"
                       f"SpecifiedName;"
                       f"SpecifiedPhone;"
                       f"SpecifiedEmail;"
                       f"Refunded?\n")
            # For each transaction; write a new line on file
            for transaction in transactions:
                file.write(f"{transaction.user_id if transaction.user_id is not None else ''};"
                           f"{transaction.value if transaction.value is not None else ''};"
                           f"{transaction.notes if transaction.notes is not None else ''};"
                           f"{transaction.provider if transaction.provider is not None else ''};"
                           f"{transaction.provider_charge_id if transaction.provider_charge_id is not None else ''};"
                           f"{transaction.payment_name if transaction.payment_name is not None else ''};"
                           f"{transaction.payment_phone if transaction.payment_phone is not None else ''};"
                           f"{transaction.payment_email if transaction.payment_email is not None else ''};"
                           f"{transaction.refunded if transaction.refunded is not None else ''}\n")
        # Describe the file to the user
        self.bot.send_message(self.chat.id, self.loc.get("csv_caption"))
        # Reopen the file for reading
        with open(f"transactions_{self.chat.id}.csv") as file:
            # Send the file via a manual request to Telegram
            requests.post(f"https://api.telegram.org/bot{self.cfg['Telegram']['token']}/sendDocument",
                          files={"document": file},
                          params={"chat_id": self.chat.id,
                                  "parse_mode": "HTML"})
        # Delete the created file
        os.remove(f"transactions_{self.chat.id}.csv")

    def __add_admin(self):
        """Add an administrator to the bot or edit an existing one."""
        log.debug("Displaying __add_admin")
        # Let the admin select an administrator to promote
        user = self.__user_select()
        # Allow the cancellation of the operation
        if isinstance(user, CancelSignal):
            return
        # Check if the user is already an administrator
        admin = self.session.query(db.Admin).filter_by(user=user).one_or_none()
        if admin is None:
            # Create the keyboard to be sent
            keyboard = telegram.ReplyKeyboardMarkup([[self.loc.get("emoji_yes"), self.loc.get("emoji_no")]],
                                                    one_time_keyboard=True)
            # Ask for confirmation
            self.bot.send_message(self.chat.id, self.loc.get("conversation_confirm_admin_promotion"),
                                  reply_markup=keyboard)
            # Wait for an answer
            selection = self.__wait_for_specific_message([self.loc.get("emoji_yes"), self.loc.get("emoji_no")])
            # Proceed only if the answer is yes
            if selection == self.loc.get("emoji_no"):
                return
            # Create a new admin
            admin = db.Admin(user=user,
                             edit_products=False,
                             edit_categories=False,
                             edit_subcategories=False,
                             receive_orders=False,
                             create_transactions=False,
                             display_on_help=False,
                             is_owner=False)
            self.session.add(admin)
        # Send the empty admin message and record the id
        message = self.bot.send_message(self.chat.id, self.loc.get("admin_properties", name=str(admin.user)))
        # Start accepting edits
        while True:
            # Create the inline keyboard with the admin status
            inline_keyboard = telegram.InlineKeyboardMarkup([
                [telegram.InlineKeyboardButton(
                    f"{self.loc.boolmoji(admin.edit_products)} {self.loc.get('prop_edit_products')}",
                    callback_data="toggle_edit_products"
                )],
                [telegram.InlineKeyboardButton(
                    f"{self.loc.boolmoji(admin.edit_categories)} {self.loc.get('prop_edit_categories')}",
                    callback_data="toggle_edit_categories"
                )],
                [telegram.InlineKeyboardButton(
                    f"{self.loc.boolmoji(admin.edit_subcategories)} {self.loc.get('prop_edit_subcategories')}",
                    callback_data="toggle_edit_subcategories"
                )],
                [telegram.InlineKeyboardButton(
                    f"{self.loc.boolmoji(admin.receive_orders)} {self.loc.get('prop_receive_orders')}",
                    callback_data="toggle_receive_orders"
                )],
                [telegram.InlineKeyboardButton(
                    f"{self.loc.boolmoji(admin.create_transactions)} {self.loc.get('prop_create_transactions')}",
                    callback_data="toggle_create_transactions"
                )],
                [telegram.InlineKeyboardButton(
                    f"{self.loc.boolmoji(admin.display_on_help)} {self.loc.get('prop_display_on_help')}",
                    callback_data="toggle_display_on_help"
                )],
                [telegram.InlineKeyboardButton(
                    self.loc.get('menu_done'),
                    callback_data="cmd_done"
                )]
            ])
            # Update the inline keyboard
            self.bot.edit_message_reply_markup(message_id=message.message_id,
                                               chat_id=self.chat.id,
                                               reply_markup=inline_keyboard)
            # Wait for an user answer
            callback = self.__wait_for_inlinekeyboard_callback()
            # Toggle the correct property
            if callback.data == "toggle_edit_products":
                admin.edit_products = not admin.edit_products
            elif callback.data == "toggle_edit_categories":
                admin.edit_categories = not admin.edit_categories
            elif callback.data == "toggle_edit_subcategories":
                admin.edit_subcategories = not admin.edit_subcategories
            elif callback.data == "toggle_receive_orders":
                admin.receive_orders = not admin.receive_orders
            elif callback.data == "toggle_create_transactions":
                admin.create_transactions = not admin.create_transactions
            elif callback.data == "toggle_display_on_help":
                admin.display_on_help = not admin.display_on_help
            elif callback.data == "cmd_done":
                break
        self.session.commit()

    def __add_category(self):
        """Add a new root category."""
        log.debug("Adding new root category")
        try:
            # Ask for the category name
            self.bot.send_message(self.chat.id, self.loc.get("ask_category_name"))
            name = self.__wait_for_regex(r"(.*)", cancellable=True)

            if isinstance(name, CancelSignal):
                log.debug("User cancelled adding category")
                return

            # Check if category with this name already exists
            existing_category = self.session.query(db.Category).filter_by(name=name, deleted=False).one_or_none()
            if existing_category:
                log.debug(f"Category with name {name} already exists")
                self.bot.send_message(self.chat.id, self.loc.get("error_duplicate_name"))
                return

            # Ask for the category description
            skip_button = telegram.InlineKeyboardMarkup([[
                telegram.InlineKeyboardButton(self.loc.get("menu_skip"), callback_data="skip_description")
            ]])
            self.bot.send_message(self.chat.id, self.loc.get("ask_category_description"), reply_markup=skip_button)
            description = self.__wait_for_regex_or_callback(r"(.*)", cancellable=True)

            if isinstance(description, CancelSignal):
                description = None
            elif isinstance(description, telegram.CallbackQuery) and description.data == "skip_description":
                description = None

            # Ask for the category image
            skip_button = telegram.InlineKeyboardMarkup([[
                telegram.InlineKeyboardButton(self.loc.get("menu_skip"), callback_data="skip_image")
            ]])
            self.bot.send_message(self.chat.id, self.loc.get("ask_category_image"), reply_markup=skip_button)
            photo_list = self.__wait_for_photo_or_callback(cancellable=True)

            # Create new category
            new_category = db.Category(name=name, description=description, parent_id=None, deleted=False)
            self.session.add(new_category)

            # If a photo has been sent, add it to the category
            if isinstance(photo_list, list):
                largest_photo = max(photo_list, key=lambda p: p.width * p.height)
                photo_file = self.bot.get_file(largest_photo.file_id)
                new_category.set_image(photo_file)

            self.session.commit()

            log.debug(f"Created new root category: {new_category}")
            self.bot.send_message(self.chat.id, self.loc.get("success_category_created"))
        except Exception as e:
            log.error(f"Error in __add_category: {e}")
            self.bot.send_message(self.chat.id, f"An error occurred: {e}")

    def __add_subcategory(self):
        """Add a new subcategory."""
        log.debug("Adding new subcategory")
        try:
            # Get all root categories
            root_categories = self.session.query(db.Category).filter_by(parent_id=None, deleted=False).all()

            if not root_categories:
                log.debug("No root categories found")
                self.bot.send_message(self.chat.id, self.loc.get("error_no_root_categories"))
                return

            # Create keyboard with root categories
            keyboard = [[telegram.KeyboardButton(cat.name)] for cat in root_categories]
            keyboard.append([telegram.KeyboardButton(self.loc.get("menu_cancel"))])

            # Ask user to select parent category
            self.bot.send_message(
                self.chat.id,
                self.loc.get("ask_parent_category"),
                reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )

            parent_name = self.__wait_for_specific_message(
                [cat.name for cat in root_categories] + [self.loc.get("menu_cancel")], cancellable=True)

            if isinstance(parent_name, CancelSignal) or parent_name == self.loc.get("menu_cancel"):
                log.debug("User cancelled adding subcategory")
                return

            parent_category = next((cat for cat in root_categories if cat.name == parent_name), None)

            # Ask for the subcategory name
            self.bot.send_message(self.chat.id, self.loc.get("ask_subcategory_name"))
            name = self.__wait_for_regex(r"(.*)", cancellable=True)

            if isinstance(name, CancelSignal):
                log.debug("User cancelled adding subcategory")
                return

            # Check if subcategory with this name already exists under the parent
            existing_subcategory = self.session.query(db.Category).filter_by(name=name, parent_id=parent_category.id,
                                                                             deleted=False).one_or_none()
            if existing_subcategory:
                log.debug(f"Subcategory with name {name} already exists under parent {parent_name}")
                self.bot.send_message(self.chat.id, self.loc.get("error_duplicate_name"))
                return

            # Ask for the subcategory description
            skip_button = telegram.InlineKeyboardMarkup([[
                telegram.InlineKeyboardButton(self.loc.get("menu_skip"), callback_data="skip_description")
            ]])
            self.bot.send_message(self.chat.id, self.loc.get("ask_subcategory_description"), reply_markup=skip_button)
            description = self.__wait_for_regex_or_callback(r"(.*)", cancellable=True)

            if isinstance(description, CancelSignal):
                description = None
            elif isinstance(description, telegram.CallbackQuery) and description.data == "skip_description":
                description = None

            # Ask for the subcategory image
            skip_button = telegram.InlineKeyboardMarkup([[
                telegram.InlineKeyboardButton(self.loc.get("menu_skip"), callback_data="skip_image")
            ]])
            self.bot.send_message(self.chat.id, self.loc.get("ask_subcategory_image"), reply_markup=skip_button)
            photo_list = self.__wait_for_photo_or_callback(cancellable=True)

            # Create new subcategory
            new_subcategory = db.Category(name=name, description=description, parent_id=parent_category.id,
                                          deleted=False)
            self.session.add(new_subcategory)

            # If a photo has been sent, add it to the subcategory
            if isinstance(photo_list, list):
                largest_photo = max(photo_list, key=lambda p: p.width * p.height)
                photo_file = self.bot.get_file(largest_photo.file_id)
                new_subcategory.set_image(photo_file)

            self.session.commit()

            log.debug(f"Created new subcategory: {new_subcategory} under parent {parent_category}")
            self.bot.send_message(self.chat.id, self.loc.get("success_subcategory_created"))
        except Exception as e:
            log.error(f"Error in __add_subcategory: {e}")
            self.bot.send_message(self.chat.id, f"An error occurred: {e}")

    def __categories_menu(self):
        """Display the admin menu to manage categories and subcategories."""
        log.debug("Displaying __categories_menu")

        def display_categories(parent_id=None, level=0):
            categories = self.session.query(db.Category).filter_by(parent_id=parent_id, deleted=False).all()
            keyboard = []
            for category in categories:
                indent = "  " * level
                keyboard.append([f"{indent}{category.name}"])
            keyboard.append([self.loc.get("menu_add_category"), self.loc.get("menu_add_subcategory")])
            if parent_id is not None:
                keyboard.append([self.loc.get("menu_back")])
            keyboard.append([self.loc.get("menu_cancel")])
            return keyboard, categories

        stack = []
        current_category = None

        while True:
            keyboard, categories = display_categories(current_category.id if current_category else None, len(stack))

            self.bot.send_message(
                self.chat.id,
                self.loc.get("conversation_admin_select_category"),
                reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )

            selection = self.__wait_for_specific_message([item for sublist in keyboard for item in sublist],
                                                         cancellable=True)

            if isinstance(selection, CancelSignal) or selection == self.loc.get("menu_cancel"):
                return
            elif selection == self.loc.get("menu_back"):
                if stack:
                    current_category = stack.pop()
                else:
                    current_category = None
                continue
            elif selection == self.loc.get("menu_add_category"):
                self.__add_category()
            elif selection == self.loc.get("menu_add_subcategory"):
                self.__add_subcategory()
            else:
                selected_category = next((cat for cat in categories if cat.name == selection.strip()), None)
                if selected_category:
                    action_keyboard = [
                        [self.loc.get("menu_edit_category")],
                        [self.loc.get("menu_delete_category")],
                        [self.loc.get("menu_view_subcategories")],
                        [self.loc.get("menu_back")]
                    ]
                    self.bot.send_message(
                        self.chat.id,
                        self.loc.get("category_action_prompt"),
                        reply_markup=telegram.ReplyKeyboardMarkup(action_keyboard, one_time_keyboard=True)
                    )

                    action = self.__wait_for_specific_message([item[0] for item in action_keyboard], cancellable=True)

                    if action == self.loc.get("menu_edit_category"):
                        self.__edit_category_menu(selected_category)
                    elif action == self.loc.get("menu_delete_category"):
                        if self.__delete_category():
                            if current_category:
                                current_category = stack.pop() if stack else None
                            continue
                    elif action == self.loc.get("menu_view_subcategories"):
                        stack.append(current_category)
                        current_category = selected_category
                    elif action == self.loc.get("menu_back") or isinstance(action, CancelSignal):
                        continue
                else:
                    self.bot.send_message(self.chat.id, self.loc.get("category_not_found"))

    def __edit_category_menu(self, category: Optional[db.Category] = None):
        """Add a category to the database or edit an existing one."""
        log.debug(f"Entering __edit_category_menu for category: {category}")
        # Create an inline keyboard with a single skip button
        cancel = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(self.loc.get("menu_skip"),
                                                                               callback_data="cmd_cancel")]])

        log.debug("Asking for category name")
        # Ask for the category name
        while True:
            self.bot.send_message(self.chat.id, self.loc.get("ask_category_name"))
            if category:
                self.bot.send_message(self.chat.id, self.loc.get("edit_current_value", value=escape(category.name)),
                                      reply_markup=cancel)
            name = self.__wait_for_regex(r"(.*)", cancellable=bool(category))
            log.debug(f"Received category name: {name}")
            if (category and isinstance(name, CancelSignal)) or \
                    self.session.query(db.Category).filter_by(name=name, deleted=False).one_or_none() in [None,
                                                                                                          category]:
                break
            self.bot.send_message(self.chat.id, self.loc.get("error_duplicate_name"))

        log.debug("Asking for parent category")
        # Ask for the parent category
        parent_categories = self.session.query(db.Category).filter_by(deleted=False).all()
        parent_names = ["None"] + [cat.name for cat in parent_categories if cat != category]
        self.bot.send_message(self.chat.id, self.loc.get("ask_category_parent"))
        if category and category.parent:
            self.bot.send_message(self.chat.id, self.loc.get("edit_current_value", value=escape(category.parent.name)),
                                  reply_markup=cancel)
        parent_name = self.__wait_for_specific_message(parent_names, cancellable=bool(category))
        log.debug(f"Received parent category: {parent_name}")

        try:
            log.debug("Saving category to database")
            if not category:
                category = db.Category(name=name,
                                       parent=None if parent_name == "None" else next(
                                           cat for cat in parent_categories if cat.name == parent_name),
                                       deleted=False)
                self.session.add(category)
                log.debug(f"Created new category: {category}")
            else:
                category.name = name if not isinstance(name, CancelSignal) else category.name
                if not isinstance(parent_name, CancelSignal):
                    category.parent = None if parent_name == "None" else next(
                        cat for cat in parent_categories if cat.name == parent_name)
                log.debug(f"Updated category: {category}")

            self.session.commit()
            log.debug("Category changes committed to database")
            self.bot.send_message(self.chat.id, self.loc.get("success_category_edited"))
        except Exception as e:
            log.error(f"Error while saving category: {e}")
            self.bot.send_message(self.chat.id, f"An error occurred: {e}")

        log.debug("Exiting __edit_category_menu")

    def __delete_category(self):
        """Delete a category."""
        log.debug("Deleting category")
        categories = self.session.query(db.Category).filter_by(parent_id=None, deleted=False).all()

        if not categories:
            self.bot.send_message(self.chat.id, self.loc.get("no_categories_to_delete"))
            return False

        keyboard = [[category.name] for category in categories]
        keyboard.append([self.loc.get("menu_cancel")])

        self.bot.send_message(
            self.chat.id,
            self.loc.get("select_category_to_delete"),
            reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

        selection = self.__wait_for_specific_message([cat.name for cat in categories] + [self.loc.get("menu_cancel")])

        if selection == self.loc.get("menu_cancel"):
            self.bot.send_message(self.chat.id, self.loc.get("deletion_canceled"))
            return False

        category = next((cat for cat in categories if cat.name == selection), None)
        if category:
            # Запитуємо підтвердження
            confirm_keyboard = [
                [self.loc.get("menu_confirm")],
                [self.loc.get("menu_cancel")]
            ]
            self.bot.send_message(
                self.chat.id,
                self.loc.get("confirm_delete_category", category=category.name),
                reply_markup=telegram.ReplyKeyboardMarkup(confirm_keyboard, one_time_keyboard=True)
            )

            confirm = self.__wait_for_specific_message([self.loc.get("menu_confirm"), self.loc.get("menu_cancel")])

            if confirm == self.loc.get("menu_confirm"):
                category.deleted = True
                # Move all products in this category to "No category"
                for product in category.products:
                    product.category_id = None
                self.session.commit()
                self.bot.send_message(self.chat.id, self.loc.get("category_deleted"))
                return True
            else:
                self.bot.send_message(self.chat.id, self.loc.get("deletion_canceled"))
                return False
        else:
            self.bot.send_message(self.chat.id, self.loc.get("category_not_found"))
            return False

    def __delete_subcategory(self):
        """Delete a subcategory."""
        log.debug("Deleting subcategory")
        while True:
            categories = self.session.query(db.Category).filter(db.Category.parent_id != None,
                                                                db.Category.deleted == False).all()

            if not categories:
                self.bot.send_message(self.chat.id, self.loc.get("no_subcategories_to_delete"))
                return

            keyboard = [[category.name] for category in categories]
            keyboard.append([self.loc.get("menu_cancel")])

            self.bot.send_message(
                self.chat.id,
                self.loc.get("select_subcategory_to_delete"),
                reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )

            selection = self.__wait_for_specific_message(
                [cat.name for cat in categories] + [self.loc.get("menu_cancel")])

            if selection == self.loc.get("menu_cancel"):
                self.bot.send_message(self.chat.id, self.loc.get("deletion_canceled"))
                return

            category = next((cat for cat in categories if cat.name == selection), None)
            if category:
                # Запитуємо підтвердження
                confirm_keyboard = [
                    [self.loc.get("menu_confirm")],
                    [self.loc.get("menu_cancel")]
                ]
                self.bot.send_message(
                    self.chat.id,
                    self.loc.get("confirm_delete_subcategory", subcategory=category.name),
                    reply_markup=telegram.ReplyKeyboardMarkup(confirm_keyboard, one_time_keyboard=True)
                )

                confirm = self.__wait_for_specific_message([self.loc.get("menu_confirm"), self.loc.get("menu_cancel")])

                if confirm == self.loc.get("menu_confirm"):
                    category.deleted = True
                    # Move all products in this subcategory to parent category
                    for product in category.products:
                        product.category_id = category.parent_id
                    self.session.commit()
                    self.bot.send_message(self.chat.id, self.loc.get("subcategory_deleted"))
                    return
                else:
                    self.bot.send_message(self.chat.id, self.loc.get("deletion_canceled"))
                    return
            else:
                self.bot.send_message(self.chat.id, self.loc.get("subcategory_not_found"))

    def __add_pickup_point(self):
        """Add a new pickup point."""
        log.debug("Adding new pickup point")
        self.bot.send_message(self.chat.id, self.loc.get("ask_pickup_point_address"))
        address = self.__wait_for_regex(r"(.*)", cancellable=True)

        if isinstance(address, CancelSignal):
            return

        self.bot.send_message(self.chat.id, self.loc.get("ask_pickup_point_description"))
        description = self.__wait_for_regex(r"(.*)", cancellable=True)

        if isinstance(description, CancelSignal):
            description = None

        pickup_point = db.PickupPoint(address=address, description=description)
        self.session.add(pickup_point)
        self.session.commit()

        self.bot.send_message(self.chat.id, self.loc.get("success_pickup_point_added"))

    def __list_pickup_points(self):
        """List all active pickup points."""
        log.debug("Listing pickup points")
        pickup_points = self.session.query(db.PickupPoint).filter_by(is_active=True).all()
        if not pickup_points:
            self.bot.send_message(self.chat.id, self.loc.get("no_pickup_points"))
            return

        keyboard = []
        for point in pickup_points:
            keyboard.append([f"{point.id}. {point.address}"])
        keyboard.append([self.loc.get("menu_back")])

        self.bot.send_message(
            self.chat.id,
            self.loc.get("pickup_points_list"),
            reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

        selection = self.__wait_for_specific_message(
            [item[0] for item in keyboard],
            cancellable=True
        )

        if isinstance(selection, CancelSignal) or selection == self.loc.get("menu_back"):
            return

        point_id = int(selection.split('.')[0])
        self.__edit_pickup_point(point_id)

    def __edit_pickup_point(self, point_id):
        """Edit an existing pickup point."""
        point = self.session.query(db.PickupPoint).get(point_id)
        if not point:
            self.bot.send_message(self.chat.id, self.loc.get("error_pickup_point_not_found"))
            return

        keyboard = [
            [self.loc.get("edit_pickup_point_address")],
            [self.loc.get("edit_pickup_point_description")],
            [self.loc.get("toggle_pickup_point_status")],
            [self.loc.get("menu_back")]
        ]

        self.bot.send_message(
            self.chat.id,
            self.loc.get("edit_pickup_point"),
            reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

        selection = self.__wait_for_specific_message([item[0] for item in keyboard], cancellable=True)

        if isinstance(selection, CancelSignal) or selection == self.loc.get("menu_back"):
            return

        if selection == self.loc.get("edit_pickup_point_address"):
            self.bot.send_message(self.chat.id, self.loc.get("ask_new_pickup_point_address"))
            new_address = self.__wait_for_regex(r"(.*)", cancellable=True)
            if not isinstance(new_address, CancelSignal):
                point.address = new_address
        elif selection == self.loc.get("edit_pickup_point_description"):
            self.bot.send_message(self.chat.id, self.loc.get("ask_new_pickup_point_description"))
            new_description = self.__wait_for_regex(r"(.*)", cancellable=True)
            if not isinstance(new_description, CancelSignal):
                point.description = new_description
        elif selection == self.loc.get("toggle_pickup_point_status"):
            point.is_active = not point.is_active

        self.session.commit()
        self.bot.send_message(self.chat.id, self.loc.get("success_pickup_point_updated"))

    def __language_menu(self):
        """Select a language."""
        log.debug("Displaying __language_menu")
        keyboard = []
        options: Dict[str, str] = {}
        # https://en.wikipedia.org/wiki/List_of_language_names
        if "it" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇮🇹 Italiano"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "it"
        if "pl" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇵🇱 Polish"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "pl"
        if "en" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇬🇧 English"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "en"
        if "ru" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇷🇺 Русский"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "ru"
        if "uk" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇺🇦 Українська"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "uk"
        if "zh_cn" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇨🇳 简体中文"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "zh_cn"
        if "he" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇮🇱 עברית"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "he"
        if "es_mx" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇲🇽 Español"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "es_mx"
        if "pt_br" in self.cfg["Language"]["enabled_languages"]:
            lang = "🇧🇷 Português"
            keyboard.append([telegram.KeyboardButton(lang)])
            options[lang] = "pt_br"

        # Додаємо кнопку "Скасувати" використовуючи локалізацію
        cancel_button = self.loc.get("menu_cancel")
        keyboard.append([telegram.KeyboardButton(cancel_button)])
        options[cancel_button] = "cancel"

        # Відправляємо створену клавіатуру користувачу
        self.bot.send_message(self.chat.id,
                              self.loc.get("conversation_language_select"),
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

        # Очікуємо на відповідь
        response = self.__wait_for_specific_message(list(options.keys()), cancellable=True)

        # Обробка відповіді
        if isinstance(response, CancelSignal):
            # Повертаємо користувача до головного меню
            return

        # Встановлюємо мову відповідно до вибору користувача
        self.user.language = options[response]
        # Зберігаємо зміни у базі даних
        self.session.commit()
        # Перезавантажуємо об'єкт локалізації
        self.__create_localization()

    def __create_localization(self):
        # Check if the user's language is enabled; if it isn't, change it to the default
        if self.user.language not in self.cfg["Language"]["enabled_languages"]:
            log.debug(f"User's language '{self.user.language}' is not enabled, changing it to the default")
            self.user.language = self.cfg["Language"]["default_language"]
            self.session.commit()
        # Create a new Localization object
        self.loc = localization.Localization(
            language=self.user.language,
            fallback=self.cfg["Language"]["fallback_language"],
            replacements={
                "user_string": str(self.user),
                "user_mention": self.user.mention(),
                "user_full_name": self.user.full_name,
                "user_first_name": self.user.first_name,
                "today": datetime.datetime.now().strftime("%a %d %b %Y"),
            }
        )

    def __graceful_stop(self, stop_trigger: StopSignal):
        """Handle the graceful stop of the thread."""
        log.debug("Gracefully stopping the conversation")
        # If the session has expired...
        if stop_trigger.reason == "timeout":
            # Notify the user that the session has expired and remove the keyboard
            self.bot.send_message(self.chat.id, self.loc.get('conversation_expired'),
                                  reply_markup=telegram.ReplyKeyboardRemove())
        # If a restart has been requested...
        # Do nothing.
        # Close the database session
        self.session.close()
        # End the process
        sys.exit(0)
