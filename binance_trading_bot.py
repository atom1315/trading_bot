import time
import requests
from binance.futures import FuturesClient
from tradingview_ta import TA_Handler, Interval, Exchange

INTERVAL = Interval.INTERVAL_15_MINUTES
TELEGRAM_TOKEN = 'number tocken'
TELEGRAM_CHANNEL = 'name chanel'

client = FuturesClient(api_key, api_secret)

def get_data(symbol):
    output = TA_Handler(symbol=symbol,
                        screener='Crypto',
                        exchange='Binance',
                        interval=INTERVAL)
    activiti = output.get_analysis().summary
    activiti['SYMBOL'] = symbol
    return activiti

# Spisok simvolov pokazivaet vse screener
def get_symbols():
    tickers = client.mark_price()
    symbols = []
    for i in tickers:
        ticker = i['symbol']
        symbols.append(ticker)
    return symbols

def send_message(text):
    try:
        res = requests.get('https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN), params=dict(
            chat_id=TELEGRAM_CHANNEL, text=text))
    except:
        print('Error sending message to Telegram')

def first_data():
    print('Search first data')
    send_message('Search first data')
    long = []
    shorts = []
    symbols = get_symbols()
    for i in symbols:
        try:
            data = get_data(i)
            #print(data)
            if (data['RECOMMENDATION'] == 'STRONG_BUY'):
                long.append(data['SYMBOL'])
                # print(data['SYMBOL'], 'Buy')

            if (data['RECOMMENDATION'] == 'STRONG_SELL'):
                shorts.append(data['SYMBOL'])
            time.sleep(0.01)
        except:
            pass
    print('longs:')
    print(long)
    print('shorts:')
    print(shorts)
    return long, shorts

print('Start')
send_message('Start')
longs, shorts = first_data()

while True:
    print('______________________NEW ROUND____________________')
    symbols = get_symbols()
    for i in symbols:
        try:
            data = get_data(i)
            # print(data)
            if (data['RECOMMENDATION'] == 'STRONG_BUY' and (data['SYMBOL'] not in longs)):
                print(data['SYMBOL'], 'Buy')
                text = data['SYMBOL'] + ' BUY'
                send_message(text)
                longs.append(data['SYMBOL'])

            if (data['RECOMMENDATION'] == 'STRONG_SELL' and (data['SYMBOL'] not in shorts)):
                print(data['SYMBOL'], 'Sell')
                text = data['SYMBOL'] + ' SELL'
                send_message(text)

        except:
            pass
        time.sleep(0.01)