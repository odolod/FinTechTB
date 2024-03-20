from telegram import Update
from telegram.ext import ContextTypes
from log import log
from database import save_user_symbol, save_user_interval, load_user_settings, load_chart_data, save_chart_data
from finance_yahoo_data import get_yahoo_symbol_name, get_yahoo_chart

async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'hello_command')
    await update.message.reply_text(f'Привет {update.effective_user.first_name} это бот для предсказания движения финансовых рынков')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'start_command')
    await update.message.reply_text(f'Команды:\n/hello\n/setInterval\n/setSymbol\n/settings\n/load\n/prediction\n/start')

async def set_interval_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'set_interval_command')
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

async def set_symbol_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'set_symbol_command')
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
    
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'settings_command')
    settings = load_user_settings(update.effective_user.id)
    if settings:
        await update.message.reply_text(f'Тикер:{settings["symbol"]} Интервал:{settings["interval"]}')
    else:
        await update.message.reply_text(f'Настройки не найдены. Установите:/setInterval\n/setSymbol')


async def load_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'load_command')
    settings = load_user_settings(update.effective_user.id)
    if settings:
        symbol = settings["symbol"]
        interval = settings["interval"]
        if symbol and interval:
            chart = get_yahoo_chart(symbol,interval)
            if chart:
                save_chart_data(symbol,interval,chart)
                await update.message.reply_text(f'Загрузка успешна.')
            else:
               await update.message.reply_text(f'Загрузка не удалась.')                 
        else:
            await update.message.reply_text(f'Проверьте настройки. Загрузка невозможна.')            
    else:
        await update.message.reply_text(f'Hастройки не найдены. Загрузка невозможна.')
    

async def prediction_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, 'prediction_command')
    await update.message.reply_text(f'TODO: сделать магию!')