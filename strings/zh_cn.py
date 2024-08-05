# greed 的字符串/本地化文件
# 可以编辑，但不要删除替换字段（被{大括号}包围的单词）
# 当前本地化：简体中文

# 货币符号
currency_symbol = "¥"

# 货币符号的位置
currency_format_string = "{symbol}{value}"

# 产品库存数量
in_stock_format_string = "库存：{quantity}"

# 购物车中的产品数量
in_cart_format_string = "购物车：{quantity}"

# 产品信息
product_format_string = "<b>{name}</b>\n" \
                        "{description}\n" \
                        "{price}\n" \
                        "<b>{cart}</b>"

# 订单号，显示在订单信息中
order_number = "订单 #{id}"

# 订单信息字符串，显示给管理员
order_format_string = "来自 {user}\n" \
                      "创建于 {date}\n" \
                      "\n" \
                      "{items}\n" \
                      "总计：<b>{value}</b>\n" \
                      "\n" \
                      "客户备注：{notes}\n"

# 订单信息字符串，显示给用户
user_order_format_string = "{status_emoji} <b>订单 {status_text}</b>\n" \
                           "{items}\n" \
                           "总计：<b>{value}</b>\n" \
                           "\n" \
                           "备注：{notes}\n"

# 交易页面正在加载
loading_transactions = "<i>正在加载交易...\n" \
                       "请稍等几秒钟。</i>"

# 交易页面
transactions_page = "第 <b>{page}</b> 页：\n" \
                    "\n" \
                    "{transactions}"

# transactions.csv 标题
csv_caption = "已生成包含机器人数据库中所有交易的 📄 .csv 文件。\n" \
              "您可以使用其他程序（如 LibreOffice Calc）打开此文件以处理数据。"

# 对话：发送了 start 命令，机器人应该欢迎用户
conversation_after_start = "你好！\n" \
                           "欢迎使用 greed！\n" \
                           "这是软件的 🅱️ <b>测试版</b>。\n" \
                           "它完全可用，但可能还存在一些错误。\n" \
                           "如果您发现任何错误，请在 https://github.com/Steffo99/greed/issues 上报告。"

# 对话：要发送内联键盘，您需要发送一条带有它的消息
conversation_open_user_menu = "您想做什么？\n" \
                              "💰 您的钱包中有 <b>{credit}</b>。\n" \
                              "\n" \
                              "<i>按下底部键盘上的按钮来选择操作。\n" \
                              "如果键盘没有打开，您可以通过按消息栏中带有四个小方块的按钮来打开它。</i>"

# 对话：如上所述，但针对管理员
conversation_open_admin_menu = "您是这家商店的 💼 <b>管理员</b>！\n" \
                               "您想做什么？\n" \
                               "\n" \
                               "<i>按下底部键盘上的按钮来选择操作。\n" \
                               "如果键盘没有打开，您可以通过按消息栏中带有四个小方块的按钮来打开它。</i>"

# 对话：选择支付方式
conversation_payment_method = "您想如何向钱包添加资金？"

# 对话：选择要编辑的产品
conversation_admin_select_product = "✏️ 您想编辑哪个产品？"

# 对话：选择要删除的产品
conversation_admin_select_product_to_delete = "❌ 您想删除哪个产品？"

# 对话：选择要编辑的用户
conversation_admin_select_user = "选择要对其执行所选操作的用户。"

# 对话：点击下方支付购买
conversation_cart_actions = "<i>通过向上滚动并按下您想购买的产品下方的添加按钮来将产品添加到购物车。完成后，返回此消息并按下完成按钮。</i>"

# 对话：确认购物车内容
conversation_confirm_cart = "🛒 您的购物车包含以下产品：\n" \
                            "{product_list}" \
                            "总计：<b>{total_cost}</b>\n" \
                            "\n" \
                            "<i>按下此消息下方的完成按钮继续。\n" \
                            "要取消，请按取消按钮。</i>"

# 实时订单模式：开始
conversation_live_orders_start = "您正处于<b>实时订单</b>模式！\n" \
                                 "客户下的所有新订单都会实时出现在此聊天中，您可以将它们标记为 ✅ 已完成" \
                                 "或 ✴️ 退款给客户。"

# 实时订单模式：停止接收消息
conversation_live_orders_stop = "<i>按下此消息下方的停止按钮以停止接收实时订单。</i>"

# 对话：帮助菜单已打开
conversation_open_help_menu = "您需要什么帮助？"

# 对话：确认升级为管理员
conversation_confirm_admin_promotion = "您确定要将此用户提升为 💼 管理员吗？\n" \
                                       "这是一个不可逆的操作！"

# 对话：语言选择菜单标题
conversation_language_select = "选择一种语言："

# 对话：切换到用户模式
conversation_switch_to_user_mode = "您正在切换到 👤 客户模式。\n" \
                                   "如果您想返回 💼 管理员模式，请使用 /start 重新启动对话。"

# 通知：对话已过期
conversation_expired = "🕐 我已经有一段时间没有收到任何消息了，所以为了节省能源，" \
                       "我关闭了对话。\n" \
                       "如果您想开始新的对话，请再次发送 /start 命令。"

# 用户菜单：订单
menu_order = "🛒 下单"

# 用户菜单：订单状态
menu_order_status = "🛍 我的订单"

# 用户菜单：添加资金
menu_add_credit = "💵 添加资金"

# 用户菜单：机器人信息
menu_bot_info = "ℹ️ 机器人信息"

# 用户菜单：现金
menu_cash = "💵 现金"

# 用户菜单：信用卡
menu_credit_card = "💳 信用卡"

# 管理员菜单：产品
menu_products = "📝️ 产品"

# 管理员菜单：订单
menu_orders = "📦 订单"

# 菜单：交易
menu_transactions = "💳 交易列表"

# 菜单：编辑信用
menu_edit_credit = "💰 创建交易"

# 管理员菜单：切换到用户模式
menu_user_mode = "👤 切换到客户模式"

# 管理员菜单：添加产品
menu_add_product = "✨ 新产品"

# 管理员菜单：删除产品
menu_delete_product = "❌ 删除产品"

# 菜单：取消
menu_cancel = "🔙 取消"

# 菜单：返回
menu_go_back = "🔙 返回"

# 菜单：跳过
menu_skip = "⏭ 跳过"

# 菜单：完成
menu_done = "✅️ 完成"

# 菜单：支付发票
menu_pay = "💳 支付"

# 菜单：完成
menu_complete = "✅ 完成"

# 菜单：退款
menu_refund = "✴️ 退款"

# 菜单：停止
menu_stop = "🛑 停止"

# 菜单：添加到购物车
menu_add_to_cart = "➕ 添加"

# 菜单：从购物车移除
menu_remove_from_cart = "➖ 移除"

# 菜单：帮助菜单
menu_help = "❓ 帮助和支持"

# 菜单：指南
menu_guide = "📖 指南"

# 菜单：下一页
menu_next = "▶️ 下一页"

# 菜单：上一页
menu_previous = "◀️ 上一页"

# 菜单：联系店主
menu_contact_shopkeeper = "👨‍💼 联系商店"

# 菜单：生成交易 .csv 文件
menu_csv = "📄 .csv"

# 菜单：编辑管理员列表
menu_edit_admins = "🏵 编辑管理员"

# 菜单：语言
menu_language = "🇨🇳 语言"

# 表情：未处理订单
emoji_not_processed = "*️⃣"

# 表情：已完成订单
emoji_completed = "✅"

# 表情：已退款订单
emoji_refunded = "✴️"

# 表情：是
emoji_yes = "✅"

# 表情：否
emoji_no = "🚫"

# 文本：未处理订单
text_not_processed = "处理中"

# 文本：已完成订单
text_completed = "已完成"

# 文本：已退款订单
text_refunded = "已退款"

# 添加产品：类别？
ask_product_category = "产品应属于哪个类别？"

# 添加产品：名称？
ask_product_name = "产品的名称应该是什么？"

# 添加产品：描述？
ask_product_description = "产品的描述应该是什么？"

# 添加产品：价格？
ask_product_price = "产品的价格应该是多少？\n" \
                    "如果您希望产品尚未出售，请输入 <code>X</code>。"

# 添加产品：尚未出售文本
not_for_sale_yet = "尚未出售"

# 添加产品：图片？
ask_product_image = "🖼 您希望产品使用什么图片？\n" \
                    "\n" \
                    "<i>发送一张照片，或如果您希望产品没有图片，请按下方的跳过按钮。</i>"

# 添加类别：名称？
ask_category_name = "类别的名称应该是什么？"

# 订购产品：备注？
ask_order_notes = "您想为订单留下备注吗？\n" \
                  "💼 这将对商店管理员可见。\n" \
                  "\n" \
                  "<i>发送一条包含您想留下的备注的消息，或按此消息下方的跳过按钮不留下任何内容。</i>"

# 退款产品：原因？
ask_refund_reason = "为这次退款附加一个原因。\n" \
                    "👤 这将对客户可见。"

# 编辑信用：备注？
ask_transaction_notes = "为这笔交易附加一个备注。\n" \
                        "👤 这将在信用/借记后对客户可见" \
                        "并对 💼 管理员在交易日志中可见。"

# 编辑信用：金额？
ask_credit = "您想更改客户的信用额度多少？\n" \
             "\n" \
             "<i>发送一条包含金额的消息。\n" \
             "使用 </i><code>+</code><i> 符号向客户账户添加信用，" \
             "或使用 </i><code>-</code><i> 符号扣除信用。</i>"

# 编辑管理员消息的标题
admin_properties = "<b>{name} 的权限：</b>"

# 编辑管理员：可以编辑产品？
prop_edit_products = "编辑产品"

# 编辑管理员：可以编辑类别？
prop_edit_categories = "编辑类别"

# 编辑管理员：可以接收订单？
prop_receive_orders = "接收订单"

# 编辑管理员：可以创建交易？
prop_create_transactions = "管理交易"

# 编辑管理员：在帮助消息中显示？
prop_display_on_help = "客户支持"

# 线程已开始下载图片，可能无响应
downloading_image = "我正在下载您的照片！\n" \
                    "这可能需要一些时间... 请耐心等待！\n" \
                    "在下载过程中我将无法回复您。"

# 编辑产品：当前值
edit_current_value = "当前值为：\n" \
                     "<pre>{value}</pre>\n" \
                     "\n" \
                     "<i>按此消息下方的跳过按钮保持相同的值。</i>"

# 支付：现金支付信息
payment_cash = "您可以在实体店以现金支付。\n" \
               "在收银台付款，并向店主提供此 ID：\n" \
               "<b>{user_cash_id}</b>"

# 用户菜单：信用历史
menu_credit_history = "📈 信用历史"

# 用户菜单：输入促销码
menu_promocode = "🤩 输入促销码"

# 询问促销码
ask_promocode = "输入促销码："

# 促销码已应用
promocode_applied = "促销码已应用！"

# 无效促销码
promocode_invalid = "无效的促销码。"

# 用户菜单：个人资料
menu_profile = "🧾 个人资料"

# 信用历史为空
credit_history_null = "您还没有进行任何充值！"

# 信用历史
credit_history = "您的充值历史："

# 支付：信用卡金额
payment_cc_amount = "您想向钱包添加多少资金？\n" \
                    "\n" \
                    "<i>使用下方按钮选择金额，或使用普通键盘手动输入。</i>"

# 支付：添加资金发票标题
payment_invoice_title = "添加资金"

# 支付：添加资金发票描述
payment_invoice_description = "支付此发票将向您的钱包添加 {amount}。"

# 支付：发票上标记价格的标签
payment_invoice_label = "充值"

# 支付：发票上手续费的标签
payment_invoice_fee_label = "卡费"

# 通知：订单已下达
notification_order_placed = "已下达新订单：\n" \
                            "{order}"

# 通知：订单已完成
notification_order_completed = "您的订单已完成！\n" \
                               "{order}"

# 通知：订单已退款
notification_order_refunded = "您的订单已退款！\n" \
                              "{order}"

# 通知：已应用手动交易
notification_transaction_created = "ℹ️ 已向您的钱包应用新交易：\n" \
                                   "{transaction}"

# 退款原因
refund_reason = "退款原因：\n" \
                "{reason}"

# 信息：关于机器人的信息
bot_info = '此机器人使用 <a href="https://github.com/Steffo99/greed">greed</a>，' \
           '这是由 @Steffo 开发的 Telegram 支付框架，根据' \
           ' <a href="https://github.com/Steffo99/greed/blob/master/LICENSE.txt">' \
           'Affero 通用公共许可证 3.0</a> 发布。\n'

# 帮助：指南
help_msg = "关于如何使用此机器人的指南可在以下地址获得：\n" \
           "https://docs.google.com/document/d/1f4MKVr0B7RSQfWTSa_6ZO0LM4nPpky_GX_qdls3EHtQ/"

# 帮助：联系店主
contact_shopkeeper = "目前可提供用户帮助的工作人员包括：\n" \
                     "{shopkeepers}\n" \
                     "<i>点击/触摸其中一个名字以在 Telegram 聊天中联系他们。</i>"

# 成功：产品已添加/编辑到数据库
success_product_edited = "✅ 产品已成功添加/修改！"

# 成功：产品已从数据库删除
success_product_deleted = "✅ 产品已成功删除！"

# 成功：订单已创建
success_order_created = "✅ 订单已成功发送！\n" \
                        "\n" \
                        "{order}"

# 成功：订单已标记为完成
success_order_completed = "✅ 您已将订单 #{order_id} 标记为完成。"

# 成功：订单已成功退款
success_order_refunded = "✴️ 订单 #{order_id} 已成功退款。"

# 成功：交易已成功创建
success_transaction_created = "✅ 交易已成功创建！\n" \
                              "{transaction}"

# 错误：消息未在私人聊天中接收
error_nonprivate_chat = "⚠️ 此机器人仅在私人聊天中工作。"

# 错误：在聊天中发送了消息，但该聊天没有工作进程。
# 建议使用 /start 创建新的工作进程
error_no_worker_for_chat = "⚠️ 与机器人的对话已中断。\n" \
                           "要重新开始，请向机器人发送 /start 命令。"

# 错误：在聊天中发送了消息，但该聊天的工作进程尚未就绪。
error_worker_not_ready = "🕒 与机器人的对话正在初始化。\n" \
                         "请等待几秒钟后再发送更多命令！"

# 错误：添加资金金额超过最大值
error_payment_amount_over_max = "⚠️ 单笔交易可添加的最大金额为 {max_amount}。"

# 错误：添加资金金额低于最小值
error_payment_amount_under_min = "⚠️ 单笔交易可添加的最小金额为 {min_amount}。"

# 错误：发票已过期且无法支付
error_invoice_expired = "⚠️ 此发票已过期并被取消。如果您仍想添加资金，请使用菜单中的添加资金选项。"

# 错误：已存在同名产品
error_duplicate_name = "️⚠️ 已存在同名产品。"

# 错误：信用不足以下单
error_not_enough_credit = "⚠️ 您没有足够的信用来下单。"

# 错误：订单已经处理完毕
error_order_already_cleared = "⚠️ 此订单已经处理完毕。"

# 错误：尚未下过订单，因此无法显示
error_no_orders = "⚠️ 您尚未下过任何订单，因此没有可显示的内容。"

# 错误：所选用户不存在
error_user_does_not_exist = "⚠️ 所选用户不存在。"

# 致命错误：对话引发异常
fatal_conversation_exception = "☢️ 哎呀！一个<b>错误</b>中断了这次对话。\n" \
                               "错误已报告给机器人所有者，以便他们修复。\n" \
                               "要开始新的对话，请再次发送 /start 命令。"
