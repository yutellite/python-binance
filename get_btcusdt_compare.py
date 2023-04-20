import pandas as pd
import mplfinance as mpf
from mplfinance import make_marketcolors, make_mpf_style
from binance.client import Client
from binance.enums import *

# 请填入自己的 API key 和 secret
api_key = 'kZlXOJYbnndBNpaSZrZpSTsmUSGcGW7MeBYVVMESriPyzN6o78Q2zxdj6VI014WS'
api_secret = 'ILa8lI59QwWe8sGOx7FIdhCeV88XAShiuBegyijSjxsR9M5piShuuzR4YqJEQrPy'

client = Client(api_key, api_secret)

# 获取所有交易对
tickers = client.get_all_tickers()

# 筛选出所有以 USDT 作为计价货币的交易对
usdt_pairs = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]

# 遍历所有 USDT 交易对并获取其蜡烛图数据
symbol='BTCUSDT'
print(f"Processing {symbol}...")

# 第一个时间段的起止时间
start_time1 = '2018-10-01 00:00:00'
end_time1 = '2019-10-31 23:59:59'

# 第二个时间段的起止时间
start_time2 = '2022-10-01 00:00:00'
end_time2 = '2023-10-31 23:59:59'

# 获取指定交易对的历史交易数据
pair = symbol

# 获取第一个时间段的 k 线数据
klines1 = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY,
 start_time1, end_time1)

# 获取第二个时间段的 k 线数据
klines2 = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY,
 start_time2, end_time2)

# 处理第 1 个时间段的 k 线数据为 dataframe 格式
df1 = pd.DataFrame(klines1, columns=[
  'timestamp', 'open', 'high', 'low', 'close',
  'volume', 'close_time', 'quote_asset_volume', 'trades',
  'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignored'
])

# 处理第 2 个时间段的 k 线数据为 dataframe 格式
df2 = pd.DataFrame(klines2, columns=[
  'timestamp', 'open', 'high', 'low', 'close',
  'volume', 'close_time', 'quote_asset_volume', 'trades',
  'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignored'
])

# 将 timestamp 列转换为日期格式
df1['timestamp'] = pd.to_datetime(df1['timestamp'], unit='ms')

# 将 Open、High、Low、Close 和 Volume 列中的值转换为浮点数类型
df1['open'] = df1['open'].astype(float)
df1['high'] = df1['high'].astype(float)
df1['low'] = df1['low'].astype(float)
df1['close'] = df1['close'].astype(float)
df1['volume'] = df1['volume'].astype(float)

# 将 timestamp 列转换为日期格式
df2['timestamp'] = pd.to_datetime(df2['timestamp'], unit='ms')

# 将 Open、High、Low、Close 和 Volume 列中的值转换为浮点数类型
df2['open'] = df2['open'].astype(float)
df2['high'] = df2['high'].astype(float)
df2['low'] = df2['low'].astype(float)
df2['close'] = df2['close'].astype(float)
df2['volume'] = df2['volume'].astype(float)

# 将 DataFrame 转换为 mplfinance 数据格式
data1 = df1.set_index('timestamp')
data1.index.name = 'Date'
data1.columns = [
  'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume',
  'Trades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignored'
]
data1 = data1[['Open', 'High', 'Low', 'Close', 'Volume']]

# 将 DataFrame 转换为 mplfinance 数据格式
data2 = df2.set_index('timestamp')
data2.index.name = 'Date'
data2.columns = [
  'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume',
  'Trades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignored'
]
data2 = data2[['Open', 'High', 'Low', 'Close', 'Volume']]

# 设置上涨和下跌的颜色
up_color = '#00ff00'  # 绿色
down_color = '#ff0000'  # 红色
marketcolors = mpf.make_marketcolors(up=up_color, down=down_color)

# 定义自定义颜色
mc = mpf.make_marketcolors(
    up='green', down='red',
    edge={'up': 'green', 'down': 'red'},
    wick={'up': 'green', 'down': 'red'},
    volume={'up': 'green', 'down': 'red'}
)

# 将自定义颜色传递给 mplfinance 风格字典
style = mpf.make_mpf_style(
    base_mpf_style='yahoo',
    marketcolors=mc
)

'''
# 假设 data1 和 data2 是两个 DataFrame，均包含 Open、High、Low、Close 和 Volume 列
# 将两个 DataFrame 按列合并
data = pd.concat([data1, data2], axis=1)
# 计算偏移量
offset = data2.index[0] - data1.index[0]
# 将 data1 的时间索引向后偏移 offset
data1.index += offset

# 将偏移后的 data1 和 data2 的列合并到一起
merged_data = pd.concat([data1, data2], axis=1, keys=['data1', 'data2'])

# 合并后的 DataFrame 会有重复的列名，需要重命名一下
# merged_data.columns = ['Open1', 'High1', 'Low1', 'Close1', 'Volume1',
#                'Open2', 'High2', 'Low2', 'Close2', 'Volume2']

merged_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 
                       'Open', 'High', 'Low', 'Close', 'Volume']

# 将 Open、High、Low、Close 和 Volume 列中的值转换为浮点数类型
merged_data['Open'] = merged_data['Open'].astype(float)
merged_data['High'] = merged_data['High'].astype(float)
merged_data['Low'] = merged_data['Low'].astype(float)
merged_data['Close'] = merged_data['Close'].astype(float)
merged_data['Volume'] = merged_data['Volume'].astype(float)

# 检查 data 是否是 DataFrame 类型
print(merged_data.head())
print(type(merged_data))
print(merged_data.columns)

# 将 Open、High、Low、Close 和 Volume 列中的值转换为浮点数类型
merged_data['Open1'] = merged_data['Open1'].astype(float)
merged_data['High1'] = merged_data['High1'].astype(float)
merged_data['Low1'] = merged_data['Low1'].astype(float)
merged_data['Close1'] = merged_data['Close1'].astype(float)
merged_data['Volume1'] = merged_data['Volume1'].astype(float)

# 将 Open、High、Low、Close 和 Volume 列中的值转换为浮点数类型
merged_data['Open2'] = merged_data['Open2'].astype(float)
merged_data['High2'] = merged_data['High2'].astype(float)
merged_data['Low2'] = merged_data['Low2'].astype(float)
merged_data['Close2'] = merged_data['Close2'].astype(float)
merged_data['Volume2'] = merged_data['Volume2'].astype(float)
'''
# 绘制蜡烛图 
# figratio 参数设置为 (16, 9)，表示图像宽度和高度的比例为 16:9。
# figsize 参数设置为 (19.2, 10.8)，表示图像的实际大小为 1920x1080，
# 设置分辨率为4096×2160
# 创建附加绘图对象ap，显示data1的蜡烛图数据，包括7、25和99日移动平均线和成交量
ap = mpf.make_addplot(data1, type='candle', mav=(7, 25, 99), 
                      title='Price History', ylabel='Price')

# 创建主图表格fig和ax，显示data2的蜡烛图数据，并将ap添加为附加绘图
fig, ax = mpf.plot(data1, type='candle', mav=(7, 25, 99), style=style,
                   title='Price History', ylabel='Price', volume=True,
                   figratio=(21, 9), figsize=(40.96, 21.6), returnfig=True,
                   addplot=ap)

# 将生成的图表保存为PNG格式的图像文件，文件名为"symbol_candle.png"
dpi = 440
fig.savefig('symbol_candle.png', dpi=dpi)

# 保存 csv 格式文件
#df.to_csv(f'{pair}.csv', index=False)
