import pandas as pd
import mplfinance as mpf
from mplfinance import make_marketcolors, make_mpf_style
from binance.client import Client
from binance.enums import *
import matplotlib.pyplot as plt

# 请填入自己的 API key 和 secret
api_key = 'kZlXOJYbnndBNpaSZrZpSTsmUSGcGW7MeBYVVMESriPyzN6o78Q2zxdj6VI014WS'
api_secret = 'ILa8lI59QwWe8sGOx7FIdhCeV88XAShiuBegyijSjxsR9M5piShuuzR4YqJEQrPy'

client = Client(api_key, api_secret)

# 获取所有 USDT 交易对的交易信息
exchange_info = client.get_exchange_info()
symbols = exchange_info['symbols']
usdt_pairs = [symbol['symbol'] for symbol in symbols if symbol['quoteAsset'] == 'USDT']

# 获取 2019 年的历史 K 线数据
start_date = '2019-01-01'
end_date = '2020-01-01'
interval = Client.KLINE_INTERVAL_1DAY
df_list = []
for pair in usdt_pairs:
    klines = client.get_historical_klines(pair, interval, start_date, end_date)
    data = [[pd.to_datetime(kline[0], unit='ms'), float(kline[1]), float(kline[4])] for kline in klines]
    df = pd.DataFrame(data, columns=['date', 'open', 'close'])
    df['pair'] = pair
    df_list.append(df)

# 计算每个交易对的涨幅
df = pd.concat(df_list)
df['change'] = (df['close'] - df['open']) / df['open'] * 100

# 找出涨幅最大的交易对
max_change_pair = df.loc[df['change'].idxmax()]

print(max_change_pair)
