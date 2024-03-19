import requests
from fake_useragent import UserAgent
import json

headers = {"User-Agent": UserAgent().chrome}
cookie = None
crumb = None

def get_yahoo_cookie():
    cookie = None
    response = requests.get(
        "https://fc.yahoo.com", headers=headers, allow_redirects=True
    )
    if not response.cookies:
        raise Exception("Failed to obtain Yahoo auth cookie.")
    cookie = list(response.cookies)[0]
    return cookie

def get_yahoo_crumb(cookie):
    crumb = None
    crumb_response = requests.get(
        "https://query1.finance.yahoo.com/v1/test/getcrumb",
        headers=headers,
        cookies={cookie.name: cookie.value},
        allow_redirects=True,
    )
    crumb = crumb_response.text
    if crumb is None:
        raise Exception("Failed to retrieve Yahoo crumb.")
    return crumb

def check_crumb():
    global crumb
    global cookie
    if not crumb:
        cookie = get_yahoo_cookie()
        crumb = get_yahoo_crumb(cookie)

#Запрос данных по символу 
#https://query2.finance.yahoo.com/v7/finance/quote?symbols=TSLA&crumb=[crumb-value]
def get_yahoo_quote(symbol):
    check_crumb()
    params = {
        "symbols": symbol,
        "crumb": crumb,
    }

    quote_response = requests.get(
        "https://query2.finance.yahoo.com/v7/finance/quote",
        headers=headers,
        cookies={cookie.name: cookie.value},
        params=params,
        allow_redirects=True,
    )
    quote = quote_response.text

    if quote is None:
        raise Exception("Failed to retrieve Yahoo quote.")

    return quote

def get_yahoo_symbol_name(symbol):
    quote = get_yahoo_quote(symbol)
    name = None
    try:
        data = json.loads(quote)
        name = data["quoteResponse"]["result"][0]["shortName"]
    except Exception:
        name = None

    return name    

#https://query1.finance.yahoo.com/v8/finance/chart/GOOGL?symbol=AAPL&period1=0&period2=9999999999&interval=1d
#"validRanges":["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]}
def get_yahoo_chart(symbol, interval):
    check_crumb()
    params = {
        "crumb": crumb,
        "interval": interval,
        "period1": 0,
        "period2": 9999999999
    }

    chart_response = requests.get(
        "https://query1.finance.yahoo.com/v8/finance/chart/"+symbol,
        headers=headers,
        cookies={cookie.name: cookie.value},
        params=params,
        allow_redirects=True,
    )
    chart = chart_response.text

    if chart is None:
        raise Exception("Failed to retrieve Yahoo quote.")

    return chart

# Usage
#cookie = get_yahoo_cookie()
#crumb = get_yahoo_crumb(cookie)
#quote = get_yahoo_quote('GAZP.ME')
#chart = get_yahoo_chart('GAZP.ME',"3mo",crumb,cookie)

#print(get_yahoo_symbol_name('GAZP.ME'))

