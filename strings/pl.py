# Ciągi znaków / plik lokalizacyjny dla greed
# Można edytować, ale NIE USUWAJ PÓL ZAMIENNYCH (słów otoczonych {nawiasami klamrowymi})

currency_symbol = "zł"

order_number = "Zamówienie #{id}"

loading_transactions = "<i>Ładowanie transakcji...\n" \
                       "Proszę poczekać kilka sekund.</i>"

transactions_page = "Strona <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

csv_caption = "Wygenerowano plik 📄 .csv zawierający wszystkie transakcje z bazy danych bota.\n" \
              "Możesz otworzyć plik za pomocą LibreOffice Calc, aby zobaczyć szczegóły."

conversation_after_start = "Dzień dobry 🙏🏾\nWitamy w sklepiku Grace Glade🎅🏽🍄"

conversation_open_user_menu = "Co chciałbyś zrobić?\n" \
                              "💰 Masz <b>{credit}</b> w portfelu.\n" \
                              "\n" \
                              "<i>Wybierz opcję z klawiatury.\n" \
                              "Jeśli klawiatura nie jest widoczna, możesz ją aktywować przyciskiem z czterema kwadratami na dole</i>."

profile_info = "ID: {id}\nImię: {name}\nSaldo: {balance}\nZ nami od: {time_with_us}"
day = "dzień"
days_2_4 = "dni"
days_many = "dni"

ask_number_of_buttons = "Ile przycisków chcesz dodać do wiadomości? (od 0 do 6)"

invalid_number_of_buttons = "Nieprawidłowa liczba przycisków. Proszę wpisać liczbę od 0 do 6."

error_cart_menu = "Wystąpił błąd podczas przetwarzania koszyka. Spróbuj ponownie lub skontaktuj się z administratorem."

error_no_deposits_for_promocode = "⚠️ Aby użyć kodu promocyjnego, musisz najpierw doładować konto bota. Proszę doładować konto i spróbować ponownie."
promocode_already_used = "Już użyłeś tego kodu promocyjnego."
promocode_expired = "Ten kod promocyjny nie jest już dostępny."
promocode_applied = "Kod promocyjny zastosowany! Dodano {amount} do twojego salda."
error_applying_promocode = "Wystąpił błąd podczas stosowania kodu promocyjnego. Spróbuj ponownie później."

ask_product_name = "Wprowadź nazwę produktu:"
edit_current_value = "Aktualna wartość: {value}"
error_duplicate_name = "Produkt o tej nazwie już istnieje. Proszę wybrać inną nazwę."

conversation_admin_product_menu = "Menu zarządzania produktami. Wybierz akcję:"
menu_add_product = "➕ Dodaj nowy produkt"
menu_edit_product = "✏️ Edytuj produkt"
menu_delete_product = "🗑️ Usuń produkt"
conversation_admin_select_product_to_edit = "Wybierz produkt do edycji:"

menu_edit_cart = "✏️ Edytuj koszyk"
cart_edit_header = "Edycja koszyka:"

success_product_edited = "✅ Produkt został pomyślnie edytowany!"

ask_button_text = "Wprowadź tekst dla przycisku {button_number}:"

ask_button_url = "Wprowadź URL dla przycisku {button_number} (musi zaczynać się od http:// lub https://):"

checkout_canceled = "Anulowano finalizację zamówienia."

menu_cart = "🛒 Koszyk"
cart_empty = "Twój koszyk jest pusty."
cart_contents = "Zawartość koszyka:"
cart_total = "Suma całkowita:"
cart_cleared = "Koszyk wyczyszczony."

menu_go_to_cart = "🛒 Przejdź do koszyka"
menu_main_menu = "🏠 Menu główne"

add_funds = "💰 Doładuj portfel"
return_to_main_menu = "🏠 Powrót do menu głównego"

insufficient_funds = ("Niestety, nie masz wystarczających środków, aby zrealizować zamówienie.\nŁączna kwota: {"
                      "total}\nTwoje saldo: {balance}\nBrakuje: {shortage}\nProszę doładować saldo i "
                      "spróbować ponownie.")

ask_broadcast_message = "Wprowadź tekst wiadomości do wysłania:"
ask_broadcast_image = "Czy chcesz dodać obraz do wiadomości?"
send_broadcast_image = "Proszę wysłać obraz do rozesłania."
confirm_broadcast = "Czy na pewno chcesz wysłać tę wiadomość do wszystkich użytkowników?"
broadcast_canceled = "Anulowano wysyłanie wiadomości."
broadcast_complete = "Wysyłanie zakończone. Pomyślnie wysłano: {success_count}/{total_count}"
yes = "Tak"
no = "Nie"

confirm_delete_category = "Czy na pewno chcesz usunąć kategorię {category}?"
confirm_delete_subcategory = "Czy na pewno chcesz usunąć podkategorię {subcategory}?"
menu_confirm = "✅ Potwierdź"
deletion_canceled = "Usuwanie anulowane."

ask_category_image = "Wyślij zdjęcie dla kategorii (lub naciśnij 'Pomiń'):"
menu_skip = "⏭ Pomiń"
order_canceled = "Zamówienie anulowane. Koszyk wyczyszczony."
select_category_for_product = "Wybierz kategorię dla produktu:"

menu_add_subcategory = "➕ Dodaj podkategorię"
menu_edit_category = "✏️ Edytuj kategorię"
menu_view_subcategories = "👁️ Zobacz podkategorie"
category_action_prompt = "Wybierz akcję dla kategorii:"
ask_category_name = "Wprowadź nazwę kategorii:"
ask_category_description = "Wprowadź opis kategorii (lub pomiń ten krok):"
category_deleted = "Kategoria została pomyślnie usunięta."
category_not_found = "Nie znaleziono kategorii."

product_price = "Cena"
product_in_cart = "W koszyku"
product_pieces = "szt."
product_subtotal = "Suma w koszyku"
product_added_to_cart = "Produkt dodany do koszyka"
product_removed_from_cart = "Produkt usunięty z koszyka"
menu_add_to_cart = "➕ Dodaj do koszyka"
menu_remove_from_cart = "➖ Usuń z koszyka"

post_order_options = "Co chciałbyś zrobić dalej?"
continue_shopping = "🛒 Kontynuuj zakupy"
no_categories_to_delete = "Brak kategorii do usunięcia."
no_subcategories_to_delete = "Brak podkategorii do usunięcia."
select_category_to_delete = "Wybierz kategorię do usunięcia:"
select_subcategory_to_delete = "Wybierz podkategorię do usunięcia:"
subcategory_deleted = "Podkategoria została pomyślnie usunięta."
subcategory_not_found = "Nie znaleziono podkategorii."

choose_pickup_point = "Wybierz punkt odbioru:"
error_no_pickup_points = "Przepraszamy, obecnie nie ma dostępnych punktów odbioru. Proszę wybrać inną metodę dostawy."
ask_nova_poshta_city = "Wprowadź miasto dostawy:"
ask_nova_poshta_office = "Wprowadź numer oddziału Nova Poshta:"
ask_nova_poshta_phone = "Wprowadź swój numer telefonu:"
ask_nova_poshta_name = "Wprowadź swoje imię i nazwisko:"
ask_kyiv_address = "Wprowadź adres dostawy w Kijowie:"
ask_kyiv_phone = "Wprowadź swój numer telefonu kontaktowego:"
error_checkout_canceled = "Anulowano finalizację zamówienia. Spróbuj ponownie lub skontaktuj się z obsługą klienta."

conversation_open_admin_menu = "Jesteś 💼 <b>Menedżerem</b> tego sklepu!\n" \
                               "Co chciałbyś zrobić?\n" \
                               "\n" \
                               "<i>Wybierz opcję z klawiatury.\n" \
                               "Jeśli klawiatura nie jest widoczna, możesz ją aktywować przyciskiem z czterema kwadratami na dole</i>."

conversation_payment_method = "Jak chciałbyś doładować portfel?"

menu_edit_admins = "👥 Edytuj menedżerów"

admin_properties = "<b>Prawa dostępu dla {name}:</b>"
prop_edit_products = "Edytuj produkty"
prop_edit_categories = "Edytuj kategorie"
prop_edit_subcategories = "Edytuj podkategorie"
prop_receive_orders = "Otrzymuj zamówienia"
prop_create_transactions = "Twórz transakcje"
prop_display_on_help = "Wyświetlaj w pomocy"

conversation_confirm_admin_promotion = "Czy na pewno chcesz nadać temu użytkownikowi prawa menedżera?"

promocode_management_menu = "Wybierz akcję do zarządzania kodami promocyjnymi:"
menu_manage_promocodes = "🎟 Zarządzaj kodami promocyjnymi"
menu_delete_promocode = "🗑 Usuń kod promocyjny"
choose_promocode_type = "Wybierz typ kodu promocyjnego:"
choose_amount_type = "Wybierz typ kwoty:"
ask_fixed_amount = "Wprowadź stałą kwotę:"
ask_min_amount = "Wprowadź minimalną kwotę:"
ask_max_amount = "Wprowadź maksymalną kwotę:"
ask_uses_number = "Wprowadź liczbę możliwych aktywacji:"
promocode_created_qr = "Utworzono kod QR: {code}\nLink: {link}"
promocode_created_text = "Utworzono kod promocyjny: {code}"
promocode_info = "Kod: {code}\nTyp: {type}\nKwota: {amount}\nPozostało aktywacji: {uses_left}/{total_uses}\nUtworzony przez: {creator}\nUżyty: {used_count} razy\nŁączna kwota: {total_amount}"
no_active_promocodes = "Brak aktywnych kodów promocyjnych."
text_promocode = "Tekstowy"
no_promocodes_to_delete = "Brak kodów promocyjnych do usunięcia."
choose_promocode_to_delete = "Wybierz kod promocyjny do usunięcia:"
promocode_deleted = "Kod promocyjny {code} został usunięty."
promocode_not_found = "Nie znaleziono kodu promocyjnego."

conversation_admin_select_product_to_delete = "❌ Który produkt należy usunąć?"

cancel_order = "❌ Anuluj zamówienie"
confirm = "✅ Potwierdź"
confirm_delivery_method = "Wybrałeś metodę dostawy: {method}\nCena dostawy: {price}\nInformacje: {info}\n\nPotwierdź swój wybór:"
or_press_back = "Lub naciśnij 'Wstecz', aby wrócić"

conversation_admin_select_user = "Wybierz użytkownika do edycji."

conversation_cart_actions = "<i>Dodaj produkty do koszyka naciskając przycisk Dodaj." \
                            "  Gdy dokonasz wyboru, wróć do tej wiadomości" \
                            " i naciśnij przycisk Gotowe.</i>"

conversation_confirm_cart = "🛒 Masz następujące produkty w koszyku:\n" \
                            "{product_list}" \
                            "Razem: <b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>Aby kontynuować, naciśnij Gotowe.\n" \
                            "Jeśli zmieniłeś zdanie - wybierz Anuluj.</i>"

conversation_live_orders_start = "Jesteś w trybie <b>Bieżące Zamówienia</b>\n" \
                                 "Wszystkie nowe zamówienia od klientów pojawią się w tym czacie w czasie rzeczywistym," \
                                 " i będziesz mógł oznaczyć je jako ✅ Zrealizowane" \
                                 " lub ✴️ Zwrot środków dla klienta."

conversation_live_orders_stop = "<i>Naciśnij przycisk Stop w tym czacie, aby zakończyć ten tryb.</i>"

conversation_open_help_menu = "Jak możemy Ci pomóc?"

conversation_language_select = "Wybierz język:"

conversation_switch_to_user_mode = " Przeszedłeś w tryb 👤 Klienta.\n" \
                                   "Jeśli chcesz wrócić do menu 💼 Menedżera, zrestartuj rozmowę komendą /start."

conversation_expired = "🕐  Przez długi czas nie otrzymałem żadnej wiadomości, więc zakończyłem rozmowę" \
                       " aby oszczędzać zasoby.\n" \
                       "Aby rozpocząć ponownie, wyślij komendę /start ."

conversation_admin_select_category = "✏️ Którą kategorię chcesz edytować"

ask_subcategory_name = "Wprowadź nazwę podkategorii:"

ask_parent_category = "Wybierz kategorię nadrzędną dla nowej podkategorii:"

error_no_root_categories = "Błąd: brak kategorii głównych. Najpierw utwórz kategorię główną."

success_category_created = "✅ Kategoria została pomyślnie utworzona!"

success_subcategory_created = "✅ Podkategoria została pomyślnie utworzona!"

ask_subcategory_description = "Wprowadź opis podkategorii (lub pomiń ten krok):"

ask_subcategory_image = "Wyślij obraz dla podkategorii (lub pomiń ten krok):"

conversation_select_category = "Wybierz kategorię"

conversation_order_category = "Wybierz kategorię:"

error_product_not_found = "Nie znaleziono produktu."

menu_back = "⬅️ Wstecz"
menu_checkout = "💳 Do kasy"
menu_clear_cart = "🗑️ Wyczyść koszyk"

menu_credit_history = "📈 Historia doładowań"

menu_promocode = "🤩 Wprowadź kod promocyjny"

ask_promocode = "Wprowadź kod promocyjny:"

menu_order = "🛒 Produkty"

menu_uncategorized = "Bez kategorii"

menu_go_back = "🔙 Wróć"

menu_order_status = "🛍 Moje zamówienia"

menu_add_credit = "💵 Doładuj portfel"

menu_profile = "🧾 Profil"

menu_create_promocode = "Utwórz kod promocyjny/kod QR"

menu_list_promocodes = "Statystyki kodów promocyjnych"

credit_history_null = "Nie masz jeszcze żadnych doładowań!"

credit_history = "Historia Twoich doładowań:"

menu_cash = "💵 Gotówką"

menu_credit_card = "💳 Kartą kredytową"

menu_products = "📝️ Produkty"

menu_orders = "📦 Zamówienia"

menu_transactions = "💳 Lista transakcji"

menu_edit_credit = "💰 Utwórz transakcję"

menu_user_mode = "👤 Tryb klienta"

menu_cancel = "🔙 Anuluj"

menu_done = "✅️ Gotowe"

menu_categories = "📝️ Kategorie"

menu_add_category = "✨ Nowa kategoria"

menu_delete_category = "❌ Usuń kategorię"

menu_pay = "💳 Zapłać"

menu_complete = "✅ Zakończ"

menu_refund = "✴️ Zwrot środków"

menu_stop = "🛑 Stop"

menu_all_products = "Wszystkie produkty"

menu_help = "❓ Pomoc"

menu_guide = "📖 Instrukcja"

menu_promo_text = "Tekstowy"

menu_promo_qr = "Kod QR"

menu_promo_fixed = "Stała"

menu_promo_range = "Zakres"

menu_next = "▶️ Następna"

menu_previous = "◀️ Poprzednia"

menu_contact_shopkeeper = "👨‍💼 Kontakt ze sklepem"

menu_csv = "📄 .csv"

menu_language = "🇵🇱 Język"

emoji_yes = "✅"

emoji_no = "🚫"

ask_product_description = "Jaki będzie opis produktu?"

ask_product_price = "Jaka będzie cena?\n" \
                    "Wprowadź <code>X</code> jeśli produkt nie jest obecnie na sprzedaż."

ask_product_image = "🖼 Jakie zdjęcie dodać do produktu?\n" \
                    "\n" \
                    "<i>Wyślij zdjęcie lub Pomiń ten krok.</i>"

ask_order_notes = "Zostawić wiadomość z tym zakupem?\n" \
                  "💼 Wiadomość będzie dostępna dla Menedżera sklepu.\n" \
                  "\n" \
                  "<i>Wyślij swoją wiadomość lub naciśnij Pomiń," \
                  " aby nie zostawiać wiadomości.</i>"

ask_refund_reason = " Napisz powód zwrotu środków.\n" \
                    "👤 Powód będzie dostępny dla klienta."

ask_transaction_notes = " Dodaj wiadomość do transakcji.\n" \
                        "👤 Wiadomość będzie dostępna dla klienta po doładowaniu/wypłacie" \
                        " i dla 💼 Administratora w logach transakcji."

ask_credit = "Jak chcesz zmienić saldo klienta?\n" \
             "\n" \
             "<i>Wyślij wiadomość z kwotą.\n" \
             "Użyj </i><code>+</code><i> aby doładować konto," \
             " i znaku </i><code>-</code><i> aby odjąć środki.</i>"

downloading_image = "Pobieram zdjęcie!\n" \
                    "Może to zająć chwilę... Proszę o cierpliwość!\n" \
                    "Nie będę mógł odpowiadać podczas pobierania."

payment_cash = "Możesz doładować gotówką bezpośrednio w sklepie.\n" \
               "Zapłać i podaj ten identyfikator menedżerowi:\n" \
               "<b>{user_cash_id}</b>"

payment_cc_amount = "Na jaką kwotę chcesz doładować portfel?\n" \
                    "\n" \
                    "<i>Wybierz kwotę z sugerowanych wartości lub wprowadź ręcznie w wiadomości.</i>"

payment_invoice_title = "Doładowanie"

payment_invoice_description = "Opłacenie tego rachunku doda {amount} do twojego portfela."

payment_invoice_label = "Płatność"

payment_invoice_fee_label = "Opłata za doładowanie"

notification_order_placed = "Otrzymano nowe zamówienie:\n" \
                            "\n" \
                            "{order}"

notification_order_completed = "Twoje zamówienie zostało pomyślnie zrealizowane!\n" \
                               "\n" \
                               "{order}"

notification_order_refunded = "Twoje zamówienie zostało anulowane. Środki zostały zwrócone!\n" \
                              "\n" \
                              "{order}"

notification_transaction_created = "ℹ️ Nowa transakcja w twoim portfelu:\n" \
                                   "{transaction}"

contact_shopkeeper = "Obecnie dostępni są następujący pracownicy, którzy mogą pomóc:\n" \
                     "{shopkeepers}\n" \
                     "<i>Wybierz jednego i napisz do niego w czacie Telegram.</i>"

success_category_edited = "✅ Kategoria została pomyślnie utworzona/zaktualizowana!"

ask_category_parent = "Wybierz kategorię nadrzędną dla tej kategorii (lub 'None' dla kategorii głównej):"

success_product_deleted = "✅ Produkt został pomyślnie usunięty!"

success_order_created = "✅ Zamówienie zostało pomyślnie wysłane!\n" \
                        "\n" \
                        "{order}"

success_order_refunded = "✴️ Środki za zamówienie #{order_id} zostały zwrócone."

success_transaction_created = "✅ Transakcja została pomyślnie utworzona!\n" \
                              "{transaction}"

error_payment_amount_over_max = "⚠️ Maksymalna kwota jednej transakcji to {max_amount}."

error_payment_amount_under_min = "⚠️ Minimalna kwota jednej transakcji to {min_amount}."

error_during_checkout = "Wystąpił błąd podczas finalizacji zamówienia. Spróbuj ponownie później."
order_confirmation = "Zamówienie #{order_id} zostało pomyślnie utworzone!\nŁączna kwota: {total}\nMetoda dostawy: {delivery_method}"
manage_delivery_and_pickup = "Wybierz akcję do zarządzania dostawą i odbiorem:"
menu_view_delivery_methods = "👀 Zobacz metody dostawy"
menu_view_pickup_points = "👀 Zobacz punkty odbioru"
view_delivery_methods = "Wybierz metodę dostawy do edycji:"
edit_pickup_point = "Wybierz, co chcesz zmienić:"
edit_pickup_point_address = "Zmień adres"
edit_pickup_point_description = "Zmień opis"
toggle_pickup_point_status = "Zmień status (aktywny/nieaktywny)"
ask_new_pickup_point_address = "Wprowadź nowy adres punktu odbioru:"
ask_new_pickup_point_description = "Wprowadź nowy opis punktu odbioru:"
error_pickup_point_not_found = "❌ Nie znaleziono punktu odbioru."
success_pickup_point_updated = "✅ Punkt odbioru został pomyślnie zaktualizowany!"

choose_delivery_method = "Wybierz metodę dostawy:"
ask_pickup_point_address = "Wprowadź adres punktu odbioru:"
ask_pickup_point_description = "Wprowadź opis punktu odbioru (lub pomiń ten krok):"
success_pickup_point_added = "✅ Punkt odbioru został pomyślnie dodany!"
no_pickup_points = "Obecnie nie ma aktywnych punktów odbioru."
pickup_points_list = "Lista punktów odbioru:"
menu_add_pickup_point = "📍 Dodaj punkt odbioru"
menu_broadcast_message = "📢 Wyślij wiadomość do wszystkich"

menu_add_delivery_method = "➕ Dodaj nową metodę dostawy"
ask_delivery_method_name = "Wprowadź nazwę nowej metody dostawy:"
ask_delivery_method_price = "Wprowadź cenę dostawy (w minimalnych jednostkach waluty):"
success_delivery_method_added = "✅ Nowa metoda dostawy została pomyślnie dodana!"
error_delivery_method_not_found = "❌ Nie znaleziono metody dostawy."
edit_delivery_method = "Wybierz, co chcesz zmienić:"
edit_delivery_method_name = "Zmień nazwę"
edit_delivery_method_price = "Zmień cenę"
toggle_delivery_method_status = "Zmień status (aktywny/nieaktywny)"
ask_new_delivery_method_name = "Wprowadź nową nazwę metody dostawy:"
ask_new_delivery_method_price = "Wprowadź nową cenę dostawy (w minimalnych jednostkach waluty):"
success_delivery_method_updated = "✅ Metoda dostawy została pomyślnie zaktualizowana!"

error_not_enough_credit = "⚠️ Nie masz wystarczających środków, aby zrealizować zamówienie."

error_order_already_cleared = "⚠️ To zamówienie zostało już wcześniej przetworzone."

error_no_orders = "⚠️ Nie złożyłeś jeszcze żadnych zamówień, dlatego tutaj jest pusto."

error_user_does_not_exist = "⚠️ Taki użytkownik nie istnieje."

fatal_conversation_exception = "☢️ Ojej! <b>Błąd</b> przerwał naszą rozmowę\n" \
                               "Właściciel bota został powiadomiony o błędzie.\n" \
                               "Aby rozpocząć rozmowę ponownie, wyślij komendę /start."
help_msg = ""

error_no_delivery_methods = "Obecnie nie ma aktywnych metod dostawy."

error_listing_promocodes = "Wystąpił błąd podczas wyświetlania kodów promocyjnych."

invalid_promocode = "Nieprawidłowy kod promocyjny"

bot_info = ""