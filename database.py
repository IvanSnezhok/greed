import datetime
import logging
import typing
import requests
import telegram
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, BigInteger, String, Text, LargeBinary, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import relationship, backref
import utils

if typing.TYPE_CHECKING:
    import worker

log = logging.getLogger(__name__)

# Create a base class to define all the database subclasses
TableDeclarativeBase = declarative_base()


# Define all the database tables using the sqlalchemy declarative base
class User(TableDeclarativeBase):
    """A Telegram user who used the bot at least once."""

    # Telegram data
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    language = Column(String, nullable=False)

    # Current wallet credit
    credit = Column(Integer, nullable=False)

    promocode_usages = relationship("PromocodeUsage", back_populates="user")

    connect_date = Column(DateTime, nullable=False)

    # Extra table parameters
    __tablename__ = "users"

    def __init__(self, w: "worker.Worker", **kwargs):
        # Initialize the super
        super().__init__(**kwargs)
        # Get the data from telegram
        self.user_id = w.telegram_user.id
        self.first_name = w.telegram_user.first_name
        self.last_name = w.telegram_user.last_name
        self.username = w.telegram_user.username
        if w.telegram_user.language_code:
            self.language = w.telegram_user.language_code
        else:
            self.language = w.cfg["Language"]["default_language"]
        # The starting wallet value is 0
        self.credit = 0
        self.connect_date = datetime.datetime.now()

    def __str__(self):
        """Describe the user in the best way possible given the available data."""
        if self.username is not None:
            return f"@{self.username}"
        elif self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name

    def identifiable_str(self):
        """Describe the user in the best way possible, ensuring a way back to the database record exists."""
        return f"user_{self.user_id} ({str(self)})"

    def mention(self):
        """Mention the user in the best way possible given the available data."""
        if self.username is not None:
            return f"@{self.username}"
        else:
            return f"[{self.first_name}](tg://user?id={self.user_id})"

    def recalculate_credit(self):
        """Recalculate the credit for this user by calculating the sum of the values of all their transactions."""
        valid_transactions: typing.List[Transaction] = [t for t in self.transactions if not t.refunded]
        self.credit = sum(map(lambda t: t.value, valid_transactions))

    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name

    def __repr__(self):
        return f"<User {self.mention()} having {self.credit} credit>"


class Category(DeferredReflection, TableDeclarativeBase):
    """A category for products."""

    # Category id
    id = Column(Integer, primary_key=True)
    # Category name
    name = Column(String, nullable=False)
    # Category description
    description = Column(Text, nullable=True)
    # Category image
    image = Column(LargeBinary, nullable=True)
    # Category has been deleted
    deleted = Column(Boolean, nullable=False, default=False)
    # Parent category id (for subcategories)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category")

    # Extra table parameters
    __tablename__ = "categories"

    def __repr__(self):
        return f"<Category {self.name}>"

    def set_image(self, file: telegram.File):
        """Download an image from Telegram and store it in the image column."""
        r = requests.get(file.file_path)
        self.image = r.content

    def send_as_message(self, w: "worker.Worker", chat_id: int) -> dict:
        """Send a message containing the category data."""
        if self.image is None:
            msg = w.bot.send_message(chat_id, self.text(w))
        else:
            msg = w.bot.send_photo(chat_id, self.image, caption=self.text(w))
        return msg.to_dict()

    def text(self, w: "worker.Worker"):
        """Return the category details formatted with Telegram HTML."""
        return w.loc.get("category_format_string",
                         name=utils.telegram_html_escape(self.name),
                         description=utils.telegram_html_escape(self.description or ""))


class Product(TableDeclarativeBase):
    """A purchasable product."""

    # Product id
    id = Column(Integer, primary_key=True)
    # Product name
    name = Column(String, nullable=False)
    # Product description
    description = Column(Text)
    # Product price, if null product is not for sale
    price = Column(Integer)
    # Category id
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    # Image data
    image = Column(LargeBinary)
    # Product has been deleted
    deleted = Column(Boolean, nullable=False, default=False)

    # Relationships
    category = relationship("Category", back_populates="products")

    # Extra table parameters
    __tablename__ = "products"


    # No __init__ is needed, the default one is sufficient

    def text(self, w: "worker.Worker", *, style: str = "full", cart_qty: int = None):
        if style == "short":
            return f"{cart_qty}x {utils.telegram_html_escape(self.name)} - {str(w.Price(self.price) * cart_qty)}"
        elif style == "full":
            cart_info = ""
            if cart_qty is not None and cart_qty > 0:
                cart_info = w.loc.get("in_cart_format_string", quantity=cart_qty)
            return w.loc.get("product_format_string",
                             name=utils.telegram_html_escape(self.name),
                             description=utils.telegram_html_escape(self.description),
                             price=str(w.Price(self.price)),
                             cart=cart_info)
        else:
            raise ValueError("style is not an accepted value")

    def __repr__(self):
        return f"<Product {self.name}>"

    def send_as_message(self, w: "worker.Worker", chat_id: int) -> dict:
        """Send a message containing the product data."""
        if self.image is None:
            msg = w.bot.send_message(chat_id, self.text(w))
        else:
            msg = w.bot.send_photo(chat_id, self.image, caption=self.text(w))
        return msg.to_dict()

    def set_image(self, file: telegram.File):
        """Download an image from Telegram and store it in the image column.
        This is a slow blocking function. Try to avoid calling it directly, use a thread if possible."""
        # Download the photo through a get request
        r = requests.get(file.file_path)
        # Store the photo in the database record
        self.image = r.content


class DeliveryMethod(TableDeclarativeBase):
    __tablename__ = 'delivery_methods'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)  # Ціна в мінімальних одиницях валюти
    is_active = Column(Boolean, default=True)

    @classmethod
    def initialize_default_methods(cls, session):
        default_methods = [
            {"name": "Самовивіз", "price": 0},
            {"name": "Нова пошта", "price": 0},
            {"name": "По Києву", "price": 0},
        ]

        for method in default_methods:
            existing = session.query(cls).filter_by(name=method["name"]).first()
            if not existing:
                new_method = cls(name=method["name"], price=method["price"])
                session.add(new_method)

        session.commit()


class Transaction(TableDeclarativeBase):
    """A greed wallet transaction.
    Wallet credit ISN'T calculated from these, but they can be used to recalculate it."""
    # TODO: split this into multiple tables

    # The internal transaction ID
    transaction_id = Column(Integer, primary_key=True)
    # The user whose credit is affected by this transaction
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", backref=backref("transactions"))
    # The value of this transaction. Can be both negative and positive.
    value = Column(Integer, nullable=False)
    # Refunded status: if True, ignore the value of this transaction when recalculating
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    refunded = Column(Boolean, default=False)
    # Extra notes on the transaction
    notes = Column(Text)

    # Payment provider
    provider = Column(String)
    # Transaction ID supplied by Telegram
    telegram_charge_id = Column(String)
    # Transaction ID supplied by the payment provider
    provider_charge_id = Column(String)
    # Extra transaction data, may be required by the payment provider in case of a dispute
    payment_name = Column(String)
    payment_phone = Column(String)
    payment_email = Column(String)

    # Order ID
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    order = relationship("Order", back_populates="transaction")

    promocode_usage_id = Column(Integer, ForeignKey('promocode_usage.id'), nullable=True)
    promocode_usage = relationship("PromocodeUsage", back_populates="transaction")

    # Extra table parameters
    __tablename__ = "transactions"
    __table_args__ = (UniqueConstraint("provider", "provider_charge_id"),)

    def text(self, w: "worker.Worker"):
        current_date_time = datetime.datetime.now()
        string = f"<b>T{self.transaction_id}</b> | {str(self.user)} | {w.Price(self.value)} | {self.date}"
        if self.refunded:
            string += f" | {w.loc.get('emoji_refunded')}"
        if self.provider:
            string += f" | {self.provider}"
        if self.notes:
            string += f" | {self.notes}"
        if self.payment_name:
            string += f" | {self.payment_name}"
        if self.payment_phone:
            string += f" | +{self.payment_phone}"
        if self.payment_email:
            string += f" | {self.payment_email}"
        return string

    def __repr__(self):
        return f"<Transaction {self.transaction_id} for User {self.user_id}>"


class BtcTransaction(TableDeclarativeBase):
    """A btc wallet transaction.
    Wallet credit ISN'T calculated from these, but they can be used to recalculate it."""
    # TODO: split this into multiple tables

    # The internal transaction ID
    transaction_id = Column(Integer, primary_key=True)
    # The user whose credit is affected by this transaction
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User")
    # The value of this transaction. Can be both negative and positive.
    price = Column(Float)
    value = Column(Float)
    currency = Column(Text)
    status = Column(Integer, nullable=False)
    timestamp = Column(Integer)
    # Extra notes on the transaction
    address = Column(Text)
    txid = Column(Text)

    # Extra table parameters
    __tablename__ = "btc_transactions"

    def __str__(self):
        string = f"<b>T{self.transaction_id}</b> | {str(self.user)} | {str(self.price)} | {str(self.value)} | {str(self.currency)} | {str(self.status)} | {str(self.timestamp)} | {str(self.address)}"
        if self.txid:
            string += f" | {self.txid}"
        return string

    def __repr__(self):
        return f"<Transaction {self.transaction_id} for User {self.user_id} {str(self)}>"


class Promocode(TableDeclarativeBase):
    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    is_qr = Column(Boolean, default=False)
    min_amount = Column(Integer, nullable=False)
    max_amount = Column(Integer)
    fixed_amount = Column(Integer)
    uses_left = Column(Integer, nullable=False)
    total_uses = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey('admins.user_id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    usages = relationship("PromocodeUsage", back_populates="promocode")

    creator = relationship("Admin", back_populates="created_promocodes")


class PromocodeUsage(TableDeclarativeBase):
    __tablename__ = 'promocode_usage'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    promocode_id = Column(Integer, ForeignKey('promocodes.id'), nullable=False)
    used_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="promocode_usages")
    promocode = relationship("Promocode", back_populates="usages")
    transaction = relationship("Transaction", back_populates="promocode_usage", uselist=False)


class Admin(TableDeclarativeBase):
    """A greed administrator with his permissions."""

    # The telegram id
    user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    user = relationship("User")
    # Permissions
    edit_products = Column(Boolean, default=False)
    edit_categories = Column(Boolean, default=False)
    edit_subcategories = Column(Boolean, default=False)  # Нове поле
    receive_orders = Column(Boolean, default=False)
    create_transactions = Column(Boolean, default=False)
    display_on_help = Column(Boolean, default=False)
    created_promocodes = relationship("Promocode", back_populates="creator")
    is_owner = Column(Boolean, default=False)
    # Live mode enabled
    live_mode = Column(Boolean, default=False)

    # Extra table parameters
    __tablename__ = "admins"

    def __repr__(self):
        return f"<Admin {self.user_id}>"


class Order(TableDeclarativeBase):
    """An order which has been placed by an user.
    It may include multiple products, available in the OrderItem table."""

    # The unique order id
    order_id = Column(Integer, primary_key=True)
    # The user who placed the order
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    user = relationship("User")
    # Date of creation
    creation_date = Column(DateTime, nullable=False)
    # Date of delivery
    delivery_date = Column(DateTime)
    # Date of refund: if null, product hasn't been refunded
    refund_date = Column(DateTime)
    # Refund reason: if null, product hasn't been refunded
    refund_reason = Column(Text)
    # List of items in the order
    items: typing.List["OrderItem"] = relationship("OrderItem", back_populates="order")
    # Extra details specified by the purchasing user
    notes = Column(Text)
    # Linked transaction
    transaction = relationship("Transaction", back_populates="order", uselist=False)
    delivery_method_id = Column(Integer, ForeignKey("delivery_methods.id"))
    delivery_method = relationship("DeliveryMethod")
    delivery_info = Column(String)

    # Extra table parameters
    __tablename__ = "orders"

    def __repr__(self):
        return f"<Order {self.order_id} placed by User {self.user_id}>"

    def text(self, w: "worker.Worker", user=False):
        items = ""
        for item in self.items:
            items += item.text(w) + "\n"
        if self.delivery_date is not None:
            status_emoji = w.loc.get("emoji_completed")
            status_text = w.loc.get("text_completed")
        elif self.refund_date is not None:
            status_emoji = w.loc.get("emoji_refunded")
            status_text = w.loc.get("text_refunded")
        else:
            status_emoji = w.loc.get("emoji_not_processed")
            status_text = w.loc.get("text_not_processed")
        if user and w.cfg["Appearance"]["full_order_info"] == "no":
            return w.loc.get("user_order_format_string",
                             status_emoji=status_emoji,
                             status_text=status_text,
                             items=items,
                             notes=self.notes,
                             value=str(w.Price(-self.transaction.value))) + \
                (w.loc.get("refund_reason", reason=self.refund_reason) if self.refund_date is not None else "")
        else:
            return status_emoji + " " + \
                w.loc.get("order_number", id=self.order_id) + "\n" + \
                w.loc.get("order_format_string",
                          user=self.user.mention(),
                          date=self.creation_date.isoformat(),
                          items=items,
                          notes=self.notes if self.notes is not None else "",
                          value=str(w.Price(-self.transaction.value))) + \
                (w.loc.get("refund_reason", reason=self.refund_reason) if self.refund_date is not None else "")


class PickupPoint(TableDeclarativeBase):
    __tablename__ = 'pickup_points'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)


class OrderItem(TableDeclarativeBase):
    __tablename__ = "orderitems"

    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    # Extra table parameters
    __tablename__ = "orderitems"

    def text(self, w: "worker.Worker"):
        return f"{self.product.name} - {str(w.Price(self.product.price))}"

    def __repr__(self):
        return f"<OrderItem {self.item_id}>"