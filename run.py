from flask import Flask
from admin_panel import app as admin_app
from telegram_bot import main as run_telegram_bot
import threading

app = Flask(__name__)
app.register_blueprint(admin_app, url_prefix='/admin')

if __name__ == '__main__':
    # 在單獨的線程中運行Telegram機器人
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.start()

    # 運行Flask應用
    app.run(debug=True, use_reloader=False)