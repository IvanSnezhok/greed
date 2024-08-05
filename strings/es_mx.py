# Strings / localization file for greed
# Can be edited, but DON'T REMOVE THE REPLACEMENT FIELDS (words surrounded by {curly braces})
# Current localization is Spanish (Mexico)

# Currency symbol
currency_symbol = "$"

# Positioning of the currency symbol
currency_format_string = "{symbol}{value}"

# Quantity of a product in stock
in_stock_format_string = "{quantity} disponibles"

# Copies of a product in cart
in_cart_format_string = "{quantity} en el carrito"

# Product information
product_format_string = "<b>{name}</b>\n" \
                        "{description}\n" \
                        "{price}\n" \
                        "<b>{cart}</b>"

# Order number, displayed in the order info
order_number = "Orden #{id}"

# Order info string, shown to the admins
order_format_string = "por {user}\n" \
                      "Creado {date}\n" \
                      "\n" \
                      "{items}\n" \
                      "TOTAL: <b>{value}</b>\n" \
                      "\n" \
                      "Notas del cliente: {notes}\n"

# Order info string, shown to the user
user_order_format_string = "{status_emoji} <b>Orden {status_text}</b>\n" \
                           "{items}\n" \
                           "TOTAL: <b>{value}</b>\n" \
                           "\n" \
                           "Notas: {notes}\n"

# Transaction page is loading
loading_transactions = "<i>Cargando transacciones...\n" \
                       "Por favor espere unos segundos.</i>"

# Transactions page
transactions_page = "Página <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

# Archivo de cadenas / localización para greed
# Puede editarse, pero NO ELIMINE LOS CAMPOS DE REEMPLAZO (palabras rodeadas por {llaves})
# Localización actual: Español (México)

# Símbolo de moneda
currency_symbol = "$"

# Posicionamiento del símbolo de moneda
currency_format_string = "{symbol}{value}"

# Cantidad de un producto en stock
in_stock_format_string = "{quantity} disponibles"

# Copias de un producto en el carrito
in_cart_format_string = "{quantity} en el carrito"

# Información del producto
product_format_string = "<b>{name}</b>\n" \
                        "{description}\n" \
                        "{price}\n" \
                        "<b>{cart}</b>"

# Número de orden, mostrado en la información de la orden
order_number = "Orden #{id}"

# Cadena de información de la orden, mostrada a los administradores
order_format_string = "por {user}\n" \
                      "Creada {date}\n" \
                      "\n" \
                      "{items}\n" \
                      "TOTAL: <b>{value}</b>\n" \
                      "\n" \
                      "Notas del cliente: {notes}\n"

# Cadena de información de la orden, mostrada al usuario
user_order_format_string = "{status_emoji} <b>Orden {status_text}</b>\n" \
                           "{items}\n" \
                           "TOTAL: <b>{value}</b>\n" \
                           "\n" \
                           "Notas: {notes}\n"

# La página de transacciones está cargando
loading_transactions = "<i>Cargando transacciones...\n" \
                       "Por favor, espere unos segundos.</i>"

# Página de transacciones
transactions_page = "Página <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

# Leyenda del archivo transactions.csv
csv_caption = "Se ha generado un archivo 📄 .csv que contiene todas las transacciones almacenadas en la base de datos del bot.\n" \
              "Puede abrir este archivo con otros programas, como LibreOffice Calc, para procesar los datos."

# Conversación: se envió el comando de inicio y el bot debe dar la bienvenida al usuario
conversation_after_start = "¡Hola!\n" \
                           "¡Bienvenido a greed!\n" \
                           "Esta es la versión 🅱️ <b>Beta</b> del software.\n" \
                           "Es completamente funcional, pero puede haber algunos errores.\n" \
                           "Si encuentra alguno, por favor repórtelo en https://github.com/Steffo99/greed/issues."

# Conversación: para enviar un teclado en línea necesitas enviar un mensaje con él
conversation_open_user_menu = "¿Qué le gustaría hacer?\n" \
                              "💰 Tiene <b>{credit}</b> en su cartera.\n" \
                              "\n" \
                              "<i>Presione un botón en el teclado de abajo para seleccionar una operación.\n" \
                              "Si el teclado no se abre, puede abrirlo presionando el botón con cuatro pequeños cuadrados en la barra de mensajes.</i>"

# Conversación: como arriba, pero para administradores
conversation_open_admin_menu = "¡Usted es un 💼 <b>Gerente</b> de esta tienda!\n" \
                               "¿Qué le gustaría hacer?\n" \
                               "\n" \
                               "<i>Presione un botón en el teclado de abajo para seleccionar una operación.\n" \
                               "Si el teclado no se abre, puede abrirlo presionando el botón con cuatro pequeños cuadrados en la barra de mensajes.</i>"

# Conversación: seleccionar un método de pago
conversation_payment_method = "¿Cómo le gustaría añadir fondos a su cartera?"

# Conversación: seleccionar un producto para editar
conversation_admin_select_product = "✏️ ¿Qué producto desea editar?"

# Conversación: seleccionar un producto para eliminar
conversation_admin_select_product_to_delete = "❌ ¿Qué producto desea eliminar?"

# Conversación: seleccionar un usuario para editar
conversation_admin_select_user = "Seleccione un usuario para realizar la acción seleccionada."

# Conversación: hacer clic abajo para pagar la compra
conversation_cart_actions = "<i>Añada productos al carrito desplazándose hacia arriba y presionando el botón Añadir debajo de los productos que desea comprar. Cuando haya terminado, vuelva a este mensaje y presione el botón Listo.</i>"

# Conversación: confirmar el contenido del carrito
conversation_confirm_cart = "🛒 Su carrito contiene estos productos:\n" \
                            "{product_list}" \
                            "Total: <b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>Presione el botón Listo debajo de este mensaje para proceder.\n" \
                            "Para cancelar, presione el botón Cancelar.</i>"

# Modo de órdenes en vivo: inicio
conversation_live_orders_start = "¡Está en el modo de <b>Órdenes en Vivo</b>!\n" \
                                 "Todas las nuevas órdenes realizadas por los clientes aparecerán en tiempo real en este chat, y podrá marcarlas como ✅ completadas" \
                                 " o ✴️ reembolsar el crédito al cliente."

# Modo de órdenes en vivo: detener la recepción de mensajes
conversation_live_orders_stop = "<i>Presione el botón Detener debajo de este mensaje para dejar de recibir órdenes en vivo.</i>"

# Conversación: se ha abierto el menú de ayuda
conversation_open_help_menu = "¿Qué tipo de ayuda necesita?"

# Conversación: confirmar promoción a administrador
conversation_confirm_admin_promotion = "¿Está seguro de que desea promover a este usuario a 💼 Gerente?\n" \
                                       "¡Esta es una acción irreversible!"

# Conversación: encabezado del menú de selección de idioma
conversation_language_select = "Seleccione un idioma:"

# Conversación: cambiar al modo de usuario
conversation_switch_to_user_mode = "Está cambiando al modo de 👤 Cliente.\n" \
                                   "Si desea volver al modo de 💼 Gerente, reinicie la conversación con /start."

# Notificación: la conversación ha expirado
conversation_expired = "🕐 No he recibido ningún mensaje en un tiempo, así que he cerrado la conversación para ahorrar energía.\n" \
                       "Si desea iniciar una nueva, envíe el comando /start de nuevo."

# Menú de usuario: ordenar
menu_order = "🛒 Ordenar"

# Menú de usuario: estado de la orden
menu_order_status = "🛍 Mis órdenes"

# Menú de usuario: añadir crédito
menu_add_credit = "💵 Añadir fondos"

# Menú de usuario: información del bot
menu_bot_info = "ℹ️ Información del bot"

# Menú de usuario: efectivo
menu_cash = "💵 Efectivo"

# Menú de usuario: tarjeta de crédito
menu_credit_card = "💳 Tarjeta de crédito"

# Menú de administrador: productos
menu_products = "📝️ Productos"

# Menú de administrador: órdenes
menu_orders = "📦 Órdenes"

# Menú: transacciones
menu_transactions = "💳 Lista de transacciones"

# Menú: editar crédito
menu_edit_credit = "💰 Crear transacción"

# Menú de administrador: ir al modo de usuario
menu_user_mode = "👤 Cambiar al modo de cliente"

# Menú de administrador: añadir producto
menu_add_product = "✨ Nuevo producto"

# Menú de administrador: eliminar producto
menu_delete_product = "❌ Eliminar producto"

# Menú: cancelar
menu_cancel = "🔙 Cancelar"

# Menú: volver
menu_go_back = "🔙 Volver"

# Menú: saltar
menu_skip = "⏭ Saltar"

# Menú: listo
menu_done = "✅️ Listo"

# Menú: pagar factura
menu_pay = "💳 Pagar"

# Menú: completar
menu_complete = "✅ Completar"

# Menú: reembolsar
menu_refund = "✴️ Reembolsar"

# Menú: detener
menu_stop = "🛑 Detener"

# Menú: añadir al carrito
menu_add_to_cart = "➕ Añadir"

# Menú: eliminar del carrito
menu_remove_from_cart = "➖ Eliminar"

# Menú: menú de ayuda
menu_help = "❓ Ayuda y soporte"

# Menú: guía
menu_guide = "📖 Guía"

# Menú: siguiente página
menu_next = "▶️ Siguiente"

# Menú: página anterior
menu_previous = "◀️ Anterior"

# Menú: contactar al vendedor
menu_contact_shopkeeper = "👨‍💼 Contactar a la tienda"

# Menú: generar archivo .csv de transacciones
menu_csv = "📄 .csv"

# Menú: editar lista de administradores
menu_edit_admins = "🏵 Editar gerentes"

# Menú: idioma
menu_language = "🇲🇽 Idioma"

# Emoji: orden no procesada
emoji_not_processed = "*️⃣"

# Emoji: orden completada
emoji_completed = "✅"

# Emoji: orden reembolsada
emoji_refunded = "✴️"

# Emoji: sí
emoji_yes = "✅"

# Emoji: no
emoji_no = "🚫"

# Texto: orden no procesada
text_not_processed = "pendiente"

# Texto: orden completada
text_completed = "completada"

# Texto: orden reembolsada
text_refunded = "reembolsada"

# Añadir producto: ¿categoría?
ask_product_category = "¿Cuál debe ser la categoría del producto?"

# Añadir producto: ¿nombre?
ask_product_name = "¿Cuál debe ser el nombre del producto?"

# Añadir producto: ¿descripción?
ask_product_description = "¿Cuál debe ser la descripción del producto?"

# Añadir producto: ¿precio?
ask_product_price = "¿Cuál debe ser el precio del producto?\n" \
                    "Escriba <code>X</code> si desea que el producto no esté a la venta todavía."

# Añadir producto: texto "No a la venta aún"
not_for_sale_yet = "No a la venta aún"

# Añadir producto: ¿imagen?
ask_product_image = "🖼 ¿Qué imagen desea que tenga el producto?\n" \
                    "\n" \
                    "<i>Envíe una foto, o si prefiere dejar el producto sin imagen, presione el botón Saltar debajo.</i>"

# Añadir categoría: ¿nombre?
ask_category_name = "¿Cuál debe ser el nombre de la categoría?"

# Ordenar producto: ¿notas?
ask_order_notes = "¿Desea dejar una nota junto con la orden?\n" \
                  "💼 Será visible para los gerentes de la tienda.\n" \
                  "\n" \
                  "<i>Envíe un mensaje con la nota que desea dejar, o presione el botón Saltar debajo de este mensaje para no dejar nada.</i>"

# Reembolsar producto: ¿razón?
ask_refund_reason = "Adjunte una razón a este reembolso.\n" \
                    "👤 Será visible para el cliente."

# Editar crédito: ¿notas?
ask_transaction_notes = "Adjunte una nota a esta transacción.\n" \
                        "👤 Será visible para el cliente después del crédito/débito" \
                        " y para los 💼 Gerentes en el registro de transacciones."

# Editar crédito: ¿cantidad?
ask_credit = "¿Cuánto desea cambiar el crédito del cliente?\n" \
             "\n" \
             "<i>Envíe un mensaje que contenga la cantidad.\n" \
             "Use el signo </i><code>+</code><i> para añadir crédito a la cuenta del cliente," \
             " o el signo </i><code>-</code><i> para deducirlo.</i>"

# Encabezado para el mensaje de edición de administrador
admin_properties = "<b>Permisos para {name}:</b>"

# Editar administrador: ¿puede editar productos?
prop_edit_products = "Editar productos"

# Editar administrador: ¿puede editar categorías?
prop_edit_categories = "Editar categorías"

# Editar administrador: ¿puede recibir órdenes?
prop_receive_orders = "Recibir órdenes"

# Editar administrador: ¿puede crear transacciones?
prop_create_transactions = "Gestionar transacciones"

# Editar administrador: ¿mostrar en el mensaje de ayuda?
prop_display_on_help = "Soporte al cliente"

# El hilo ha comenzado a descargar una imagen y puede no responder
downloading_image = "¡Estoy descargando tu foto!\n" \
                    "Puede tomar un momento... ¡Por favor, ten paciencia!\n" \
                    "No podré responderte durante la descarga."

# Editar producto: valor actual
edit_current_value = "El valor actual es:\n" \
                     "<pre>{value}</pre>\n" \
                     "\n" \
                     "<i>Presione el botón Saltar debajo de este mensaje para mantener el mismo valor.</i>"

# Pago: información de pago en efectivo
payment_cash = "Puede pagar en efectivo en la tienda física.\n" \
               "Pague en la caja y proporcione este id al gerente de la tienda:\n" \
               "<b>{user_cash_id}</b>"

# Menú de usuario: historial de crédito
menu_credit_history = "📈 Historial de crédito"

# Menú de usuario: ingresar código promocional
menu_promocode = "🤩 Ingresar código promocional"

# Solicitar código promocional
ask_promocode = "Ingrese el código promocional:"

# Código promocional aplicado con éxito
promocode_applied = "¡Código promocional aplicado!"

# Código promocional inválido
promocode_invalid = "Código promocional inválido."

# Menú de usuario: perfil
menu_profile = "🧾 Perfil"

# El historial de crédito está vacío
credit_history_null = "¡Aún no has realizado ninguna recarga!"

# Historial de crédito
credit_history = "Tu historial de recargas:"

# Pago: cantidad de tarjeta de crédito
payment_cc_amount = "¿Cuánto dinero quieres agregar a tu cartera?\n" \
                    "\n" \
                    "<i>Selecciona una cantidad con los botones de abajo, o ingrésala manualmente con el teclado normal.</i>"

# Pago: título de la factura para agregar fondos
payment_invoice_title = "Agregar fondos"

# Pago: descripción de la factura para agregar fondos
payment_invoice_description = "Pagar esta factura agregará {amount} a tu cartera."

# Pago: etiqueta del precio etiquetado en la factura
payment_invoice_label = "Recarga"

# Pago: etiqueta de la comisión en la factura
payment_invoice_fee_label = "Comisión de tarjeta"

# Notificación: se ha realizado un pedido
notification_order_placed = "Se ha realizado un nuevo pedido:\n" \
                            "{order}"

# Notificación: el pedido ha sido completado
notification_order_completed = "¡Tu pedido ha sido completado!\n" \
                               "{order}"

# Notificación: el pedido ha sido reembolsado
notification_order_refunded = "¡Tu pedido ha sido reembolsado!\n" \
                              "{order}"

# Notificación: se ha aplicado una transacción manual
notification_transaction_created = "ℹ️ Se ha aplicado una nueva transacción a tu cartera:\n" \
                                   "{transaction}"

# Razón del reembolso
refund_reason = "Razón del reembolso:\n" \
                "{reason}"

# Info: información sobre el bot
bot_info = 'Este bot utiliza <a href="https://github.com/Steffo99/greed">greed</a>,' \
           ' un framework de @Steffo para pagos en Telegram lanzado bajo la' \
           ' <a href="https://github.com/Steffo99/greed/blob/master/LICENSE.txt">' \
           'Affero General Public License 3.0</a>.\n'

# Ayuda: guía
help_msg = "Una guía sobre cómo usar este bot está disponible en esta dirección:\n" \
           "https://docs.google.com/document/d/1f4MKVr0B7RSQfWTSa_6ZO0LM4nPpky_GX_qdls3EHtQ/"

# Ayuda: contactar al vendedor
contact_shopkeeper = "El personal actualmente disponible para proporcionar asistencia al usuario está compuesto por:\n" \
                     "{shopkeepers}\n" \
                     "<i>Haz clic / Toca uno de sus nombres para contactarlos en un chat de Telegram.</i>"

# Éxito: el producto ha sido añadido/editado en la base de datos
success_product_edited = "✅ ¡El producto ha sido añadido/modificado con éxito!"

# Éxito: el producto ha sido eliminado de la base de datos
success_product_deleted = "✅ ¡El producto ha sido eliminado con éxito!"

# Éxito: se ha creado el pedido
success_order_created = "✅ ¡El pedido se ha enviado con éxito!\n" \
                        "\n" \
                        "{order}"

# Éxito: el pedido se ha marcado como completado
success_order_completed = "✅ Has marcado el pedido #{order_id} como completado."

# Éxito: el pedido se ha reembolsado con éxito
success_order_refunded = "✴️ El pedido #{order_id} ha sido reembolsado con éxito."

# Éxito: la transacción se ha creado con éxito
success_transaction_created = "✅ ¡La transacción se ha creado con éxito!\n" \
                              "{transaction}"

# Error: mensaje recibido no en un chat privado
error_nonprivate_chat = "⚠️ Este bot solo funciona en chats privados."

# Error: se envió un mensaje en un chat, pero no existe un trabajador para ese chat.
# Sugiere la creación de un nuevo trabajador con /start
error_no_worker_for_chat = "⚠️ La conversación con el bot fue interrumpida.\n" \
                           "Para reiniciarla, envía el comando /start al bot."

# Error: se envió un mensaje en un chat, pero el trabajador para ese chat no está listo.
error_worker_not_ready = "🕒 La conversación con el bot está iniciando actualmente.\n" \
                         "¡Por favor, espera unos momentos antes de enviar más comandos!"

# Error: cantidad de fondos a agregar sobre el máximo
error_payment_amount_over_max = "⚠️ La cantidad máxima que se puede agregar en una sola transacción es {max_amount}."

# Error: cantidad de fondos a agregar bajo el mínimo
error_payment_amount_under_min = "⚠️ La cantidad mínima que se puede agregar en una sola transacción es {min_amount}."

# Error: la factura ha expirado y no se puede pagar
error_invoice_expired = "⚠️ Esta factura ha expirado y fue cancelada. Si aún quieres agregar fondos, usa la opción Agregar fondos del menú."

# Error: ya existe un producto con ese nombre
error_duplicate_name = "️⚠️ Ya existe un producto con el mismo nombre."

# Error: no hay suficiente crédito para hacer el pedido
error_not_enough_credit = "⚠️ No tienes suficiente crédito para realizar el pedido."

# Error: el pedido ya ha sido procesado
error_order_already_cleared = "⚠️ Este pedido ya ha sido procesado."

# Error: no se han realizado pedidos, así que no se puede mostrar ninguno
error_no_orders = "⚠️ Aún no has realizado ningún pedido, así que no hay nada que mostrar."

# Error: el usuario seleccionado no existe
error_user_does_not_exist = "⚠️ El usuario seleccionado no existe."

# Fatal: la conversación generó una excepción
fatal_conversation_exception = "☢️ ¡Oh no! Un <b>error</b> interrumpió esta conversación.\n" \
                               "El error ha sido reportado al dueño del bot para que puedan arreglarlo.\n" \
                               "Para reiniciar la conversación, envía el comando /start de nuevo."
