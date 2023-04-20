import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait
from binance.client import Client
from binance.exceptions import BinanceAPIException
from mplfinance import make_marketcolors, make_mpf_style
import psutil
import os

def limit_memory(max_mem):
  """限制脚本最大内存使用量"""
  process = psutil.Process(os.getpid())
  available_mem = psutil.virtual_memory().available
  max_mem_bytes = int(max_mem * available_mem)
  if hasattr(process, 'rlimit'):
      # 在Linux/MacOS上使用rlimit方法
      # RLIMIT_DATA: 数据段的最大大小
      # RLIMIT_AS: 进程地址空间（堆栈、数据段、共享库等）的最大大小
      # RLIM_INFINITY: 表示无限制
      process.rlimit(psutil.RLIMIT_DATA, (max_mem_bytes, max_mem_bytes))
      process.rlimit(psutil.RLIMIT_AS, (max_mem_bytes, max_mem_bytes))
  else:
      # 在Windows上使用memory_info方法
      process.memory_info().rss

# 限制内存使用量为2GB
# limit_memory(2)


# 请填入自己的 API key 和 secret
api_key = 'kZlXOJYbnndBNpaSZrZpSTsmUSGcGW7MeBYVVMESriPyzN6o78Q2zxdj6VI014WS'
api_secret = 'ILa8lI59QwWe8sGOx7FIdhCeV88XAShiuBegyijSjxsR9M5piShuuzR4YqJEQrPy'

client = Client(api_key, api_secret)

# 获取所有交易对
tickers = client.get_all_tickers()

# 筛选出所有以 USDT 作为计价货币的交易对
usdt_pairs = [ticker for ticker in tickers if ticker['symbol'].endswith('USDT')]

# 创建一个锁对象
global_lock = threading.Lock()

# 第二个时间段的起止时间
start_time = '2020-10-01 00:00:00'
end_time = 'now'

class MyThread(threading.Thread):
  def __init__(self, name, paris):
    super().__init__()
    self.name = name
    self.pairs = paris
  
  def process_pair(self):
    flag = True
    klines = ""
    for pair in self.pairs:
      symbol = pair['symbol']
      print(f"Processing {symbol}...")
      each_pair_symbol = pair['symbol']
      # 获取指定交易对的历史交易数据
      pair = each_pair_symbol
      # 获取指定交易对的历史交易数据
      thread_id = threading.get_ident()
      #if flag:
      #  print(f"Thread {thread_id} processing pairs: {pairs}")
      #  flag = False
      #continue
      print(f"Thread {thread_id} processing pair: {pair}")
      #global_lock.acquire()
      try:
        klines = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, start_time, end_time)
      except BinanceAPIException as e:
        print(f"Exceptions found, {e}")
      finally:
        # 释放锁
        #global_lock.release()
        print(f"test")
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
      # 设置分辨率为4096×2160,figsize=(40.96, 21.6)
      fig, ax = mpf.plot(data, type='candle', mav=(7, 25, 99), style=style, 
              title=pair + ' Price History', ylabel='Price',
              volume=True, figratio=(21, 9), figsize=(19.2, 10.8), returnfig=True)

      # dpi 参数设置为 100，表示图像的每英寸点数为 100。
      # dpi = 100
      #dpi = 440
      dpi = 200
      fig.savefig('./output_1/' + pair + '_candle.png', dpi=dpi)

      # 保存 csv 格式文件
      #df.to_csv(f'{pair}.csv', index=False)

  def run(self):
    # 线程执行的操作
    self.process_pair()

# 计算每个线程需要处理的交易对数量
num_pairs_per_thread = len(usdt_pairs) // 8

# 创建 8 个线程
threads = []

# 创建线程池
# 这里的 args=(usdt_pairs[i::8],) 表示将 process_pair 函数的参数 pairs 
# 设置为 usdt_pairs[i::8]，其中 i 的取值为 0 到 7。
# usdt_pairs[i::8] 表示从列表 usdt_pairs 的第 i 个元素开始，每隔 8 个元素取一个元素，
# 得到的新列表就是每个线程处理的交易对列表。这样做是为了让不同的线程处理不同的交易对，
# 以达到并行处理的目的。比如当 i=0 时，usdt_pairs[i::8] 就表示从列表 usdt_pairs 的
# 第 0 个元素开始，每隔 8 个元素取一个元素，得到的就是第 0、第 8、第 16 个元素组成的
# 新列表；当 i=1 时，usdt_pairs[i::8] 就表示从列表 usdt_pairs 的第 1 个元素开始，
# 每隔 8 个元素取一个元素，得到的就是第 1、第 9、第 17 个元素组成的新列表，以此类推。
chunk_size = len(usdt_pairs) // 8
for i in range(1):
  start = i * chunk_size
  end = start + chunk_size
  if i == 7:
    # 如果是最后一个线程，则处理剩余的交易对
    end = len(usdt_pairs)
  thread_pairs = usdt_pairs[start:end]
  # 将交易对列表切片，并传入线程
  thread = MyThread(f"Thread-{i+1}", thread_pairs)
  threads.append(thread)

# 启动线程
for thread in threads:
  thread.start()

# 等待所有线程执行完毕
for t in threading.enumerate():
  if t != threading.current_thread():
      t.join()

print("All threads finished.")
