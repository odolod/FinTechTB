import json
from pathlib import Path

# UserID, UserName, Interval, Symbol
settigs_file = 'settigs.json'

def read_settigs() -> list:
    settigs = []
    with open(Path.cwd() / settigs_file, 'r', encoding='utf-8') as fin:
        settigs = json.load(fin)
    return settigs

def write_settigs(settigs: list):
    with open(Path.cwd() / settigs_file, 'w', encoding='utf-8') as fout:
        fout.write(json.dumps(settigs) + '\n')

def save_user_interval(user_id, user_name, interval):
    settings = read_settigs()
    user = {}
    for set in settings:
        if set["UserID"] == user_id:
            user = set
    if user:
        user["interval"] = interval
    else:
        settings.append({'UserID':user_id, 'UserName':user_name, 'interval':interval})
    write_settigs(settings)

def save_user_symbol(user_id, user_name, symbol):
    settings = read_settigs()
    user = {}
    for set in settings:
        if set["UserID"] == user_id:
            user = set
    if user:
        user["symbol"] = symbol
    else:
        settings.append({'UserID':user_id, 'UserName':user_name, 'symbol':symbol})
    write_settigs(settings)