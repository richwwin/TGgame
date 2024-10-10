from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from game_logic import game_logic
from payment import process_payment

TOKEN = 'your_telegram_bot_token'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="歡迎來到太空爪子遊戲!")

def grab(update, context):
    user_id = update.effective_user.id
    grab_type = context.args[0] if context.args else 'one'
    
    payment_amount = {
        'one': 100,
        'five': 500,
        'ten': 1000
    }.get(grab_type)
    
    if not payment_amount:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="請選擇有效的抓取類型：one, five, 或 ten")
        return

    payment_id = process_payment(user_id, payment_amount)
    if not payment_id:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="支付失敗,請稍後再試")
        return

    results = game_logic.calculate_grab_result(user_id, grab_type)
    if results:
        message = f"恭喜! 您抓到了 {len(results)} 個獎品:\n"
        for prize in results:
            message += f"- {prize['name']}\n"
    else:
        message = "哎呀，看來今天運氣不太好。但別灰心，再來一次肯定能抓到好東西！"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("grab", grab))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()