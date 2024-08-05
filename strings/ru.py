# Строки / файл локализации для greed
# Можно редактировать, но НЕ УДАЛЯЙТЕ ПОЛЯ ЗАМЕНЫ (слова, окруженные {фигурными скобками})

currency_symbol = "₽"

order_number = "Заказ #{id}"

loading_transactions = "<i>Загружаю транзакции...\n" \
                       "Подождите несколько секунд.</i>"

transactions_page = "Страница <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

csv_caption = "Файл 📄 .csv, содержащий все транзакции из базы данных бота, был сгенерирован.\n" \
              "Вы можете открыть файл с помощью LibreOffice Calc, чтобы просмотреть детали."

conversation_after_start = "Добрый день 🙏🏾\nДобро пожаловать в магазинчик Grace Glade🎅🏽🍄"

conversation_open_user_menu = "Что бы вы хотели сделать?\n" \
                              "💰 У вас <b>{credit}</b> в кошельке.\n" \
                              "\n" \
                              "<i>Выберите опцию из вариантов на клавиатуре.\n" \
                              "Если клавиатура не видна - ее можно активировать кнопкой с четырьмя квадратами внизу</i>."

profile_info = "ID: {id}\nИмя: {name}\nБаланс: {balance}\nС нами: {time_with_us}"
day = "день"
days_2_4 = "дня"
days_many = "дней"

ask_number_of_buttons = "Сколько кнопок вы хотите добавить к сообщению? (от 0 до 6)"

invalid_number_of_buttons = "Неверное количество кнопок. Пожалуйста, введите число от 0 до 6."

error_cart_menu = "Произошла ошибка при обработке корзины. Пожалуйста, попробуйте еще раз или обратитесь к администратору."

error_no_deposits_for_promocode = "⚠️ Для использования промокода необходимо сначала пополнить счет бота. Пожалуйста, пополните счет и попробуйте снова."
promocode_already_used = "Вы уже использовали этот промокод."
promocode_expired = "Этот промокод больше не доступен."
promocode_applied = "Промокод применен! Добавлено {amount} к вашему балансу."
error_applying_promocode = "Произошла ошибка при применении промокода. Попробуйте еще раз позже."

ask_product_name = "Введите название продукта:"
edit_current_value = "Текущее значение: {value}"
error_duplicate_name = "Продукт с таким названием уже существует. Пожалуйста, выберите другое название."

conversation_admin_product_menu = "Меню управления продуктами. Выберите действие:"
menu_add_product = "➕ Добавить новый продукт"
menu_edit_product = "✏️ Редактировать продукт"
menu_delete_product = "🗑️ Удалить продукт"
conversation_admin_select_product_to_edit = "Выберите продукт для редактирования:"

menu_edit_cart = "✏️ Редактировать корзину"
cart_edit_header = "Редактирование корзины:"

success_product_edited = "✅ Товар успешно отредактирован!"

ask_button_text = "Введите текст для кнопки {button_number}:"

ask_button_url = "Введите URL для кнопки {button_number} (должен начинаться с http:// или https://):"

checkout_canceled = "Оформление заказа отменено."

menu_cart = "🛒 Корзина"
cart_empty = "Ваша корзина пуста."
cart_contents = "Содержимое корзины:"
cart_total = "Общая сумма:"
cart_cleared = "Корзина очищена."

menu_go_to_cart = "🛒 Перейти в корзину"
menu_main_menu = "🏠 Главное меню"

add_funds = "💰 Пополнить кошелек"
return_to_main_menu = "🏠 Вернуться в главное меню"

insufficient_funds = ("К сожалению, на вашем балансе недостаточно средств для оформления заказа.\nОбщая сумма: {"
                      "total}\nВаш баланс: {balance}\nНе хватает: {shortage}\nПожалуйста, пополните баланс и "
                      "попробуйте снова.")

ask_broadcast_message = "Введите текст сообщения для рассылки:"
ask_broadcast_image = "Хотите добавить изображение к сообщению?"
send_broadcast_image = "Пожалуйста, отправьте изображение для рассылки."
confirm_broadcast = "Вы уверены, что хотите разослать это сообщение всем пользователям?"
broadcast_canceled = "Рассылка отменена."
broadcast_complete = "Рассылка завершена. Успешно отправлено: {success_count}/{total_count}"
yes = "Да"
no = "Нет"

confirm_delete_category = "Вы уверены, что хотите удалить категорию {category}?"
confirm_delete_subcategory = "Вы уверены, что хотите удалить подкатегорию {subcategory}?"
menu_confirm = "✅ Подтвердить"
deletion_canceled = "Удаление отменено."

ask_category_image = "Отправьте фото для категории (или нажмите 'Пропустить'):"
menu_skip = "⏭ Пропустить"
order_canceled = "Заказ отменен. Корзина очищена."
select_category_for_product = "Выберите категорию для продукта:"

menu_add_subcategory = "➕ Добавить подкатегорию"
menu_edit_category = "✏️ Редактировать категорию"
menu_view_subcategories = "👁️ Просмотреть подкатегории"
category_action_prompt = "Выберите действие для категории:"
ask_category_name = "Введите название категории:"
ask_category_description = "Введите описание категории (или пропустите этот шаг):"
category_deleted = "Категория успешно удалена."
category_not_found = "Категория не найдена."

product_price = "Цена"
product_in_cart = "В корзине"
product_pieces = "шт."
product_subtotal = "Сумма в корзине"
product_added_to_cart = "Товар добавлен в корзину"
product_removed_from_cart = "Товар удален из корзины"
menu_add_to_cart = "➕ Добавить в корзину"
menu_remove_from_cart = "➖ Удалить из корзины"

post_order_options = "Что бы вы хотели сделать дальше?"
continue_shopping = "🛒 Продолжить покупки"
no_categories_to_delete = "Нет категорий для удаления."
no_subcategories_to_delete = "Нет подкатегорий для удаления."
select_category_to_delete = "Выберите категорию для удаления:"
select_subcategory_to_delete = "Выберите подкатегорию для удаления:"
subcategory_deleted = "Подкатегория успешно удалена."
subcategory_not_found = "Подкатегория не найдена."

choose_pickup_point = "Выберите пункт самовывоза:"
error_no_pickup_points = "К сожалению, сейчас нет доступных пунктов самовывоза. Пожалуйста, выберите другой способ доставки."
ask_nova_poshta_city = "Введите город доставки:"
ask_nova_poshta_office = "Введите номер отделения Новой почты:"
ask_nova_poshta_phone = "Введите ваш номер телефона:"
ask_nova_poshta_name = "Введите ваше ФИО:"
ask_kyiv_address = "Введите адрес доставки в Киеве:"
ask_kyiv_phone = "Введите ваш номер телефона для связи:"
error_checkout_canceled = "Оформление заказа отменено. Пожалуйста, попробуйте еще раз или обратитесь в службу поддержки."

conversation_open_admin_menu = "Вы являетесь 💼 <b>Менеджером</b> этого магазина!\n" \
                               "Что бы вы хотели сделать?\n" \
                               "\n" \
                               "<i>Выберите опцию из вариантов на клавиатуре.\n" \
                               "Если клавиатура не видна - ее можно активировать кнопкой с четырьмя квадратами внизу</i>."

conversation_payment_method = "Как бы Вы хотели пополнить кошелек?"

menu_edit_admins = "👥 Редактировать менеджеров"

admin_properties = "<b>Права доступа для {name}:</b>"
prop_edit_products = "Редактировать товары"
prop_edit_categories = "Редактировать категории"
prop_edit_subcategories = "Редактировать подкатегории"
prop_receive_orders = "Получать заказы"
prop_create_transactions = "Создавать транзакции"
prop_display_on_help = "Отображать в справке"

conversation_confirm_admin_promotion = "Вы уверены, что хотите предоставить этому пользователю права менеджера?"

promocode_management_menu = "Выберите действие для управления промокодами:"
menu_manage_promocodes = "🎟 Управление промокодами"
menu_delete_promocode = "🗑 Удалить промокод"
choose_promocode_type = "Выберите тип промокода:"
choose_amount_type = "Выберите тип суммы:"
ask_fixed_amount = "Введите фиксированную сумму:"
ask_min_amount = "Введите минимальную сумму:"
ask_max_amount = "Введите максимальную сумму:"
ask_uses_number = "Введите количество возможных активаций:"
promocode_created_qr = "QR-код создан: {code}\nСсылка: {link}"
promocode_created_text = "Промокод создан: {code}"
promocode_info = "Код: {code}\nТип: {type}\nСумма: {amount}\nОсталось активаций: {uses_left}/{total_uses}\nСоздан: {creator}\nИспользован: {used_count} раз\nОбщая сумма: {total_amount}"
no_active_promocodes = "Нет активных промокодов."
text_promocode = "Текстовый"
no_promocodes_to_delete = "Нет промокодов для удаления."
choose_promocode_to_delete = "Выберите промокод для удаления:"
promocode_deleted = "Промокод {code} удален."
promocode_not_found = "Промокод не найден."

conversation_admin_select_product_to_delete = "❌ Какой продукт нужно удалить?"

cancel_order = "❌ Отменить заказ"
confirm = "✅ Подтвердить"
confirm_delivery_method = "Вы выбрали способ доставки: {method}\nЦена доставки: {price}\nИнформация: {info}\n\nПодтвердите ваш выбор:"
or_press_back = "Или нажмите 'Назад', чтобы вернуться"

conversation_admin_select_user = "Выберите пользователя для редактирования."

conversation_cart_actions = "<i>Добавьте продукты в корзину нажатием кнопки Добавить." \
                            "  Когда сделаете Ваш выбор, вернитесь к этому сообщению" \
                            " и нажмите кнопку Готово.</i>"

conversation_confirm_cart = "🛒 У вас в корзине следующие продукты:\n" \
                            "{product_list}" \
                            "Всего: <b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>Чтобы продолжить нажмите Готово.\n" \
                            "Если передумали - выбирайте Отмена.</i>"

conversation_live_orders_start = "Вы в режиме <b>Свежие Заказы</b>\n" \
                                 "Все новые заказы от покупателей появятся в этом чате в режиме реального времени," \
                                 " и вы сможете отмечать их ✅ Выполнено" \
                                 " или ✴️ Вернуть деньги покупателю."

conversation_live_orders_stop = "<i>Нажмите кнопку Стоп в этом чате, чтобы остановить этот режим.</i>"

conversation_open_help_menu = "Как можем Вам помочь?"

conversation_language_select = "Выберите язык:"

conversation_switch_to_user_mode = " Вы перешли в режим 👤 Заказчика.\n" \
                                   "Если хотите вернуться в меню 💼 Менеджера, перезапустите разговор с /start."

conversation_expired = "🕐  За долгое время я не получил ни одного сообщения, поэтому я завершил разговор" \
                       " чтобы сохранить ресурсы.\n" \
                       "Чтобы начать снова, отправьте команду /start ."

conversation_admin_select_category = "✏️ Какую категорию хотите отредактировать"

ask_subcategory_name = "Введите название подкатегории:"

ask_parent_category = "Выберите родительскую категорию для новой подкатегории:"

error_no_root_categories = "Ошибка: нет ни одной корневой категории. Сначала создайте корневую категорию."

success_category_created = "✅ Категория успешно создана!"

success_subcategory_created = "✅ Подкатегория успешно создана!"

ask_subcategory_description = "Введите описание подкатегории (или пропустите этот шаг):"

ask_subcategory_image = "Отправьте изображение для подкатегории (или пропустите этот шаг):"

conversation_select_category = "Выберите категорию"

conversation_order_category = "Выберите категорию:"

error_product_not_found = "Товар не найден."

menu_back = "⬅️ Назад"
menu_checkout = "💳 Оформить заказ"
menu_clear_cart = "🗑️ Очистить корзину"

menu_credit_history = "📈 История пополнения"

menu_promocode = "🤩 Ввести промокод"

ask_promocode = "Введите промокод:"

menu_order = "🛒 Товары"

menu_uncategorized = "Без категории"

menu_go_back = "🔙 Вернуться"

menu_order_status = "🛍 Мои заказы"

menu_add_credit = "💵 Пополнить кошелек"

menu_profile = "🧾 Профиль"

menu_create_promocode = "Создать промокод/QR-код"

menu_list_promocodes = "Статистика промокодов"

credit_history_null = "У вас еще не было пополнений!"

credit_history = "История Ваших пополнений:"

menu_cash = "💵 Наличными"

menu_credit_card = "💳 Кредитной картой"

menu_products = "📝️ Продукты"

menu_orders = "📦 Заказы"

menu_transactions = "💳 Список транзакций"

menu_edit_credit = "💰 Создать транзакцию"

menu_user_mode = "👤 Режим заказчика"

menu_cancel = "🔙 Отмена"

menu_done = "✅️ Готово"

menu_categories = "📝️ Категории"

menu_add_category = "✨ Новая категория"

menu_delete_category = "❌ Удалить категорию"

menu_pay = "💳 Оплатить"

menu_complete = "✅ Готово"

menu_refund = "✴️ Возврат средств"

menu_stop = "🛑 Стоп"

menu_all_products = "Все товары"

menu_help = "❓ Помощь"

menu_guide = "📖 Инструкция"

menu_promo_text = "Текстовый"

menu_promo_qr = "QR-код"

menu_promo_fixed = "Фиксированная"

menu_promo_range = "Диапазон"

menu_next = "▶️ Следующая"

menu_previous = "◀️ Предыдущая"

menu_contact_shopkeeper = "👨‍💼 Контакты магазина"

menu_csv = "📄 .csv"

menu_language = "🇷🇺 Язык"

emoji_yes = "✅"

emoji_no = "🚫"

ask_product_description = "Каким будет описание продукта?"

ask_product_price = "Какая будет цена?\n" \
                    "Введите <code>X</code> Если продукт сейчас не продается."

ask_product_image = "🖼 Какую картинку добавить к продукту?\n" \
                    "\n" \
                    "<i>Отправьте фото, или Пропустите этот шаг.</i>"

ask_order_notes = "Оставить сообщение вместе с этой покупкой?\n" \
                  "💼 Сообщение будет доступно Менеджеру магазина.\n" \
                  "\n" \
                  "<i>Отправьте Ваше сообщение, или нажмите Пропустить" \
                  " чтобы не оставлять сообщение.</i>"

ask_refund_reason = " Напишите причину возврата средств.\n" \
                    "👤  Причина будет доступна заказчику."

ask_transaction_notes = " Добавьте сообщение к транзакции.\n" \
                        "👤 Сообщение будет доступно заказчику после пополнения/списания" \
                        " и 💼 Администратору в логах транзакций."

ask_credit = "Как вы хотите изменить баланс заказчика?\n" \
             "\n" \
             "<i>Отправьте сообщение с суммой.\n" \
             "Используйте  </i><code>+</code><i> чтобы пополнить счет," \
             " и знак </i><code>-</code><i> чтобы списать средства.</i>"

downloading_image = "Я загружаю фото!\n" \
                    "Может занять некоторое время... Имейте терпение!\n" \
                    "Я не смогу отвечать, пока идет загрузка."

payment_cash = "Вы можете пополнить наличными прямо в магазине.\n" \
               "Рассчитайтесь и дайте этот id менеджеру:\n" \
               "<b>{user_cash_id}</b>"

payment_cc_amount = "На какую сумму вы хотите пополнить кошелек?\n" \
                    "\n" \
                    "<i>Выберите сумму из предложенных значений, или введите вручную в сообщении.</i>"

payment_invoice_title = "Пополнение"

payment_invoice_description = "Оплата этого счета добавит {amount} в ваш кошелек."

payment_invoice_label = "Платеж"

payment_invoice_fee_label = "Оплата за пополнение"

notification_order_placed = "Получен новый заказ:\n" \
                            "\n" \
                            "{order}"

notification_order_completed = "Ваш заказ успешно завершен!\n" \
                               "\n" \
                               "{order}"

notification_order_refunded = "Ваш заказ отменен. Средства возвращены!\n" \
                              "\n" \
                              "{order}"

notification_transaction_created = "ℹ️  Новая транзакция в вашем кошельке:\n" \
                                   "{transaction}"

contact_shopkeeper = "В настоящее время следующие сотрудники доступны и смогут помочь:\n" \
                     "{shopkeepers}\n" \
                     "<i>Выберите кого-нибудь одного и напишите в Телеграм чат.</i>"

success_category_edited = "✅ Категория успешно создана/обновлена!"

ask_category_parent = "Выберите родительскую категорию для этой категории (или 'None' для корневой категории):"

success_product_deleted = "✅ Продукт успешно удален!"

success_order_created = "✅ Заказ успешно отправлен!\n" \
                        "\n" \
                        "{order}"

success_order_refunded = "✴️ Средства по заказу #{order_id} были возмещены."

success_transaction_created = "✅ Транзакция успешно создана!\n" \
                              "{transaction}"

error_payment_amount_over_max = "⚠️ Максимальная сумма одной транзакции {max_amount}."

error_payment_amount_under_min = "⚠️ Минимальная сумма одной транзакции {min_amount}."

error_during_checkout = "Произошла ошибка во время оформления заказа. Пожалуйста, попробуйте еще раз позже."
order_confirmation = "Заказ №{order_id} успешно создан!\nОбщая сумма: {total}\nСпособ доставки: {delivery_method}"
manage_delivery_and_pickup = "Выберите действие для управления доставкой и самовывозом:"
menu_view_delivery_methods = "👀 Просмотреть методы доставки"
menu_view_pickup_points = "👀 Просмотреть пункты самовывоза"
view_delivery_methods = "Выберите метод доставки для редактирования:"
edit_pickup_point = "Выберите, что вы хотите изменить:"
edit_pickup_point_address = "Изменить адрес"
edit_pickup_point_description = "Изменить описание"
toggle_pickup_point_status = "Изменить статус (активный/неактивный)"
ask_new_pickup_point_address = "Введите новый адрес пункта самовывоза:"
ask_new_pickup_point_description = "Введите новое описание пункта самовывоза:"
error_pickup_point_not_found = "❌ Пункт самовывоза не найден."
success_pickup_point_updated = "✅ Пункт самовывоза успешно обновлен!"

choose_delivery_method = "Выберите способ доставки:"
ask_pickup_point_address = "Введите адрес пункта самовывоза:"
ask_pickup_point_description = "Введите описание пункта самовывоза (или пропустите этот шаг):"
success_pickup_point_added = "✅ Пункт самовывоза успешно добавлен!"
no_pickup_points = "На данный момент нет активных пунктов самовывоза."
pickup_points_list = "Список пунктов самовывоза:"
menu_add_pickup_point = "📍 Добавить пункт самовывоза"
menu_broadcast_message = "📢 Разослать сообщение"

menu_add_delivery_method = "➕ Добавить новый метод доставки"
ask_delivery_method_name = "Введите название нового метода доставки:"
ask_delivery_method_price = "Введите цену доставки (в минимальных единицах валюты):"
success_delivery_method_added = "✅ Новый метод доставки успешно добавлен!"
error_delivery_method_not_found = "❌ Метод доставки не найден."
edit_delivery_method = "Выберите, что вы хотите изменить:"
edit_delivery_method_name = "Изменить название"
edit_delivery_method_price = "Изменить цену"
toggle_delivery_method_status = "Изменить статус (активный/неактивный)"
ask_new_delivery_method_name = "Введите новое название метода доставки:"
ask_new_delivery_method_price = "Введите новую цену доставки (в минимальных единицах валюты):"
success_delivery_method_updated = "✅ Метод доставки успешно обновлен!"

error_not_enough_credit = "⚠️ У вас недостаточно средств, чтобы выполнить заказ."

error_order_already_cleared = "⚠️  Этот заказ уже был обработан ранее."

error_no_orders = "⚠️  Вы еще не сделали ни одного заказа, поэтому здесь пусто."

error_user_does_not_exist = "⚠️  Такого пользователя не существует."

fatal_conversation_exception = "☢️ Ой-ой! <b>Ошибка</b> прервала наш разговор\n" \
                               "Об ошибке было сообщено владельцу бота.\n" \
                               "Чтобы начать разговор заново, отправьте команду /start."
help_msg = ""

error_no_delivery_methods = "Сейчас нет активных методов доставки."

error_listing_promocodes = "Возникла ошибка при просмотре промокодов."

invalid_promocode = "Неверный промокод"

bot_info = ""