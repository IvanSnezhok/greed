# Arquivo de strings / localização para greed
# Pode ser editado, mas NÃO REMOVA OS CAMPOS DE SUBSTITUIÇÃO (palavras cercadas por {chaves})
# Localização atual: Português Brasileiro

# Símbolo da moeda
currency_symbol = "R$"

# Posicionamento do símbolo da moeda
currency_format_string = "{symbol} {value}"

# Quantidade de um produto em estoque
in_stock_format_string = "{quantity} disponíveis"

# Cópias de um produto no carrinho
in_cart_format_string = "{quantity} no carrinho"

# Informações do produto
product_format_string = "<b>{name}</b>\n" \
                        "{description}\n" \
                        "{price}\n" \
                        "<b>{cart}</b>"

# Número do pedido, exibido nas informações do pedido
order_number = "Pedido #{id}"

# String de informações do pedido, mostrada aos administradores
order_format_string = "por {user}\n" \
                      "Criado em {date}\n" \
                      "\n" \
                      "{items}\n" \
                      "TOTAL: <b>{value}</b>\n" \
                      "\n" \
                      "Observações do cliente: {notes}\n"

# String de informações do pedido, mostrada ao usuário
user_order_format_string = "{status_emoji} <b>Pedido {status_text}</b>\n" \
                           "{items}\n" \
                           "TOTAL: <b>{value}</b>\n" \
                           "\n" \
                           "Observações: {notes}\n"

# A página de transações está carregando
loading_transactions = "<i>Carregando transações...\n" \
                       "Por favor, aguarde alguns segundos.</i>"

# Página de transações
transactions_page = "Página <b>{page}</b>:\n" \
                    "\n" \
                    "{transactions}"

# Legenda do arquivo transactions.csv
csv_caption = "Um arquivo 📄 .csv contendo todas as transações armazenadas no banco de dados do bot foi gerado.\n" \
              "Você pode abrir este arquivo com outros programas, como o LibreOffice Calc, para processar os dados."

# Conversa: o comando start foi enviado e o bot deve dar as boas-vindas ao usuário
conversation_after_start = "Olá!\n" \
                           "Bem-vindo ao greed!\n" \
                           "Esta é a versão 🅱️ <b>Beta</b> do software.\n" \
                           "É totalmente utilizável, mas ainda pode haver alguns bugs.\n" \
                           "Se você encontrar algum, por favor, reporte em https://github.com/Steffo99/greed/issues."

# Conversa: para enviar um teclado inline, você precisa enviar uma mensagem com ele
conversation_open_user_menu = "O que você gostaria de fazer?\n" \
                              "💰 Você tem <b>{credit}</b> em sua carteira.\n" \
                              "\n" \
                              "<i>Pressione um botão no teclado abaixo para selecionar uma operação.\n" \
                              "Se o teclado não abrir, você pode abri-lo pressionando o botão com quatro pequenos quadrados na barra de mensagem.</i>"

# Conversa: como acima, mas para administradores
conversation_open_admin_menu = "Você é um 💼 <b>Gerente</b> desta loja!\n" \
                               "O que você gostaria de fazer?\n" \
                               "\n" \
                               "<i>Pressione um botão no teclado abaixo para selecionar uma operação.\n" \
                               "Se o teclado não abrir, você pode abri-lo pressionando o botão com quatro pequenos quadrados na barra de mensagem.</i>"

# Conversa: selecione um método de pagamento
conversation_payment_method = "Como você gostaria de adicionar fundos à sua carteira?"

# Conversa: selecione um produto para editar
conversation_admin_select_product = "✏️ Qual produto você quer editar?"

# Conversa: selecione um produto para excluir
conversation_admin_select_product_to_delete = "❌ Qual produto você quer excluir?"

# Conversa: selecione um usuário para editar
conversation_admin_select_user = "Selecione um usuário para realizar a ação selecionada."

# Conversa: clique abaixo para pagar pela compra
conversation_cart_actions = "<i>Adicione produtos ao carrinho rolando para cima e pressionando o botão Adicionar abaixo dos produtos que deseja comprar. Quando terminar, volte a esta mensagem e pressione o botão Concluído.</i>"

# Conversa: confirme o conteúdo do carrinho
conversation_confirm_cart = "🛒 Seu carrinho contém estes produtos:\n" \
                            "{product_list}" \
                            "Total: <b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>Pressione o botão Concluído abaixo desta mensagem para prosseguir.\n" \
                            "Para cancelar, pressione o botão Cancelar.</i>"

# Modo de pedidos ao vivo: início
conversation_live_orders_start = "Você está no modo de <b>Pedidos ao Vivo</b>!\n" \
                                 "Todos os novos pedidos feitos pelos clientes aparecerão em tempo real neste chat, e você poderá marcá-los como ✅ concluídos" \
                                 " ou ✴️ reembolsar o crédito ao cliente."

# Modo de pedidos ao vivo: pare de receber mensagens
conversation_live_orders_stop = "<i>Pressione o botão Parar abaixo desta mensagem para parar de receber pedidos ao vivo.</i>"

# Conversa: o menu de ajuda foi aberto
conversation_open_help_menu = "Que tipo de ajuda você precisa?"

# Conversa: confirme a promoção para administrador
conversation_confirm_admin_promotion = "Tem certeza de que deseja promover este usuário a 💼 Gerente?\n" \
                                       "Esta é uma ação irreversível!"

# Conversa: cabeçalho do menu de seleção de idioma
conversation_language_select = "Selecione um idioma:"

# Conversa: mudando para o modo de usuário
conversation_switch_to_user_mode = "Você está mudando para o modo 👤 Cliente.\n" \
                                   "Se quiser voltar ao modo 💼 Gerente, reinicie a conversa com /start."

# Notificação: a conversa expirou
conversation_expired = "🕐 Não recebi nenhuma mensagem por um tempo, então fechei a conversa para economizar energia.\n" \
                       "Se quiser iniciar uma nova, envie o comando /start novamente."

# Menu do usuário: pedido
menu_order = "🛒 Fazer pedido"

# Menu do usuário: status do pedido
menu_order_status = "🛍 Meus pedidos"

# Menu do usuário: adicionar crédito
menu_add_credit = "💵 Adicionar fundos"

# Menu do usuário: informações do bot
menu_bot_info = "ℹ️ Informações do bot"

# Menu do usuário: dinheiro
menu_cash = "💵 Dinheiro"

# Menu do usuário: cartão de crédito
menu_credit_card = "💳 Cartão de crédito"

# Menu do administrador: produtos
menu_products = "📝️ Produtos"

# Menu do administrador: pedidos
menu_orders = "📦 Pedidos"

# Menu: transações
menu_transactions = "💳 Lista de transações"

# Menu: editar crédito
menu_edit_credit = "💰 Criar transação"

# Menu do administrador: ir para o modo de usuário
menu_user_mode = "👤 Mudar para o modo cliente"

# Menu do administrador: adicionar produto
menu_add_product = "✨ Novo produto"

# Menu do administrador: excluir produto
menu_delete_product = "❌ Excluir produto"

# Menu: cancelar
menu_cancel = "🔙 Cancelar"

# Menu: voltar
menu_go_back = "🔙 Voltar"

# Menu: pular
menu_skip = "⏭ Pular"

# Menu: concluído
menu_done = "✅️ Concluído"

# Menu: pagar fatura
menu_pay = "💳 Pagar"

# Menu: completar
menu_complete = "✅ Completar"

# Menu: reembolsar
menu_refund = "✴️ Reembolsar"

# Menu: parar
menu_stop = "🛑 Parar"

# Menu: adicionar ao carrinho
menu_add_to_cart = "➕ Adicionar"

# Menu: remover do carrinho
menu_remove_from_cart = "➖ Remover"

# Menu: menu de ajuda
menu_help = "❓ Ajuda e suporte"

# Menu: guia
menu_guide = "📖 Guia"

# Menu: próxima página
menu_next = "▶️ Próxima"

# Menu: página anterior
menu_previous = "◀️ Anterior"

# Menu: contatar o vendedor
menu_contact_shopkeeper = "👨‍💼 Contatar a loja"

# Menu: gerar arquivo .csv de transações
menu_csv = "📄 .csv"

# Menu: editar lista de administradores
menu_edit_admins = "🏵 Editar gerentes"

# Menu: idioma
menu_language = "🇧🇷 Idioma"

# Emoji: pedido não processado
emoji_not_processed = "*️⃣"

# Emoji: pedido concluído
emoji_completed = "✅"

# Emoji: pedido reembolsado
emoji_refunded = "✴️"

# Emoji: sim
emoji_yes = "✅"

# Emoji: não
emoji_no = "🚫"

# Texto: pedido não processado
text_not_processed = "pendente"

# Texto: pedido concluído
text_completed = "concluído"

# Texto: pedido reembolsado
text_refunded = "reembolsado"

# Adicionar produto: categoria?
ask_product_category = "Qual deve ser a categoria do produto?"

# Adicionar produto: nome?
ask_product_name = "Qual deve ser o nome do produto?"

# Adicionar produto: descrição?
ask_product_description = "Qual deve ser a descrição do produto?"

# Adicionar produto: preço?
ask_product_price = "Qual deve ser o preço do produto?\n" \
                    "Escreva <code>X</code> se você quiser que o produto ainda não esteja à venda."

# Adicionar produto: texto "Ainda não à venda"
not_for_sale_yet = "Ainda não à venda"

# Adicionar produto: imagem?
ask_product_image = "🖼 Que imagem você quer que o produto tenha?\n" \
                    "\n" \
                    "<i>Envie uma foto ou, se preferir deixar o produto sem imagem, pressione o botão Pular abaixo.</i>"

# Adicionar categoria: nome?
ask_category_name = "Qual deve ser o nome da categoria?"

# Pedir produto: observações?
ask_order_notes = "Você gostaria de deixar uma observação junto com o pedido?\n" \
                  "💼 Será visível para os gerentes da loja.\n" \
                  "\n" \
                  "<i>Envie uma mensagem com a observação que deseja deixar, ou pressione o botão Pular abaixo desta mensagem para não deixar nada.</i>"

# Reembolsar produto: motivo?
ask_refund_reason = "Anexe um motivo a este reembolso.\n" \
                    "👤 Será visível para o cliente."

# Editar crédito: observações?
ask_transaction_notes = "Anexe uma observação a esta transação.\n" \
                        "👤 Será visível para o cliente após o crédito/débito" \
                        " e para os 💼 Gerentes no registro de transações."

# Editar crédito: quantia?
ask_credit = "Quanto você quer mudar o crédito do cliente?\n" \
             "\n" \
             "<i>Envie uma mensagem contendo o valor.\n" \
             "Use o sinal </i><code>+</code><i> para adicionar crédito à conta do cliente," \
             " ou o sinal </i><code>-</code><i> para deduzi-lo.</i>"

# Cabeçalho para a mensagem de edição do administrador
admin_properties = "<b>Permissões para {name}:</b>"

# Editar administrador: pode editar produtos?
prop_edit_products = "Editar produtos"

# Editar administrador: pode editar categorias?
prop_edit_categories = "Editar categorias"

# Editar administrador: pode receber pedidos?
prop_receive_orders = "Receber pedidos"

# Editar administrador: pode criar transações?
prop_create_transactions = "Gerenciar transações"

# Editar administrador: mostrar na mensagem de ajuda?
prop_display_on_help = "Suporte ao cliente"

# O thread começou a baixar uma imagem e pode não responder
downloading_image = "Estou baixando sua foto!\n" \
                    "Pode levar um tempo... Por favor, seja paciente!\n" \
                    "Não poderei responder durante o download."

# Editar produto: valor atual
edit_current_value = "O valor atual é:\n" \
                     "<pre>{value}</pre>\n" \
                     "\n" \
                     "<i>Pressione o botão Pular abaixo desta mensagem para manter o mesmo valor.</i>"

# Pagamento: informações de pagamento em dinheiro
payment_cash = "Você pode pagar em dinheiro na loja física.\n" \
               "Pague no caixa e forneça este ID ao gerente da loja:\n" \
               "<b>{user_cash_id}</b>"

# Menu do usuário: histórico de crédito
menu_credit_history = "📈 Histórico de crédito"

# Menu do usuário: inserir código promocional
menu_promocode = "🤩 Inserir código promocional"

# Pedir código promocional
ask_promocode = "Insira o código promocional:"

# Código promocional aplicado
promocode_applied = "Código promocional aplicado!"

# Código promocional inválido
promocode_invalid = "Código promocional inválido."

# Menu do usuário: perfil
menu_profile = "🧾 Perfil"

# O histórico de crédito está vazio
credit_history_null = "Você ainda não fez nenhuma recarga!"

# Histórico de crédito
credit_history = "Seu histórico de recargas:"

# Pagamento: valor do cartão de crédito
payment_cc_amount = "Quanto dinheiro você quer adicionar à sua carteira?\n" \
                    "\n" \
                    "<i>Selecione um valor com os botões abaixo, ou insira manualmente com o teclado normal.</i>"

# Pagamento: título da fatura para adicionar fundos
payment_invoice_title = "Adicionando fundos"

# Pagamento: descrição da fatura para adicionar fundos
payment_invoice_description = "Pagar esta fatura adicionará {amount} à sua carteira."

# Pagamento: rótulo do preço rotulado na fatura
payment_invoice_label = "Recarga"

# Pagamento: rótulo da taxa na fatura
payment_invoice_fee_label = "Taxa do cartão"

# Notificação: um pedido foi feito
notification_order_placed = "Um novo pedido foi feito:\n" \
                            "{order}"

# Notificação: o pedido foi concluído
notification_order_completed = "Seu pedido foi concluído!\n" \
                               "{order}"

# Notificação: o pedido foi reembolsado
notification_order_refunded = "Seu pedido foi reembolsado!\n" \
                              "{order}"

# Notificação: uma transação manual foi aplicada
notification_transaction_created = "ℹ️ Uma nova transação foi aplicada à sua carteira:\n" \
                                   "{transaction}"

# Motivo do reembolso
refund_reason = "Motivo do reembolso:\n" \
                "{reason}"

# Info: informações sobre o bot
bot_info = 'Este bot usa <a href="https://github.com/Steffo99/greed">greed</a>,' \
           ' um framework de @Steffo para pagamentos no Telegram lançado sob a' \
           ' <a href="https://github.com/Steffo99/greed/blob/master/LICENSE.txt">' \
           'Affero General Public License 3.0</a>.\n'

# Ajuda: guia
help_msg = "Um guia sobre como usar este bot está disponível neste endereço:\n" \
           "https://docs.google.com/document/d/1f4MKVr0B7RSQfWTSa_6ZO0LM4nPpky_GX_qdls3EHtQ/"

# Ajuda: contatar o vendedor
contact_shopkeeper = "A equipe atualmente disponível para fornecer assistência ao usuário é composta por:\n" \
                     "{shopkeepers}\n" \
                     "<i>Clique / Toque em um de seus nomes para contatá-los em um chat do Telegram.</i>"

# Sucesso: o produto foi adicionado/editado no banco de dados
success_product_edited = "✅ O produto foi adicionado/modificado com sucesso!"

# Sucesso: o produto foi excluído do banco de dados
success_product_deleted = "✅ O produto foi excluído com sucesso!"

# Sucesso: o pedido foi criado
success_order_created = "✅ O pedido foi enviado com sucesso!\n" \
                        "\n" \
                        "{order}"

# Sucesso: o pedido foi marcado como concluído
success_order_completed = "✅ Você marcou o pedido #{order_id} como concluído."

# Sucesso: o pedido foi reembolsado com sucesso
success_order_refunded = "✴️ O pedido #{order_id} foi reembolsado com sucesso."

# Sucesso: a transação foi criada com sucesso
success_transaction_created = "✅ A transação foi criada com sucesso!\n" \
                              "{transaction}"

# Erro: mensagem recebida não em um chat privado
error_nonprivate_chat = "⚠️ Este bot só funciona em chats privados."

# Erro: uma mensagem foi enviada em um chat, mas nenhum worker existe para esse chat.
# Sugere a criação de um novo worker com /start
error_no_worker_for_chat = "⚠️ A conversa com o bot foi interrompida.\n" \
                           "Para reiniciá-la, envie o comando /start para o bot."

# Erro: uma mensagem foi enviada em um chat, mas o worker para esse chat não está pronto.
error_worker_not_ready = "🕒 A conversa com o bot está iniciando no momento.\n" \
                         "Por favor, aguarde alguns momentos antes de enviar mais comandos!"

# Erro: valor de adição de fundos acima do máximo
error_payment_amount_over_max = "⚠️ O valor máximo que pode ser adicionado em uma única transação é {max_amount}."

# Erro: valor de adição de fundos abaixo do mínimo
error_payment_amount_under_min = "⚠️ O valor mínimo que pode ser adicionado em uma única transação é {min_amount}."

# Erro: a fatura expirou e não pode ser paga
error_invoice_expired = "⚠️ Esta fatura expirou e foi cancelada. Se você ainda deseja adicionar fundos, use a opção Adicionar fundos no menu."

# Erro: já existe um produto com esse nome
error_duplicate_name = "️⚠️ Já existe um produto com o mesmo nome."

# Erro: crédito insuficiente para fazer o pedido
error_not_enough_credit = "⚠️ Você não tem crédito suficiente para fazer o pedido."

# Erro: o pedido já foi processado
error_order_already_cleared = "⚠️ Este pedido já foi processado."

# Erro: nenhum pedido foi feito, então nenhum pode ser mostrado
error_no_orders = "⚠️ Você ainda não fez nenhum pedido, então não há nada para exibir."

# Erro: o usuário selecionado não existe
error_user_does_not_exist = "⚠️ O usuário selecionado não existe."

# Fatal: a conversa gerou uma exceção
fatal_conversation_exception = "☢️ Oh não! Um <b>erro</b> interrompeu esta conversa.\n" \
                               "O erro foi relatado ao proprietário do bot para que eles possam corrigi-lo.\n" \
                               "Para iniciar uma nova conversa, envie o comando /start novamente."
