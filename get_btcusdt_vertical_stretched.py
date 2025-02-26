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

# 获取所有交易对
tickers = client.get_all_tickers()

# 筛选出所有以 USDT 作为计价货币的交易对
usdt_pairs = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]

# 遍历所有 USDT 交易对并获取其蜡烛图数据
#symbol='BTCUSDT'
symbol='FILUSDT'
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
# klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY,
# start_time1, end_time1)

# 获取第二个时间段的 k 线数据
klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY,
  start_time1, "now")

# klines = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, "1 Jan, 2022", "now")
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

# 绘制蜡烛图 
# figratio 参数设置为 (16, 9)，表示图像宽度和高度的比例为 16:9。
# figsize 参数设置为 (19.2, 10.8)，表示图像的实际大小为 1920x1080，
# 设置分辨率为4096×2160
fig, ax = mpf.plot(data, type='candle', mav=(7, 25, 99), style=style, 
        title=pair + ' Price History', ylabel='Price',
        volume=True, figratio=(21, 9), figsize=(40.96, 21.6), returnfig=True)

# dpi 参数设置为 1000，表示图像的每英寸点数为 100。
dpi = 440
fig.savefig(symbol+'_2.png', dpi=dpi)

# 保存 csv 格式文件
#df.to_csv(f'{pair}.csv', index=False)

def plot_candlestick(data):
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    mpf.candlestick2_ochl(ax, data['Open'], data['Close'], data['High'], data['Low'], width=0.5, colorup='r', colordown='g', alpha=0.6)

    def on_scroll(event):
        # 获取当前y轴范围
        ymin, ymax = ax.get_ylim()
        # 获取滚轮滚动方向，向上滚动为1，向下滚动为-1
        direction = 1 if event.button == 'up' else -1
        # 计算纵轴范围的新值
        dy = (ymax - ymin) * 0.1 * direction
        ymin_new = ymin - dy
        ymax_new = ymax + dy
        # 更新y轴范围
        ax.set_ylim(ymin_new, ymax_new)
        # 重新绘制图形
        fig.canvas.draw()

    # 注册滚轮事件处理函数
    fig.canvas.mpl_connect('scroll_event', on_scroll)
    
    plt.show()