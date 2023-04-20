import mplfinance as mpf
from binance.client import Client
import matplotlib.pyplot as plt
import pandas as pd

# Set up Binance API client
# 请填入自己的 API key 和 secret
api_key = 'kZlXOJYbnndBNpaSZrZpSTsmUSGcGW7MeBYVVMESriPyzN6o78Q2zxdj6VI014WS'
api_secret = 'ILa8lI59QwWe8sGOx7FIdhCeV88XAShiuBegyijSjxsR9M5piShuuzR4YqJEQrPy'

client = Client(api_key, api_secret)

# Get k-lines for BTCUSDT
symbol = 'BTCUSDT'
interval = '1d'

# 第一个时间段的起止时间
start_time = '2018-10-01 00:00:00'
end_time = 'now'

klines = client.get_historical_klines(symbol, interval, start_time, end_time)

# Format k-lines into dataframe
ohlc = []
for line in klines:
    time = line[0] / 1000 # convert to timestamp
    open_price = float(line[1])
    high = float(line[2])
    low = float(line[3])
    close = float(line[4])
    volume = float(line[5])
    ohlc.append([time, open_price, high, low, close, volume])

df = pd.DataFrame(ohlc, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
df.set_index('Date', inplace=True)
print(df.columns)
df.index = pd.to_datetime(df['Date'])
# Define function to handle key press events
def on_key(event):
    if event.key == 'r':
        refresh_chart()

# Define function to handle scrolling events
def on_scroll(event):
    if event.button == 'up':
        mpf._offset -= 1
        refresh_chart()
    elif event.button == 'down':
        mpf._offset += 1
        refresh_chart()

# Define function to refresh chart
def refresh_chart():
    mpf.plot(df, type='candle', style='charles', volume=True)

# Register event handlers
fig, ax = mpf.plot(df, type='candle', style='charles', volume=True, returnfig=True)
fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('scroll_event', on_scroll)

# Show the chart
plt.show()
