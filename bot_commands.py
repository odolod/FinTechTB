from telegram import Update
from telegram.ext import ContextTypes
from log import log
from database import save_user_symbol, save_user_interval
from finance_yahoo_data import get_yahoo_symbol_name

async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'hello_command')
    await update.message.reply_text(f'Привет {update.effective_user.first_name} это бот для предсказания движения финансовых рынков')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'start_command')
    await update.message.reply_text(f'Команды:\n/hello\n/setInterval\n/settigs\n/setSymbol\n/finds\n/add\n/delete\n/update\n/start')

async def set_interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'set_interval')
    items = update.message.text.split()
    interval = "1d" # интервал
    valid_interval = ["1d","5d","1mo","3mo"]
    try:
        interval = items[1] # интервал
    except Exception:
        await update.message.reply_text(f'Интервал не задан, берем по умолчанию 1d')
    else:
        if interval in valid_interval:   
            await update.message.reply_text(f'Интервал {interval} установлен')
        else:
            await update.message.reply_text(f'Интервал {interval} неверный, допустимые: 1d, 5d, 1mo, 3mo, установлен 1d')
            interval = "1d"
    finally:
        #Записываем данные интервала для пользователя.
        save_user_interval(update.effective_user.id, update.effective_user.first_name, interval)

async def set_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'set_symbol')
    items = update.message.text.split()
    symbol = "TSLA" # тикер на https://finance.yahoo.com/trending-tickers
    try:
        symbol = items[1] # тикер
    except Exception:
        await update.message.reply_text(f'Тикер не задан, берем по умолчанию TSLA')
    else:
        name = get_yahoo_symbol_name(symbol)
        if name:   
            await update.message.reply_text(f'Тикер {symbol} ({name}) установлен')
        else:
            await update.message.reply_text(f'Тикер {symbol} неверный, допустимые: https://finance.yahoo.com/trending-tickers, установлен TSLA')
            symbol = "TSLA"
    finally:
        #Записываем данные тикера для пользователя.
        save_user_symbol(update.effective_user.id, update.effective_user.first_name, symbol)
    
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