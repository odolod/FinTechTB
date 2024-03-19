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
app.add_handler(CommandHandler("generate", generate_command))
app.add_handler(CommandHandler("find", find_command))
app.add_handler(CommandHandler("findp", findp_command))
app.add_handler(CommandHandler("finds", finds_command))
app.add_handler(CommandHandler("add", add_command))
app.add_handler(CommandHandler("delete", delete_command))
app.add_handler(CommandHandler("update", update_command))

app.run_polling()