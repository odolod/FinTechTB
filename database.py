import json
from pathlib import Path

# [{UserID, UserName, Interval, Symbol}]
settings_file = 'settings.json'
# [{symbol, interval, [chartData]}]
data_file = 'charts.json'

def read_json(filename: str) -> list:
    settigs = []
    with open(Path.cwd() / filename, 'r', encoding='utf-8') as fin:
        settigs = json.load(fin)
    return settigs

def write_json(filename: str,settigs: list):
    with open(Path.cwd() / filename, 'w', encoding='utf-8') as fout:
        fout.write(json.dumps(settigs) + '\n')

def save_user_interval(user_id, user_name, interval):
    settings = read_json(settings_file)
    user = {}
    for set in settings:
        if set["UserID"] == user_id:
            user = set
    if user:
        user["interval"] = interval
    else:
        settings.append({'UserID':user_id, 'UserName':user_name, 'interval':interval})
    write_json(settings_file,settings)

def save_user_symbol(user_id, user_name, symbol):
    settings = read_json(settings_file)
    user = {}
    for set in settings:
        if set["UserID"] == user_id:
            user = set
    if user:
        user["symbol"] = symbol
    else:
        settings.append({'UserID':user_id, 'UserName':user_name, 'symbol':symbol})
    write_json(settings_file,settings)

def save_chart_data(symbol, interval, chart_data):
    charts = read_json(data_file)
    symbol_data = {}
    for chart in charts:
        if chart["symbol"] == symbol and chart["interval"] == interval:
            symbol_data = chart
    if symbol_data:
        symbol_data["chartData"] = chart_data
    else:
        charts.append({'symbol':symbol, 'interval':interval, 'chartData':chart_data})
    write_json(data_file,charts)

def load_chart_data(symbol, interval):
    charts = read_json(data_file)
    symbol_data = {}
    for chart in charts:
        if chart["symbol"] == symbol and chart["interval"] == interval:
            symbol_data = chart
    return symbol_data

def load_user_settings(user_id):
    settings = read_json(settings_file)
    user = {}
    for set in settings:
        if set["UserID"] == user_id:
            user = set
    return user

#print(load_user_settings(404180238))