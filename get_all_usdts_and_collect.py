import os
from binance.client import Client

# 请填入自己的 API key 和 secret
api_key = 'kZlXOJYbnndBNpaSZrZpSTsmUSGcGW7MeBYVVMESriPyzN6o78Q2zxdj6VI014WS'
api_secret = 'ILa8lI59QwWe8sGOx7FIdhCeV88XAShiuBegyijSjxsR9M5piShuuzR4YqJEQrPy'

client = Client(api_key, api_secret)


# 获取所有交易对信息
exchange_info = client.get_exchange_info()

# 保存交易对的类型信息
symbol_type_dict = {}

# 遍历所有交易对
for symbol in exchange_info['symbols']:
    # 判断是否为 USDT 交易对
    if symbol['quoteAsset'] == 'USDT':
        # 遍历交易对的筛选器
        for filter in symbol['filters']:
            # 判断是否为价格过滤器
            if filter['filterType'] == 'PRICE_FILTER':
                # 获取交易对的最小价格单位
                price_unit = float(filter['tickSize'])
                # 判断交易对的类型
                if price_unit < 0.001:
                    symbol_type = '小盘币'
                elif price_unit < 0.01:
                    symbol_type = '中盘币'
                else:
                    symbol_type = '大盘币'
                # 将交易对和类型保存到字典中
                symbol_type_dict[symbol['symbol']] = symbol_type

# 打印交易对和类型信息
for symbol, symbol_type in symbol_type_dict.items():
    print(f"{symbol}: {symbol_type}")
