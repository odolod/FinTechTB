from telegram import Update
from datetime import datetime

def log(update: Update, command) -> None:
    file = open('logdb.csv','a')
    file.write(f'{command}, {datetime.now()}, {update.effective_user.id}, {update.effective_user.first_name}, {update.message.text}\n')
