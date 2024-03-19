from telegram import Update
from telegram.ext import ContextTypes
from log import log
from data_generator import generate
from database import read_json, write_csv, write_json

async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'hello_command')
    await update.message.reply_text(f'Привет {update.effective_user.first_name} это бот для предсказания движения финансовых рынков')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'start_command')
    await update.message.reply_text(f'Команды:\n/hello\n/setPeriod\n/settigs\n/setSymbol\n/finds\n/add\n/delete\n/update\n/start')

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'generate_command')
    msg = update.message.text
    items = msg.split()
    n = int(items[1])
    if n != 0: generate(n)
    await update.message.reply_text(f'Сгенерировано {n} сотрудников')

async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'find_command')
    items = update.message.text.split()
    find = items[1] # строка для поиска
    employees = read_json()
    for i in employees:
        for j in i.values():
            if find in str(j): await update.message.reply_text(f'{i}') 

async def findp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'findp_command')
    items = update.message.text.split()
    find = items[1] # должность
    employees = read_json()
    for i in employees:
        if find in str(i['position']): await update.message.reply_text(f'{i}') 

async def finds_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'finds_command')
    items = update.message.text.split()
    employees = read_json()
    l = float(items[1]) # нижний уровень зарплаты
    h = float(items[2]) # верхний уровень зарплаты
    for i in employees:
        if l < i['salary'] and h > i['salary']: await update.message.reply_text(f'{i}') 

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'add_command')
    items = update.message.text.split()
    id = int(items[1])
    last_name = items[2]
    first_name = items[3]
    position = items[4]
    phone_number = items[5]
    salary = float(items[6])
    employees = read_json()
    employees.append({'id': id, 'last_name': last_name, 'first_name': first_name, 'position': position, 'phone_number': phone_number, 'salary': salary})
    write_json(employees)
    write_csv(employees)
    await update.message.reply_text(f'Сотрудник добавлен')

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'delete_command')
    items = update.message.text.split()
    id = int(items[1])
    employees = read_json()
    for i in employees:
        if id == i['id']: employees.remove(i)
    write_json(employees)
    write_csv(employees)
    await update.message.reply_text(f'Сотрудник удален')

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'update_command')
    items = update.message.text.split()
    id = int(items[1])
    last_name = items[2]
    first_name = items[3]
    position = items[4]
    phone_number = items[5]
    salary = float(items[6])
    employees = read_json()
    for i in employees:
        if id == i['id']: i.update({'id': id, 'last_name': last_name, 'first_name': first_name, 'position': position, 'phone_number': phone_number, 'salary': salary})
    write_json(employees)
    write_csv(employees)
    await update.message.reply_text(f'Сотрудник изменен')