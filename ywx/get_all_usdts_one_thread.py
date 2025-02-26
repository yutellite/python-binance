import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

from binance.client import Client

# 请填入自己的 API key 和 secret
api_key = 'kZlXOJYbnndBNpaSZrZpSTsmUSGcGW7MeBYVVMESriPyzN6o78Q2zxdj6VI014WS'
api_secret = 'ILa8lI59QwWe8sGOx7FIdhCeV88XAShiuBegyijSjxsR9M5piShuuzR4YqJEQrPy'

client = Client(api_key, api_secret)

# 获取所有交易对
tickers = client.get_all_tickers()

# 筛选出所有以 USDT 作为计价货币的交易对
usdt_pairs = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]

# 遍历所有 USDT 交易对并获取其蜡烛图数据
for ticker in usdt_pairs:
    symbol = ticker['symbol']
    print(f"Processing {symbol}...")
    each_pair_symbol = ticker['symbol']


    # 获取指定交易对的历史交易数据
    pair = each_pair_symbol
    klines = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, "1 Jan, 2020", "now")
    if not len(klines):
      continue
    df = pd.DataFrame(klines, columns=[
      'timestamp', 'open', 'high', 'low', 'close',
      'volume', 'close_time', 'quote_asset_volume', 'trades',
      'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignored'
    ])

    # 将 timestamp 列转换为日期格式
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # 将 Open、High、Low、Close 和 Volume 列中的值转换为浮点数类型
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    # 将 DataFrame 转换为 mplfinance 数据格式
    data = df.set_index('timestamp')
    data.index.name = 'Date'
    data.columns = [
      'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume',
      'Trades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignored'
    ]
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

    # 绘制蜡烛图 
    # figratio 参数设置为 (16, 9)，表示图像宽度和高度的比例为 16:9。
    # figsize 参数设置为 (19.2, 10.8)，表示图像的实际大小为 1920x1080，
    # 设置分辨率为1920*1080
    fig, ax = mpf.plot(data, type='candle', mav=(5, 10), 
            title=pair + ' Price History', ylabel='Price',
            volume=True, figratio=(16, 9), figsize=(19.2, 10.8), returnfig=True)

    # dpi 参数设置为 100，表示图像的每英寸点数为 100。
    dpi = 100
    fig.savefig(each_pair_symbol+'_candle.png', dpi=dpi)

    # 保存 csv 格式文件
    #df.to_csv(f'{pair}.csv', index=False)
