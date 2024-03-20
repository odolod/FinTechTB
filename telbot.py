from telegram.ext import ApplicationBuilder, CommandHandler
from bot_commands import *
import os
from dotenv import load_dotenv

#Токен телеграмм бота
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.getenv("TGBOT_TOKEN")

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello_command))
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("setInterval", set_interval_command))
app.add_handler(CommandHandler("setSymbol", set_symbol_command))
app.add_handler(CommandHandler("settings", settings_command))
app.add_handler(CommandHandler("load", load_command))
app.add_handler(CommandHandler("prediction", prediction_command))

app.run_polling()