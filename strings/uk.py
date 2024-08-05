# Strings / localization file for greed
# Can be edited, but DON'T REMOVE THE REPLACEMENT FIELDS (words surrounded by {curly braces})

currency_symbol = "₴"

currency_format_string = "{value} {symbol}"

order_number = "Замовлення #{id}"

loading_transactions = "<i>Завантажую транзакції...\n" \
                       "Зачекайте кілька секунд.</i>"

transactions_page = "Сторінка <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

csv_caption = "Файл 📄 .csv, який має всі транзакції з бази даних бота було сгенеровано.\n" \
              "Можете відкрити файл за допомогою LibreOffice Calc, щоб переглянути деталі."

conversation_after_start = "Доброго дня 🙏🏾\nВітаємо у крамничці Grace Glade🎅🏽🍄"

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

error_cart_menu = "Виникла помилка при обробці кошика. Будь ласка, спробуйте ще раз або зверніться до адміністратора."

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

menu_edit_cart = "✏️ Редагувати кошик"
cart_edit_header = "Редагування кошика:"

success_product_edited = "✅ Товар успішно відредаговано!"

ask_button_text = "Введіть текст для кнопки {button_number}:"

ask_button_url = "Введіть URL для кнопки {button_number} (має починатися з http:// або https://):"

checkout_canceled = "Оформлення замовлення скасовано."

menu_cart = "🛒 Кошик"
cart_empty = "Ваш кошик порожній."
cart_contents = "Вміст кошика:"
cart_total = "Загальна сума:"
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
send_broadcast_image = "Будь ласка, надішліть зображення для розсилки."
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
order_canceled = "Замовлення скасовано. Кошик очищено."
select_category_for_product = "Виберіть категорію для продукту:"

menu_add_subcategory = "➕ Додати підкатегорію"
menu_edit_category = "✏️ Редагувати категорію"
menu_view_subcategories = "👁️ Переглянути підкатегорії"
category_action_prompt = "Оберіть дію для категорії:"
ask_category_name = "Введіть назву категорії:"
ask_category_description = "Введіть опис категорії (або пропустіть цей крок):"
category_deleted = "Категорію успішно видалено."
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
no_categories_to_delete = "Немає категорій для видалення."
no_subcategories_to_delete = "Немає підкатегорій для видалення."
select_category_to_delete = "Виберіть категорію для видалення:"
select_subcategory_to_delete = "Виберіть підкатегорію для видалення:"
subcategory_deleted = "Підкатегорію успішно видалено."
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

conversation_open_admin_menu = "Ви є 💼 <b>Менеджером</b> цього магазину!\n" \
                               "Що б ви хотіли зробити?\n" \
                               "\n" \
                               "<i>Виберіть опцію з варіантів на клавіатурі.\n" \
                               "Якщо клавіатури не видно - її можна активувати кнопкою з чотирма квадратами внизу</i>."

conversation_payment_method = "Як би Ви хотіли поповнити гаманець?"

menu_edit_admins = "👥 Редагувати менеджерів"

admin_properties = "<b>Права доступу для {name}:</b>"
prop_edit_products = "Редагувати товари"
prop_edit_categories = "Редагувати категорії"
prop_edit_subcategories = "Редагувати підкатегорії"
prop_receive_orders = "Отримувати замовлення"
prop_create_transactions = "Створювати транзакції"
prop_display_on_help = "Відображати в довідці"

conversation_confirm_admin_promotion = "Ви впевнені, що хочете надати цьому користувачу права менеджера?"

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
no_promocodes_to_delete = "Немає промокодів для видалення."
choose_promocode_to_delete = "Оберіть промокод для видалення:"
promocode_deleted = "Промокод {code} видалено."
promocode_not_found = "Промокод не знайдено."

conversation_admin_select_product_to_delete = "❌ Який продукт потрібно видалит?"

cancel_order = "❌ Скасувати замовлення"
confirm = "✅ Підтвердити"
confirm_delivery_method = "Ви обрали спосіб доставки: {method}\nЦіна доставки: {price}\nІнформація: {info}\n\nПідтвердіть ваш вибір:"
or_press_back = "Або натисніть 'Назад', щоб повернутися"

conversation_admin_select_user = "Виберіть користувача для редагування."

conversation_cart_actions = "<i>Додайте продукти в кошик натисканням кнопки Додати." \
                            "  Коли зробите Ваш вибір, повертайтесь до цього повідомлення" \
                            " і натисніть кнопку Готово.</i>"

conversation_confirm_cart = "🛒 У вас в кошику наступні продукти:\n" \
                            "{product_list}" \
                            "Всього: <b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>Щоб продовжити натисніть Готово.\n" \
                            "Якщо змінили свою думку - обирайте Відміна.</i>"

conversation_live_orders_start = "Ви в режимі <b>Свіжі Замовлення</b>\n" \
                                 "Всі нові замовення від покупців зʼявляться в цьому чаті в режимі живого часу," \
                                 " і ви зможете помічати їх ✅ Виконано" \
                                 " або ✴️ Повернути кошти покупцю."

conversation_live_orders_stop = "<i>Натисніть кнопку Стоп в цьому чаті, щоб зупинити цей режим.</i>"

conversation_open_help_menu = "Як можемо Вам допомогти?"

conversation_language_select = "Оберіть мову:"

conversation_switch_to_user_mode = " Ви перейшли в режим 👤 Замовника.\n" \
                                   "Якщо хочете повернутись в меню 💼 Менеджера, рестартуйте розмову з /start."

conversation_expired = "🕐  За довгий час я не отримав жодного повідомлення, тому я завершив розмову" \
                       " щоб зберегти ресурси.\n" \
                       "Щоб почату знову, надішліть команду /start ."

conversation_admin_select_category = "✏️ Яку категорію бажаєте відредагувати"

ask_subcategory_name = "Введіть назву підкатегорії:"

ask_parent_category = "Виберіть батьківську категорію для нової підкатегорії:"

error_no_root_categories = "Помилка: немає жодної кореневої категорії. Спочатку створіть кореневу категорію."

success_category_created = "✅ Категорію успішно створено!"

success_subcategory_created = "✅ Підкатегорію успішно створено!"

ask_subcategory_description = "Введіть опис підкатегорії (або пропустіть цей крок):"

ask_subcategory_image = "Надішліть зображення для підкатегорії (або пропустіть цей крок):"

conversation_select_category = "Оберіть категорію"

conversation_order_category = "Оберіть категорію:"

error_product_not_found = "Товар не знайдено."

menu_back = "⬅️ Назад"
menu_checkout = "💳 Оформити замовлення"
menu_clear_cart = "🗑️ Очистити кошик"

menu_credit_history = "📈 Історія поповнення"

menu_promocode = "🤩 Ввести промокод"

ask_promocode = "Введіть промокод:"

menu_order = "🛒 Товари"

menu_uncategorized = "Без категорії"

menu_go_back = "🔙 Повернутися"

menu_order_status = "🛍 Мої замовлення"

menu_add_credit = "💵 Поповнити гаманець"

menu_profile = "🧾 Профіль"

menu_create_promocode = "Створити промокод/QR-код"

menu_list_promocodes = "Статистика промокодів"

credit_history_null = "У вас ще не було поповнень!"

credit_history = "Історія Ваших поповнень:"

menu_cash = "💵 Готівкою"

menu_credit_card = "💳 Кредитною картою"

menu_products = "📝️ Продукти"

menu_orders = "📦 Замовлення"

menu_transactions = "💳 Список транзакцій"

menu_edit_credit = "💰 Створити транзакцію"

menu_user_mode = "👤 Режим замовника"

menu_cancel = "🔙 Відміна"

menu_done = "✅️ Готово"

menu_categories = "📝️ Категорії"

menu_add_category = "✨ Нова категорія"

menu_delete_category = "❌ Видалити категорію"

menu_pay = "💳 Заплатити"

menu_complete = "✅ Готово"

menu_refund = "✴️ Повернення коштів"

menu_stop = "🛑 Стоп"

menu_all_products = "Всі товари"

menu_help = "❓ Допомога"

menu_guide = "📖 Інструкція"

menu_promo_text = "Текстовий"

menu_promo_qr = "QR-код"

menu_promo_fixed = "Фіксована"

menu_promo_range = "Діапазон"

menu_next = "▶️ Наступна"

menu_previous = "◀️ Попередня"

menu_contact_shopkeeper = "👨‍💼 Контакти магазину"

menu_csv = "📄 .csv"

menu_language = "🇺🇦 Мова"

emoji_yes = "✅"

emoji_no = "🚫"

ask_product_description = "Який буде опис продукту?"

ask_product_price = "Яка буде ціна?\n" \
                    "Введіть <code>X</code> Якщо продукт зараз не продається."

ask_product_image = "🖼 Яку картинку додати до продукта?\n" \
                    "\n" \
                    "<i>Надішліть фото, або Пропустіть цей крок.</i>"

ask_order_notes = "Залишити повідомлення разом з цією покупкою?\n" \
                  "💼 Повідомлення буде доступне Менеджеру магазину.\n" \
                  "\n" \
                  "<i>Надішліть Ваше повідомлення, або натисність Пропустити" \
                  " щоб не залишати повідомлення.</i>"

ask_refund_reason = " Напишіть причину повернення коштів.\n" \
                    "👤  Причина буде доступна замовнику."

ask_transaction_notes = " Додайте повідомлення до транзакції.\n" \
                        "👤 Повідомлення буде доступне замовнику після поповнення/списання" \
                        " і 💼 Адміністратору в логах транзакцій."

# Edit credit: amount?
ask_credit = "Як ви хочете змінити баланс замовника?\n" \
             "\n" \
             "<i>Надішліть повідомлення з сумою.\n" \
             "Використовуйте  </i><code>+</code><i> щоб поповнити рахунок," \
             " і знак </i><code>-</code><i> щоб списати кошти.</i>"

downloading_image = "Я завантажую фото!\n" \
                    "Може зайняти деякий час... Майте терпіння!\n" \
                    "Я не зможу відповідати, поки йде завантаження."

payment_cash = "Ви можете поповнити готівкою прямо в магазині.\n" \
               "Розрахуйтесь і дайте цей id менеджеру:\n" \
               "<b>{user_cash_id}</b>"

payment_cc_amount = "На яку сумму ви хочете поповнити гаманець?\n" \
                    "\n" \
                    "<i>Виберіть сумму із запропонованих значень, або введіть вручну в повідомленні.</i>"

payment_invoice_title = "Поповнення"

payment_invoice_description = "Оплата цього рахунку додасть {amount} в ваш гаманець."

payment_invoice_label = "Платіж"

payment_invoice_fee_label = "Оплата за поповнення"

notification_order_placed = "Отримано нове замовлення:\n" \
                            "\n" \
                            "{order}"

notification_order_completed = "Ваше замовнення успішно завершено!\n" \
                               "\n" \
                               "{order}"

notification_order_refunded = "Ваше замовлення відмінено. Кошти повернуто!\n" \
                              "\n" \
                              "{order}"

notification_transaction_created = "ℹ️  Нова транзакція в вашому гаманці:\n" \
                                   "{transaction}"

contact_shopkeeper = "Наразі наступні працівники доступні і зможуть допомогти:\n" \
                     "{shopkeepers}\n" \
                     "<i>Виберіть когось одного і напишіть в Телеграм чат.</i>"

success_category_edited = "✅ Категорія успішно створена/оновлена!"

ask_category_parent = "Виберіть батьківську категорію для цієї категорії (або 'None' для кореневої категорії):"

success_product_deleted = "✅ Продукт успішно видалено!"

success_order_created = "✅ Замовлення успішно надіслано!\n" \
                        "\n" \
                        "{order}"

success_order_refunded = "✴️ Кошти по замовленню #{order_id} було відшкодовано."

success_transaction_created = "✅ Транзакцію успішно створено!\n" \
                              "{transaction}"

error_payment_amount_over_max = "⚠️ Максимальна сума однієї транзакції {max_amount}."

error_payment_amount_under_min = "⚠️ Мінімальна сума однієї транзакції {min_amount}."

error_during_checkout = "Виникла помилка під час оформлення замовлення. Будь ласка, спробуйте ще раз пізніше."
order_confirmation = "Замовлення №{order_id} успішно створено!\nЗагальна сума: {total}\nСпосіб доставки: {delivery_method}"
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

choose_delivery_method = "Оберіть спосіб доставки:"
ask_pickup_point_address = "Введіть адресу пункту самовивозу:"
ask_pickup_point_description = "Введіть опис пункту самовивозу (або пропустіть цей крок):"
success_pickup_point_added = "✅ Пункт самовивозу успішно додано!"
no_pickup_points = "На даний момент немає активних пунктів самовивозу."
pickup_points_list = "Список пунктів самовивозу:"
menu_add_pickup_point = "📍 Додати пункт самовивозу"
menu_broadcast_message = "📢 Розіслати повідомлення"

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

error_not_enough_credit = "⚠️ У вас недостатньо коштів, щоб виконати замовлення."

error_order_already_cleared = "⚠️  Це замовлення вже було опрацьовано раніше."

error_no_orders = "⚠️  Ви ще не зробили жодного замовлення, тому тут пусто."

error_user_does_not_exist = "⚠️  Такого користувача не існує."

fatal_conversation_exception = "☢️ Ой лишенько! <b>Помилка</b> перервала нашу розмову\n" \
                               "Про помилку було повідомлено власника бота.\n" \
                               "Щоб почати розмову знову, надішліть команду /start."
help_msg = ""

error_no_delivery_methods = "Зараз немає активних методів доставки."

error_listing_promocodes = "Виникла помилка під час перегляду промокодів."

invalid_promocode = "Не вірний промокод"

bot_info = ""
