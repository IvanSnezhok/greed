# Strings / localization file for greed
# Can be edited, but DON'T REMOVE THE REPLACEMENT FIELDS (words surrounded by {curly braces})

# Currency symbol
currency_symbol = "₴"

# Positioning of the currency symbol
currency_format_string = "{value} {symbol}"

# Quantity of a product in stock
in_stock_format_string = "{quantity} наявні"

# Copies of a product in cart
in_cart_format_string = "{quantity} в кошику"

# Product information
product_format_string = "<b>{name}</b>\n" \
                        "{description}\n" \
                        "{price}\n" \
                        "<b>{cart}</b>"

# Order number, displayed in the order info
order_number = "Замовлення #{id}"

# Order info string, shown to the admins
order_format_string = "Користувач {user}\n" \
                      "Створено {date}\n" \
                      "\n" \
                      "{items}\n" \
                      "ЗАГАЛОМ: <b>{value}</b>\n" \
                      "\n" \
                      "Нотатка: {notes}\n"

# Order info string, shown to the user
user_order_format_string = "{status_emoji} <b>Замовлення {status_text}</b>\n" \
                           "{items}\n" \
                           "Загалом: <b>{value}</b>\n" \
                           "\n" \
                           "Нотатка: {notes}\n"

# Transaction page is loading
loading_transactions = "<i>Завантажую транзакції...\n" \
                       "Зачекайте кілька секунд.</i>"

# Transactions page
transactions_page = "Сторінка <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

# transactions.csv caption
csv_caption = "Файл 📄 .csv, який має всі транзакції з бази даних бота було сгенеровано.\n" \
              "Можете відкрити файл за допомогою LibreOffice Calc, щоб переглянути деталі."

# Conversation: the start command was sent and the bot should welcome the user
conversation_after_start = "Доброго дня 🙏🏾\nВітаємо у крамничці Grace Glade🎅🏽🍄"

# Conversation: to send an inline keyboard you need to send a message with it
conversation_open_user_menu = "Щоб ви хотіли зробити?\n" \
                              "💰 У вас <b>{credit}</b> в гаманці.\n" \
                              "\n" \
                              "<i>Виберіть опцію з варіантів на клавіатурі.\n" \
                              "Якщо клавіатури не видно - її можна активувати кнопкою з чотирма квадратами внизу</i>."

profile_info = "ID: {id}\nІм'я: {name}\nБаланс: {balance}\nЗ нами: {time_with_us}"
day = "день"
days_2_4 = "дні"
days_many = "днів"

ask_number_of_buttons = "Скільки кнопок ви хочете додати до повідомлення? (від 0 до 6)"

invalid_number_of_buttons = "Невірна кількість кнопок. Будь ласка, введіть число від 0 до 6."

cart_increase = "➕"
cart_decrease = "➖"
cart_remove = "🗑"


error_cart_menu = "Виникла помилка при обробці кошика. Будь ласка, спробуйте ще раз або зверніться до адміністратора."

# Додайте ці рядки в кінець файлу old_uk.py

error_no_deposits_for_promocode = "⚠️ Для використання промокоду необхідно спочатку поповнити рахунок бота. Будь ласка, поповніть рахунок і спробуйте знову."
promocode_already_used = "Ви вже використовували цей промокод."
promocode_expired = "Цей промокод більше не доступний."
promocode_applied = "Промокод застосовано! Додано {amount} до вашого балансу."
error_applying_promocode = "Виникла помилка при застосуванні промокоду. Спробуйте ще раз пізніше."

ask_product_name = "Введіть назву продукту:"
edit_current_value = "Поточне значення: {value}"
error_duplicate_name = "Продукт з такою назвою вже існує. Будь ласка, виберіть іншу назву."

conversation_admin_product_menu = "Меню управління продуктами. Оберіть дію:"
menu_add_product = "➕ Додати новий продукт"
menu_edit_product = "✏️ Редагувати продукт"
menu_delete_product = "🗑️ Видалити продукт"
conversation_admin_select_product_to_edit = "Оберіть продукт для редагування:"

error_sending_message = "Виникла помилка при відправці повідомлення. Будь ласка, спробуйте ще раз."

menu_edit_cart = "✏️ Редагувати кошик"
cart_edit_header = "Редагування кошика:"

edit_product_prompt = "Що ви хочете відредагувати?"
edit_product_name = "Змінити назву"
edit_product_description = "Змінити опис"
edit_product_price = "Змінити ціну"
edit_product_category = "Змінити категорію"
edit_product_image = "Змінити зображення"
success_product_edited = "✅ Товар успішно відредаговано!"

select_category_first = "Будь ласка, спочатку виберіть категорію для створення підкатегорії.",

ask_button_text = "Введіть текст для кнопки {button_number}:"

ask_button_url = "Введіть URL для кнопки {button_number} (має починатися з http:// або https://):"

ask_number_of_buttons = "Скільки кнопок ви хочете додати до повідомлення?"

ask_button_text_and_url = "Введіть текст та URL для кнопки {button_number} у форматі 'текст|url':"

invalid_button_format = "Невірний формат. Будь ласка, введіть у форматі 'текст|url'."

checkout_canceled = "Оформлення замовлення скасовано."

menu_cart = "🛒 Кошик"
cart_empty = "Ваш кошик порожній."
cart_contents = "Вміст кошика:"
cart_total = "Загальна сума:"
cart_checkout = "🛍️ Оформити замовлення"
cart_clear = "🗑️ Очистити кошик"
cart_cleared = "Кошик очищено."

menu_go_to_cart = "🛒 Перейти до кошика"
menu_main_menu = "🏠 Головне меню"

add_funds = "💰 Поповнити гаманець"
return_to_main_menu = "🏠 Повернутися в головне меню"

insufficient_funds = ("На жаль, на вашому балансі недостатньо коштів для оформлення замовлення.\nЗагальна сума: {"
                      "total}\nВаш баланс: {balance}\nНе вистачає: {shortage}\nБудь ласка, поповніть баланс і "
                      "спробуйте знову.")

ask_broadcast_message = "Введіть текст повідомлення для розсилки:"
ask_broadcast_image = "Чи бажаєте додати зображення до повідомлення?"
ask_broadcast_button = "Чи бажаєте додати кнопку до повідомлення?"
send_broadcast_image = "Будь ласка, надішліть зображення для розсилки."
ask_button_text = "Введіть текст для кнопки:"
ask_button_url = "Введіть URL для кнопки:"
confirm_broadcast = "Ви впевнені, що хочете розіслати це повідомлення всім користувачам?"
broadcast_canceled = "Розсилку скасовано."
broadcast_complete = "Розсилку завершено. Успішно надіслано: {success_count}/{total_count}"
yes = "Так"
no = "Ні"

confirm_delete_category = "Ви впевнені, що хочете видалити категорію {category}?"
confirm_delete_subcategory = "Ви впевнені, що хочете видалити підкатегорію {subcategory}?"
menu_confirm = "✅ Підтвердити"
deletion_canceled = "Видалення скасовано."

ask_category_image = "Надішліть фото для категорії (або натисніть 'Пропустити'):"
menu_skip = "⏭ Пропустити"
description_too_long = "Опис занадто довгий. Максимальна довжина: {max_length} символів."
deletion_canceled = "Видалення скасовано."
order_canceled = "Замовлення скасовано. Кошик очищено."
select_category_for_product = "Виберіть категорію для продукту:"

menu_add_subcategory = "➕ Додати підкатегорію"
menu_edit_category = "✏️ Редагувати категорію"
menu_view_subcategories = "👁️ Переглянути підкатегорії"
category_action_prompt = "Оберіть дію для категорії:"
ask_category_name = "Введіть назву категорії:"
ask_category_description = "Введіть опис категорії (або пропустіть цей крок):"
category_created = "Категорію успішно створено."
category_updated = "Категорію успішно оновлено."
confirm_delete_category = "Ви впевнені, що хочете видалити категорію {category}?"
category_deleted = "Категорію успішно видалено."
deletion_canceled = "Видалення скасовано."
category_not_found = "Категорію не знайдено."

product_price = "Ціна"
product_in_cart = "У кошику"
product_pieces = "шт."
product_subtotal = "Сума в кошику"
product_added_to_cart = "Товар додано до кошика"
product_removed_from_cart = "Товар видалено з кошика"
menu_add_to_cart = "➕ Додати до кошика"
menu_remove_from_cart = "➖ Видалити з кошика"

post_order_options = "Що б ви хотіли зробити далі?"
continue_shopping = "🛒 Продовжити покупки"
return_to_main_menu = "🏠 Повернутися до головного меню"

no_categories_to_delete = "Немає категорій для видалення."
no_subcategories_to_delete = "Немає підкатегорій для видалення."
select_category_to_delete = "Виберіть категорію для видалення:"
select_subcategory_to_delete = "Виберіть підкатегорію для видалення:"
category_deleted = "Категорію успішно видалено."
subcategory_deleted = "Підкатегорію успішно видалено."
category_not_found = "Категорію не знайдено."
subcategory_not_found = "Підкатегорію не знайдено."

choose_pickup_point = "Оберіть точку самовивозу:"
error_no_pickup_points = "На жаль, зараз немає доступних точок самовивозу. Будь ласка, оберіть інший спосіб доставки."
ask_nova_poshta_city = "Введіть місто доставки:"
ask_nova_poshta_office = "Введіть номер відділення Нової пошти:"
ask_nova_poshta_phone = "Введіть ваш номер телефону:"
ask_nova_poshta_name = "Введіть ваше ПІБ:"
ask_kyiv_address = "Введіть адресу доставки в Києві:"
ask_kyiv_phone = "Введіть ваш номер телефону для зв'язку:"
error_checkout_canceled = "Оформлення замовлення скасовано. Будь ласка, спробуйте ще раз або зверніться до служби підтримки."

# Conversation: like above, but for administrators
conversation_open_admin_menu = "Ви є 💼 <b>Менеджером</b> цього магазину!\n" \
                               "Що б ви хотіли зробити?\n" \
                               "\n" \
                               "<i>Виберіть опцію з варіантів на клавіатурі.\n" \
                               "Якщо клавіатури не видно - її можна активувати кнопкою з чотирма квадратами внизу</i>."

# Conversation: select a payment method
conversation_payment_method = "Як би Ви хотіли поповнити гаманець?"

description_too_long_with_image = "Опис занадто довгий для товару з зображенням. Будь ласка, введіть опис, який не перевищує 1024 символи."

description_too_long = "Опис занадто довгий. Будь ласка, введіть опис, який не перевищує 4096 символів."
description_too_long_with_image = "Опис занадто довгий для товару з зображенням. Будь ласка, введіть опис, який не перевищує 1024 символи."

description_too_long = "Опис занадто довгий. Будь ласка, введіть опис, який не перевищує 1024 символи."

# Admin menu: edit admins
menu_edit_admins = "👥 Редагувати менеджерів"

# Admin properties
admin_properties = "<b>Права доступу для {name}:</b>"
prop_edit_products = "Редагувати товари"
prop_edit_categories = "Редагувати категорії"
prop_edit_subcategories = "Редагувати підкатегорії"
prop_receive_orders = "Отримувати замовлення"
prop_create_transactions = "Створювати транзакції"
prop_display_on_help = "Відображати в довідці"

# Confirm admin promotion
conversation_confirm_admin_promotion = "Ви впевнені, що хочете надати цьому користувачу права менеджера?"

# Promocode management
promocode_management_menu = "Оберіть дію для управління промокодами:"
menu_manage_promocodes = "🎟 Управління промокодами"
menu_delete_promocode = "🗑 Видалити промокод"
choose_promocode_type = "Оберіть тип промокоду:"
choose_amount_type = "Оберіть тип суми:"
ask_fixed_amount = "Введіть фіксовану суму:"
ask_min_amount = "Введіть мінімальну суму:"
ask_max_amount = "Введіть максимальну суму:"
ask_uses_number = "Введіть кількість можливих активацій:"
promocode_created_qr = "QR-код створено: {code}\nПосилання: {link}"
promocode_created_text = "Промокод створено: {code}"
promocode_info = "Код: {code}\nТип: {type}\nСума: {amount}\nЗалишилось активацій: {uses_left}/{total_uses}\nСтворено: {creator}\nВикористано: {used_count} разів\nЗагальна сума: {total_amount}"
no_active_promocodes = "Немає активних промокодів."
text_promocode = "Текстовий"
unknown = "Невідомо"
no_promocodes_to_delete = "Немає промокодів для видалення."
choose_promocode_to_delete = "Оберіть промокод для видалення:"
promocode_deleted = "Промокод {code} видалено."
promocode_not_found = "Промокод не знайдено."

# Conversation: select a product to edit
conversation_admin_select_product = "✏️ Який продукт потрібно редагувати?"

# Conversation: select a product to delete
conversation_admin_select_product_to_delete = "❌ Який продукт потрібно видалит?"

cancel_order = "❌ Скасувати замовлення"
confirm = "✅ Підтвердити"
confirm_delivery_method = "Ви обрали спосіб доставки: {method}\nЦіна доставки: {price}\nІнформація: {info}\n\nПідтвердіть ваш вибір:"
or_press_back = "Або натисніть 'Назад', щоб повернутися"
order_canceled = "Замовлення скасовано. Повертаємось до головного меню."


ask_continue_to_checkout = "Бажаєте продовжити оформлення замовлення?"
menu_continue_to_checkout = "Продовжити оформлення"

# Conversation: select a user to edit
conversation_admin_select_user = "Виберіть користувача для редагування."

# Conversation: click below to pay for the purchase
conversation_cart_actions = "<i>Додайте продукти в кошик натисканням кнопки Додати." \
                            "  Коли зробите Ваш вибір, повертайтесь до цього повідомлення" \
                            " і натисніть кнопку Готово.</i>"

# Conversation: confirm the cart contents
conversation_confirm_cart = "🛒 У вас в кошику наступні продукти:\n" \
                            "{product_list}" \
                            "Всього: <b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>Щоб продовжити натисніть Готово.\n" \
                            "Якщо змінили свою думку - обирайте Відміна.</i>"

# Live orders mode: start
conversation_live_orders_start = "Ви в режимі <b>Свіжі Замовлення</b>\n" \
                                 "Всі нові замовення від покупців зʼявляться в цьому чаті в режимі живого часу," \
                                 " і ви зможете помічати їх ✅ Виконано" \
                                 " або ✴️ Повернути кошти покупцю."

# Live orders mode: stop receiving messages
conversation_live_orders_stop = "<i>Натисніть кнопку Стоп в цьому чаті, щоб зупинити цей режим.</i>"

# Conversation: help menu has been opened
conversation_open_help_menu = "Як можемо Вам допомогти?"

# Conversation: language select menu header
conversation_language_select = "Оберіть мову:"

# Conversation: confirm promotion to admin
conversation_confirm_admin_promotion = "Ви впевнені, що хочете підвищити цього користувача до 💼 Менеджера?\n" \
                                       "Цю дію неможливо відмінити!"

# Conversation: switching to user mode
conversation_switch_to_user_mode = " Ви перейшли в режим 👤 Замовника.\n" \
                                   "Якщо хочете повернутись в меню 💼 Менеджера, рестартуйте розмову з /start."

# Notification: the conversation has expired
conversation_expired = "🕐  За довгий час я не отримав жодного повідомлення, тому я завершив розмову" \
                       " щоб зберегти ресурси.\n" \
                       "Щоб почату знову, надішліть команду /start ."

# Conversation: select a category to edit
conversation_admin_select_category = "✏️ Яку категорію бажаєте відредагувати"

# Conversation: select a category to delete
conversation_admin_select_category_to_delete = "❌ Яку категорію бажаєте видалити?"

# Menu: add subcategory
menu_add_subcategory = "✨ Нова підкатегорія"

# Admin menu: delete subcategory
menu_delete_subcategory = "❌ Видалити підкатегорію"

# Ask for subcategory name
ask_subcategory_name = "Введіть назву підкатегорії:"

# Ask for parent category
ask_parent_category = "Виберіть батьківську категорію для нової підкатегорії:"

# Error: no root categories
error_no_root_categories = "Помилка: немає жодної кореневої категорії. Спочатку створіть кореневу категорію."

# Success: category created
success_category_created = "✅ Категорію успішно створено!"

# Success: subcategory created
success_subcategory_created = "✅ Підкатегорію успішно створено!"

# Ask for category description
ask_category_description = "Введіть опис категорії (або пропустіть цей крок):"

# Ask for subcategory description
ask_subcategory_description = "Введіть опис підкатегорії (або пропустіть цей крок):"

# Ask for category image
ask_category_image = "Надішліть зображення для категорії (або пропустіть цей крок):"

# Ask for subcategory image
ask_subcategory_image = "Надішліть зображення для підкатегорії (або пропустіть цей крок):"

# Conversation: select category
conversation_select_category = "Оберіть категорію"

# Order menu
conversation_order_category = "Оберіть категорію:"

# Product
error_product_not_found = "Товар не знайдено."
product_added_to_cart = "Товар додано до кошика."

# Cart
cart_empty = "Ваш кошик порожній."
cart_contents = "Вміст кошика:"
cart_total = "Загальна сума"
cart_cleared = "Кошик очищено."

# Checkout
checkout_not_implemented = "Вибачте, функція оформлення замовлення ще не реалізована."

# Menu items
menu_back = "⬅️ Назад"
menu_cart = "🛒 Кошик"
menu_checkout = "💳 Оформити замовлення"
menu_clear_cart = "🗑️ Очистити кошик"

# User menu: credit history
menu_credit_history = "📈 Історія поповнення"

# User menu: menu promocode
menu_promocode = "🤩 Ввести промокод"

ask_promocode = "Введіть промокод:"

promocode_applied = "Промокод застосовано!"

promocode_invalid = "Недійсний промокод."

# User menu: order
menu_order = "🛒 Товари"

# Menu: uncategorized
menu_uncategorized = "Без категорії"

# Menu: go back
menu_go_back = "🔙 Повернутися"

# User menu: order status
menu_order_status = "🛍 Мої замовлення"

# User menu: add credit
menu_add_credit = "💵 Поповнити гаманець"

menu_profile = "🧾 Профіль"

menu_create_promocode = "Створити промокод/QR-код"

menu_list_promocodes = "Статистика промокодів"

credit_history_null = "У вас ще не було поповнень!"

credit_history = "Історія Ваших поповнень:"

# User menu: bot info
menu_bot_info = "ℹ️ Інформація про бот"

# User menu: cash
menu_cash = "💵 Готівкою"

# User menu: credit card
menu_credit_card = "💳 Кредитною картою"

# Admin menu: products
menu_products = "📝️ Продукти"

# Admin menu: orders
menu_orders = "📦 Замовлення"

# Menu: transactions
menu_transactions = "💳 Список транзакцій"

# Menu: edit credit
menu_edit_credit = "💰 Створити транзакцію"

# Admin menu: go to user mode
menu_user_mode = "👤 Режим замовника"

# Admin menu: add product
menu_add_product = "✨ Новий продукт"

# Admin menu: delete product
menu_delete_product = "❌ Видалити продукт"

# Menu: cancel
menu_cancel = "🔙 Відміна"

# Menu: skip
menu_skip = "⏭ Пропустити"

# Menu: done
menu_done = "✅️ Готово"

# Menu: category
menu_categories = "📝️ Категорії"

# Menu: add category
menu_add_category = "✨ Нова категорія"

# Admin menu: delete category
menu_delete_category = "❌ Видалити категорію"

# Menu: pay invoice
menu_pay = "💳 Заплатити"

# Menu: complete
menu_complete = "✅ Готово"

# Menu: refund
menu_refund = "✴️ Повернення коштів"

# Menu: stop
menu_stop = "🛑 Стоп"

# Menu: Всі товари
menu_all_products = "Всі товари"

# Menu: add to cart
menu_add_to_cart = "➕ Додати"

# Menu: remove from cart
menu_remove_from_cart = "➖ Прибрати"

# Menu: help menu
menu_help = "❓ Допомога"

# Menu: guide
menu_guide = "📖 Інструкція"

menu_promo_text = "Текстовий"

menu_promo_qr = "QR-код"

menu_promo_fixed = "Фіксована"

menu_promo_range = "Діапазон"

# Menu: next page
menu_next = "▶️ Наступна"

# Menu: previous page
menu_previous = "◀️ Попередня"

# Menu: contact the shopkeeper
menu_contact_shopkeeper = "👨‍💼 Контакти магазину"

# Menu: generate transactions .csv file
menu_csv = "📄 .csv"

# Menu: language
menu_language = "🇺🇦 Мова"

# Menu: edit admins list
menu_edit_admins = "🏵 Редагувати менеджерів"

# Emoji: unprocessed order
emoji_not_processed = "*️⃣"

# Emoji: completed order
emoji_completed = "✅"

# Emoji: refunded order
emoji_refunded = "✴️"

# Emoji: yes
emoji_yes = "✅"

# Emoji: no
emoji_no = "🚫"

# Text: unprocessed order
text_not_processed = "очікує"

# Text: completed order
text_completed = "завершено"

# Text: refunded order
text_refunded = "повернуто"

# Text: product not for sale
text_not_for_sale = "Не продається"

# Add category: name?
ask_category_name = "Яка буде назва категорії?"

# Add product: category?
ask_product_category = "В якій категорії буде товар?"

# Add product: name?
ask_product_name = "Як назвати продукт?"

# Add product: description?
ask_product_description = "Який буде опис продукту?"

# Add product: price?
ask_product_price = "Яка буде ціна?\n" \
                    "Введіть <code>X</code> Якщо продукт зараз не продається."

# Add product: image?
ask_product_image = "🖼 Яку картинку додати до продукта?\n" \
                    "\n" \
                    "<i>Надішліть фото, або Пропустіть цей крок.</i>"

ask_product_category = "Оберіть категорію товару"

# Order product: notes?
ask_order_notes = "Залишити повідомлення разом з цією покупкою?\n" \
                  "💼 Повідомлення буде доступне Менеджеру магазину.\n" \
                  "\n" \
                  "<i>Надішліть Ваше повідомлення, або натисність Пропустити" \
                  " щоб не залишати повідомлення.</i>"

# Refund product: reason?
ask_refund_reason = " Напишіть причину повернення коштів.\n" \
                    "👤  Причина буде доступна замовнику."

# Edit credit: notes?
ask_transaction_notes = " Додайте повідомлення до транзакції.\n" \
                        "👤 Повідомлення буде доступне замовнику після поповнення/списання" \
                        " і 💼 Адміністратору в логах транзакцій."

# Edit credit: amount?
ask_credit = "Як ви хочете змінити баланс замовника?\n" \
             "\n" \
             "<i>Надішліть повідомлення з сумою.\n" \
             "Використовуйте  </i><code>+</code><i> щоб поповнити рахунок," \
             " і знак </i><code>-</code><i> щоб списати кошти.</i>"

# Header for the edit admin message
admin_properties = "<b>Доступи користувача {name}:</b>"

# Edit admin: can edit products?
prop_edit_products = "Редагувати продукти"

# Edit admin: can receive orders?
prop_receive_orders = "Отримувати замовлення"

# Edit admin: can create transactions?
prop_create_transactions = "Керувати транзакціями"

# Edit admin: show on help message?
prop_display_on_help = "Показувати замовнику"

# Thread has started downloading an image and might be unresponsive
downloading_image = "Я завантажую фото!\n" \
                    "Може зайняти деякий час... Майте терпіння!\n" \
                    "Я не зможу відповідати, поки йде завантаження."

# Edit product: current value
edit_current_value = "Поточне значення:\n" \
                     "<pre>{value}</pre>\n" \
                     "\n" \
                     "<i>Натисність Пропустити під цим повідомленням, щоб залишити значення таким.</i>"

# Payment: cash payment info
payment_cash = "Ви можете поповнити готівкою прямо в магазині.\n" \
               "Розрахуйтесь і дайте цей id менеджеру:\n" \
               "<b>{user_cash_id}</b>"

# Payment: invoice amount
payment_cc_amount = "На яку сумму ви хочете поповнити гаманець?\n" \
                    "\n" \
                    "<i>Виберіть сумму із запропонованих значень, або введіть вручну в повідомленні.</i>"

# Payment: add funds invoice title
payment_invoice_title = "Поповнення"

# Payment: add funds invoice description
payment_invoice_description = "Оплата цього рахунку додасть {amount} в ваш гаманець."

# Payment: label of the labeled price on the invoice
payment_invoice_label = "Платіж"

# Payment: label of the labeled price on the invoice
payment_invoice_fee_label = "Оплата за поповнення"

# Notification: order has been placed
notification_order_placed = "Отримано нове замовлення:\n" \
                            "\n" \
                            "{order}"

# Notification: order has been completed
notification_order_completed = "Ваше замовнення успішно завершено!\n" \
                               "\n" \
                               "{order}"

# Notification: order has been refunded
notification_order_refunded = "Ваше замовлення відмінено. Кошти повернуто!\n" \
                              "\n" \
                              "{order}"

# Notification: a manual transaction was applied
notification_transaction_created = "ℹ️  Нова транзакція в вашому гаманці:\n" \
                                   "{transaction}"

# Refund reason
refund_reason = "Причина повернення:\n" \
                "{reason}"

# Info: informazioni sul bot
# bot_info = 'Цей бот використовує <a href="https://github.com/Steffo99/greed">greed</a>,' \
#            ' фреймворк розроблений @Steffo для платежів Телеграм випущений під ліцензією' \
#            ' <a href="https://github.com/Steffo99/greed/blob/master/LICENSE.txt">' \
#            'Affero General Public License 3.0</a>.\n'
#
# # Help: guide
# help_msg = "Інструкція по greed доступна за цією адресою:\n" \
#            "https://github.com/Steffo99/greed/wiki"

# Help: contact shopkeeper
contact_shopkeeper = "Наразі наступні працівники доступні і зможуть допомогти:\n" \
                     "{shopkeepers}\n" \
                     "<i>Виберіть когось одного і напишіть в Телеграм чат.</i>"

# Success: product has been added/edited to the database
success_product_edited = "✅ Продукт успішно створено/оновлено!"

# Success: category has been added/edited to the database
success_category_edited = "✅ Категорія успішно створена/оновлена!"

# Success: category has been added/edited to the database
success_category_deleted = "✅ Категорія успішно видалена!"

# Ask for parent category
ask_category_parent = "Виберіть батьківську категорію для цієї категорії (або 'None' для кореневої категорії):"

# Success: subcategory has been added/edited to the database
success_subcategory_edited = "✅ Підкатегорію успішно створено/оновлено!"

# Menu: add subcategory
menu_add_subcategory = "✨ Нова підкатегорія"

# Admin menu: delete subcategory
menu_delete_subcategory = "❌ Видалити підкатегорію"

# Conversation: select a subcategory to edit
conversation_admin_select_subcategory = "✏️ Яку підкатегорію бажаєте відредагувати?"

# Conversation: select a subcategory to delete
conversation_admin_select_subcategory_to_delete = "❌ Яку підкатегорію бажаєте видалити?"

# Success: product has been marked as deleted in the database
success_product_deleted = "✅ Продукт успішно видалено!"

# Success: order has been created
success_order_created = "✅ Замовлення успішно надіслано!\n" \
                        "\n" \
                        "{order}"

# Success: order was marked as completed
success_order_completed = "✅ Ваше замовлення #{order_id} було успішно проведено."

# Success: order was refunded successfully
success_order_refunded = "✴️ Кошти по замовленню #{order_id} було відшкодовано."

# Success: transaction was created successfully
success_transaction_created = "✅ Транзакцію успішно створено!\n" \
                              "{transaction}"

# Error: message received not in a private chat
error_nonprivate_chat = "⚠️ Цей бот працює тільки в приватних чатах."

# Error: a message was sent in a chat, but no worker exists for that chat.
# Suggest the creation of a new worker with /start
error_no_worker_for_chat = "⚠️ Спілкування з ботом було перервано.\n" \
                           "Щоб почати знову, надішліть боту команду /start "

# Error: add funds amount over max
error_payment_amount_over_max = "⚠️ Максимальна сума однієї транзакції {max_amount}."

# Error: add funds amount under min
error_payment_amount_under_min = "⚠️ Мінімальна сума однієї транзакції {min_amount}."

# Error: the invoice has expired and can't be paid
error_invoice_expired = "⚠️ Час дії інвойсу було вичерпано. Якщо все хочете додати кошти - виберіть Додати" \
                        " кошти в меню."

# Error: a product with that name already exists
error_duplicate_name = "️⚠️ Продукт з таким імʼям вже існує."

cart_subtotal = "Проміжний підсумок"
order_total = "Проміжний підсумок: {subtotal}\nДоставка: {delivery}\nЗагальна сума: {total}"
checkout_cancelled = "Оформлення замовлення скасовано."
error_during_checkout = "Виникла помилка під час оформлення замовлення. Будь ласка, спробуйте ще раз пізніше."
order_confirmation = "Замовлення №{order_id} успішно створено!\nЗагальна сума: {total}\nСпосіб доставки: {delivery_method}"
new_order_notification = "Нове замовлення №{order_id} від користувача {user}"

menu_manage_delivery_and_pickup = "📦 Управління доставкою та самовивозом"
manage_delivery_and_pickup = "Оберіть дію для управління доставкою та самовивозом:"
menu_view_delivery_methods = "👀 Переглянути методи доставки"
menu_view_pickup_points = "👀 Переглянути точки самовивозу"
view_delivery_methods = "Оберіть метод доставки для редагування:"
edit_pickup_point = "Оберіть, що ви хочете змінити:"
edit_pickup_point_address = "Змінити адресу"
edit_pickup_point_description = "Змінити опис"
toggle_pickup_point_status = "Змінити статус (активний/неактивний)"
ask_new_pickup_point_address = "Введіть нову адресу точки самовивозу:"
ask_new_pickup_point_description = "Введіть новий опис точки самовивозу:"
error_pickup_point_not_found = "❌ Точку самовивозу не знайдено."
success_pickup_point_updated = "✅ Точку самовивозу успішно оновлено!"

# Delivery methods
choose_delivery_method = "Оберіть спосіб доставки:"
ask_nova_poshta_info = "Введіть інформацію для доставки Новою Поштою (номер відділення або адресу):"
ask_kyiv_delivery_address = "Введіть адресу доставки по Києву:"
order_success = "Замовлення №{order_id} успішно створено!\nЗагальна сума: {total_cost}\nСпосіб доставки: {delivery_method}"

# Pickup points
ask_pickup_point_address = "Введіть адресу пункту самовивозу:"
ask_pickup_point_description = "Введіть опис пункту самовивозу (або пропустіть цей крок):"
success_pickup_point_added = "✅ Пункт самовивозу успішно додано!"
no_pickup_points = "На даний момент немає активних пунктів самовивозу."
pickup_points_list = "Список пунктів самовивозу:"
menu_add_pickup_point = "📍 Додати пункт самовивозу"
menu_list_pickup_points = "📋 Список пунктів самовивозу"

# Broadcast message
ask_broadcast_message = "Введіть текст повідомлення для розсилки:"
ask_broadcast_image = "Надішліть фото для розсилки (або пропустіть цей крок):"
ask_broadcast_button = "Введіть текст та URL для кнопки у форматі 'текст|url' (або пропустіть цей крок):"
broadcast_complete = "Розсилку завершено. Успішно надіслано: {success_count}/{total_count}"
menu_broadcast_message = "📢 Розіслати повідомлення"

menu_manage_delivery_methods = "📦 Управління методами доставки"
manage_delivery_methods = "Оберіть метод доставки для редагування або додайте новий:"
menu_add_delivery_method = "➕ Додати новий метод доставки"
ask_delivery_method_name = "Введіть назву нового методу доставки:"
ask_delivery_method_price = "Введіть ціну доставки (в мінімальних одиницях валюти):"
success_delivery_method_added = "✅ Новий метод доставки успішно додано!"
error_delivery_method_not_found = "❌ Метод доставки не знайдено."
edit_delivery_method = "Оберіть, що ви хочете змінити:"
edit_delivery_method_name = "Змінити назву"
edit_delivery_method_price = "Змінити ціну"
toggle_delivery_method_status = "Змінити статус (активний/неактивний)"
ask_new_delivery_method_name = "Введіть нову назву методу доставки:"
ask_new_delivery_method_price = "Введіть нову ціну доставки (в мінімальних одиницях валюти):"
success_delivery_method_updated = "✅ Метод доставки успішно оновлено!"

# Error: not enough credit to order
error_not_enough_credit = "⚠️ У вас недостатньо коштів, щоб виконати замовлення."

# Error: order has already been cleared
error_order_already_cleared = "⚠️  Це замовлення вже було опрацьовано раніше."

# Error: no orders have been placed, so none can be shown
error_no_orders = "⚠️  Ви ще не зробили жодного замовлення, тому тут пусто."

# Error: selected user does not exist
error_user_does_not_exist = "⚠️  Такого користувача не існує."

# Fatal: conversation raised an exception
fatal_conversation_exception = "☢️ Ой лишенько! <b>Помилка</b> перервала нашу розмову\n" \
                               "Про помилку було повідомлено власника бота.\n" \
                               "Щоб почати розмову знову, надішліть команду /start."