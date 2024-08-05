# Strings / localization file for greed
# Can be edited, but DON'T REMOVE THE REPLACEMENT FIELDS (words surrounded by {curly braces})

currency_symbol = "$"

order_number = "Order #{id}"

loading_transactions = "<i>Loading transactions...\n" \
                       "Please wait a few seconds.</i>"

transactions_page = "Page <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

csv_caption = "A 📄 .csv file containing all the transactions from the bot's database has been generated.\n" \
              "You can open the file with LibreOffice Calc to view the details."

conversation_after_start = "Hello 🙏🏾\nWelcome to the Grace Glade shop🎅🏽🍄"

conversation_open_user_menu = "What would you like to do?\n" \
                              "💰 You have <b>{credit}</b> in your wallet.\n" \
                              "\n" \
                              "<i>Select an option from the keyboard.\n" \
                              "If the keyboard is not visible, you can activate it by pressing the button with four squares at the bottom</i>."

profile_info = "ID: {id}\nName: {name}\nBalance: {balance}\nWith us since: {time_with_us}"
day = "day"
days_2_4 = "days"
days_many = "days"

ask_number_of_buttons = "How many buttons do you want to add to the message? (from 0 to 6)"

invalid_number_of_buttons = "Invalid number of buttons. Please enter a number from 0 to 6."

error_cart_menu = "An error occurred while processing the cart. Please try again or contact the administrator."

error_no_deposits_for_promocode = "⚠️ To use a promo code, you need to first top up the bot's account. Please add funds and try again."
promocode_already_used = "You have already used this promo code."
promocode_expired = "This promo code is no longer available."
promocode_applied = "Promo code applied! {amount} has been added to your balance."
error_applying_promocode = "An error occurred while applying the promo code. Please try again later."

ask_product_name = "Enter the product name:"
edit_current_value = "Current value: {value}"
error_duplicate_name = "A product with this name already exists. Please choose a different name."

conversation_admin_product_menu = "Product management menu. Choose an action:"
menu_add_product = "➕ Add new product"
menu_edit_product = "✏️ Edit product"
menu_delete_product = "🗑️ Delete product"
conversation_admin_select_product_to_edit = "Select a product to edit:"

menu_edit_cart = "✏️ Edit cart"
cart_edit_header = "Editing cart:"

success_product_edited = "✅ Product successfully edited!"

ask_button_text = "Enter the text for button {button_number}:"

ask_button_url = "Enter the URL for button {button_number} (must start with http:// or https://):"

checkout_canceled = "Order checkout canceled."

menu_cart = "🛒 Cart"
cart_empty = "Your cart is empty."
cart_contents = "Cart contents:"
cart_total = "Total amount:"
cart_cleared = "Cart cleared."

menu_go_to_cart = "🛒 Go to cart"
menu_main_menu = "🏠 Main menu"

add_funds = "💰 Add funds to wallet"
return_to_main_menu = "🏠 Return to main menu"

insufficient_funds = ("Unfortunately, you don't have enough funds to complete the order.\nTotal amount: {"
                      "total}\nYour balance: {balance}\nShortage: {shortage}\nPlease top up your balance and "
                      "try again.")

ask_broadcast_message = "Enter the message text for broadcasting:"
ask_broadcast_image = "Do you want to add an image to the message?"
send_broadcast_image = "Please send the image for broadcasting."
confirm_broadcast = "Are you sure you want to send this message to all users?"
broadcast_canceled = "Broadcast canceled."
broadcast_complete = "Broadcast completed. Successfully sent: {success_count}/{total_count}"
yes = "Yes"
no = "No"

confirm_delete_category = "Are you sure you want to delete the category {category}?"
confirm_delete_subcategory = "Are you sure you want to delete the subcategory {subcategory}?"
menu_confirm = "✅ Confirm"
deletion_canceled = "Deletion canceled."

ask_category_image = "Send a photo for the category (or press 'Skip'):"
menu_skip = "⏭ Skip"
order_canceled = "Order canceled. Cart cleared."
select_category_for_product = "Select a category for the product:"

menu_add_subcategory = "➕ Add subcategory"
menu_edit_category = "✏️ Edit category"
menu_view_subcategories = "👁️ View subcategories"
category_action_prompt = "Choose an action for the category:"
ask_category_name = "Enter the category name:"
ask_category_description = "Enter the category description (or skip this step):"
category_deleted = "Category successfully deleted."
category_not_found = "Category not found."

product_price = "Price"
product_in_cart = "In cart"
product_pieces = "pcs"
product_subtotal = "Subtotal in cart"
product_added_to_cart = "Product added to cart"
product_removed_from_cart = "Product removed from cart"
menu_add_to_cart = "➕ Add to cart"
menu_remove_from_cart = "➖ Remove from cart"

post_order_options = "What would you like to do next?"
continue_shopping = "🛒 Continue shopping"
no_categories_to_delete = "There are no categories to delete."
no_subcategories_to_delete = "There are no subcategories to delete."
select_category_to_delete = "Select a category to delete:"
select_subcategory_to_delete = "Select a subcategory to delete:"
subcategory_deleted = "Subcategory successfully deleted."
subcategory_not_found = "Subcategory not found."

choose_pickup_point = "Choose a pickup point:"
error_no_pickup_points = "Sorry, there are no pickup points available at the moment. Please choose another delivery method."
ask_nova_poshta_city = "Enter the delivery city:"
ask_nova_poshta_office = "Enter the Nova Poshta office number:"
ask_nova_poshta_phone = "Enter your phone number:"
ask_nova_poshta_name = "Enter your full name:"
ask_kyiv_address = "Enter the delivery address in Kyiv:"
ask_kyiv_phone = "Enter your contact phone number:"
error_checkout_canceled = "Order checkout canceled. Please try again or contact customer support."

conversation_open_admin_menu = "You are a 💼 <b>Manager</b> of this store!\n" \
                               "What would you like to do?\n" \
                               "\n" \
                               "<i>Select an option from the keyboard.\n" \
                               "If the keyboard is not visible, you can activate it by pressing the button with four squares at the bottom</i>."

conversation_payment_method = "How would you like to add funds to your wallet?"

menu_edit_admins = "👥 Edit managers"

admin_properties = "<b>Access rights for {name}:</b>"
prop_edit_products = "Edit products"
prop_edit_categories = "Edit categories"
prop_edit_subcategories = "Edit subcategories"
prop_receive_orders = "Receive orders"
prop_create_transactions = "Create transactions"
prop_display_on_help = "Display in help"

conversation_confirm_admin_promotion = "Are you sure you want to grant this user manager rights?"

promocode_management_menu = "Choose an action for promo code management:"
menu_manage_promocodes = "🎟 Manage promo codes"
menu_delete_promocode = "🗑 Delete promo code"
choose_promocode_type = "Choose the promo code type:"
choose_amount_type = "Choose the amount type:"
ask_fixed_amount = "Enter the fixed amount:"
ask_min_amount = "Enter the minimum amount:"
ask_max_amount = "Enter the maximum amount:"
ask_uses_number = "Enter the number of possible activations:"
promocode_created_qr = "QR code created: {code}\nLink: {link}"
promocode_created_text = "Promo code created: {code}"
promocode_info = "Code: {code}\nType: {type}\nAmount: {amount}\nActivations left: {uses_left}/{total_uses}\nCreated by: {creator}\nUsed: {used_count} times\nTotal amount: {total_amount}"
no_active_promocodes = "There are no active promo codes."
text_promocode = "Text"
no_promocodes_to_delete = "There are no promo codes to delete."
choose_promocode_to_delete = "Choose a promo code to delete:"
promocode_deleted = "Promo code {code} deleted."
promocode_not_found = "Promo code not found."

conversation_admin_select_product_to_delete = "❌ Which product needs to be deleted?"

cancel_order = "❌ Cancel order"
confirm = "✅ Confirm"
confirm_delivery_method = "You have chosen the delivery method: {method}\nDelivery price: {price}\nInformation: {info}\n\nConfirm your choice:"
or_press_back = "Or press 'Back' to return"

conversation_admin_select_user = "Select a user to edit."

conversation_cart_actions = "<i>Add products to the cart by pressing the Add button." \
                            "  When you've made your selection, return to this message" \
                            " and press the Done button.</i>"

conversation_confirm_cart = "🛒 You have the following products in your cart:\n" \
                            "{product_list}" \
                            "Total: <b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>To continue, press Done.\n" \
                            "If you've changed your mind, choose Cancel.</i>"

conversation_live_orders_start = "You are in <b>Live Orders</b> mode\n" \
                                 "All new orders from customers will appear in this chat in real-time," \
                                 " and you can mark them as ✅ Completed" \
                                 " or ✴️ Refund to the customer."

conversation_live_orders_stop = "<i>Press the Stop button in this chat to exit this mode.</i>"

conversation_open_help_menu = "How can we help you?"

conversation_language_select = "Select a language:"

conversation_switch_to_user_mode = " You have switched to 👤 Customer mode.\n" \
                                   "If you want to return to the 💼 Manager menu, restart the conversation with /start."

conversation_expired = "🕐  I haven't received any messages for a long time, so I ended the conversation" \
                       " to conserve resources.\n" \
                       "To start again, send the /start command."

conversation_admin_select_category = "✏️ Which category do you want to edit"

ask_subcategory_name = "Enter the subcategory name:"

ask_parent_category = "Select the parent category for the new subcategory:"

error_no_root_categories = "Error: there are no root categories. Please create a root category first."

success_category_created = "✅ Category successfully created!"

success_subcategory_created = "✅ Subcategory successfully created!"

ask_subcategory_description = "Enter the subcategory description (or skip this step):"

ask_subcategory_image = "Send an image for the subcategory (or skip this step):"

conversation_select_category = "Select a category"

conversation_order_category = "Select a category:"

error_product_not_found = "Product not found."

menu_back = "⬅️ Back"
menu_checkout = "💳 Checkout"
menu_clear_cart = "🗑️ Clear cart"

menu_credit_history = "📈 Top-up history"

menu_promocode = "🤩 Enter promo code"

ask_promocode = "Enter the promo code:"

menu_order = "🛒 Products"

menu_uncategorized = "Uncategorized"

menu_go_back = "🔙 Go back"

menu_order_status = "🛍 My orders"

menu_add_credit = "💵 Add funds to wallet"

menu_profile = "🧾 Profile"

menu_create_promocode = "Create promo code/QR code"

menu_list_promocodes = "Promo code statistics"

credit_history_null = "You haven't made any top-ups yet!"

credit_history = "Your top-up history:"

menu_cash = "💵 Cash"

menu_credit_card = "💳 Credit card"

menu_products = "📝️ Products"

menu_orders = "📦 Orders"

menu_transactions = "💳 Transaction list"

menu_edit_credit = "💰 Create transaction"

menu_user_mode = "👤 Customer mode"

menu_cancel = "🔙 Cancel"

menu_done = "✅️ Done"

menu_categories = "📝️ Categories"

menu_add_category = "✨ New category"

menu_delete_category = "❌ Delete category"

menu_pay = "💳 Pay"

menu_complete = "✅ Complete"

menu_refund = "✴️ Refund"

menu_stop = "🛑 Stop"

menu_all_products = "All products"

menu_help = "❓ Help"

menu_guide = "📖 Guide"

menu_promo_text = "Text"

menu_promo_qr = "QR code"

menu_promo_fixed = "Fixed"

menu_promo_range = "Range"

menu_next = "▶️ Next"

menu_previous = "◀️ Previous"

menu_contact_shopkeeper = "👨‍💼 Shop contacts"

menu_csv = "📄 .csv"

menu_language = "🇬🇧 Language"

emoji_yes = "✅"

emoji_no = "🚫"

ask_product_description = "What will be the product description?"

ask_product_price = "What will be the price?\n" \
                    "Enter <code>X</code> if the product is not currently for sale."

ask_product_image = "🖼 What image should be added to the product?\n" \
                    "\n" \
                    "<i>Send a photo, or Skip this step.</i>"

ask_order_notes = "Leave a message with this purchase?\n" \
                  "💼 The message will be available to the Store Manager.\n" \
                  "\n" \
                  "<i>Send your message, or press Skip" \
                  " to not leave a message.</i>"

ask_refund_reason = " Write the reason for the refund.\n" \
                    "👤  The reason will be available to the customer."

ask_transaction_notes = " Add a message to the transaction.\n" \
                        "👤 The message will be available to the customer after the top-up/withdrawal" \
                        " and to the 💼 Administrator in the transaction logs."

ask_credit = "How do you want to change the customer's balance?\n" \
             "\n" \
             "<i>Send a message with the amount.\n" \
             "Use </i><code>+</code><i> to add funds to the account," \
             " and </i><code>-</code><i> to deduct funds.</i>"

downloading_image = "I'm downloading the photo!\n" \
                    "It may take some time... Please be patient!\n" \
                    "I won't be able to respond while the download is in progress."

payment_cash = "You can top up with cash directly in the store.\n" \
               "Make the payment and give this id to the manager:\n" \
               "<b>{user_cash_id}</b>"

payment_cc_amount = "How much would you like to add to your wallet?\n" \
                    "\n" \
                    "<i>Choose an amount from the suggested values, or enter manually in a message.</i>"

payment_invoice_title = "Top-up"

payment_invoice_description = "Paying this invoice will add {amount} to your wallet."

payment_invoice_label = "Payment"

payment_invoice_fee_label = "Top-up fee"

notification_order_placed = "A new order has been received:\n" \
                            "\n" \
                            "{order}"

notification_order_completed = "Your order has been successfully completed!\n" \
                               "\n" \
                               "{order}"

notification_order_refunded = "Your order has been canceled. Funds have been refunded!\n" \
                              "\n" \
                              "{order}"

notification_transaction_created = "ℹ️  New transaction in your wallet:\n" \
                                   "{transaction}"

contact_shopkeeper = "The following staff members are currently available and can help:\n" \
                     "{shopkeepers}\n" \
                     "<i>Choose one and write to them in Telegram chat.</i>"

success_category_edited = "✅ Category successfully created/updated!"

ask_category_parent = "Select the parent category for this category (or 'None' for root category):"

success_product_deleted = "✅ Product successfully deleted!"

success_order_created = "✅ Order successfully sent!\n" \
                        "\n" \
                        "{order}"

success_order_refunded = "✴️ Funds for order #{order_id} have been refunded."

success_transaction_created = "✅ Transaction successfully created!\n" \
                              "{transaction}"

error_payment_amount_over_max = "⚠️ The maximum amount for a single transaction is {max_amount}."

error_payment_amount_under_min = "⚠️ The minimum amount for a single transaction is {min_amount}."

error_during_checkout = "An error occurred during checkout. Please try again later."
order_confirmation = "Order #{order_id} successfully created!\nTotal amount: {total}\nDelivery method: {delivery_method}"
manage_delivery_and_pickup = "Choose an action to manage delivery and pickup:"
menu_view_delivery_methods = "👀 View delivery methods"
menu_view_pickup_points = "👀 View pickup points"
view_delivery_methods = "Select a delivery method to edit:"
edit_pickup_point = "Choose what you want to change:"
edit_pickup_point_address = "Change address"
edit_pickup_point_description = "Change description"
toggle_pickup_point_status = "Change status (active/inactive)"
ask_new_pickup_point_address = "Enter the new address for the pickup point:"
ask_new_pickup_point_description = "Enter the new description for the pickup point:"
error_pickup_point_not_found = "❌ Pickup point not found."
success_pickup_point_updated = "✅ Pickup point successfully updated!"

choose_delivery_method = "Choose a delivery method:"
ask_pickup_point_address = "Enter the address of the pickup point:"
ask_pickup_point_description = "Enter a description for the pickup point (or skip this step):"
success_pickup_point_added = "✅ Pickup point successfully added!"
no_pickup_points = "There are currently no active pickup points."
pickup_points_list = "List of pickup points:"
menu_add_pickup_point = "📍 Add pickup point"
menu_broadcast_message = "📢 Broadcast message"

menu_add_delivery_method = "➕ Add new delivery method"
ask_delivery_method_name = "Enter the name of the new delivery method:"
ask_delivery_method_price = "Enter the delivery price (in minimum currency units):"
success_delivery_method_added = "✅ New delivery method successfully added!"
error_delivery_method_not_found = "❌ Delivery method not found."
edit_delivery_method = "Choose what you want to change:"
edit_delivery_method_name = "Change name"
edit_delivery_method_price = "Change price"
toggle_delivery_method_status = "Change status (active/inactive)"
ask_new_delivery_method_name = "Enter the new name for the delivery method:"
ask_new_delivery_method_price = "Enter the new price for delivery (in minimum currency units):"
success_delivery_method_updated = "✅ Delivery method successfully updated!"

error_not_enough_credit = "⚠️ You don't have enough funds to complete the order."

error_order_already_cleared = "⚠️  This order has already been processed."

error_no_orders = "⚠️  You haven't made any orders yet, so it's empty here."

error_user_does_not_exist = "⚠️  This user does not exist."

fatal_conversation_exception = "☢️ Oh no! An <b>error</b> interrupted our conversation\n" \
                               "The bot owner has been notified about the error.\n" \
                               "To start the conversation again, send the /start command."
help_msg = ""

error_no_delivery_methods = "There are currently no active delivery methods."

error_listing_promocodes = "An error occurred while listing promo codes."

invalid_promocode = "Invalid promo code"

bot_info = ""