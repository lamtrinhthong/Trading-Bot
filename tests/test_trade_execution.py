import sys
import os

# Add the service directory to the Python path
service_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../service'))
sys.path.append(service_dir)

# Add the strategy directory to the Python path
service_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../strategies'))
sys.path.append(service_dir)

import json
import MetaTrader5 as mt5
from mt5_service import Mt5Service
from moving_average import MovingAverage

# Load configuration
with open("C:/Thong/Python/trading_bot/config/config.json", encoding='utf-8') as config_file:
    config = json.load(config_file)

symbol = config['symbol']
number_of_candles = 100
short_window = 10
volume = 0.01
time_frame = mt5.TIMEFRAME_M5
parent_trend = "downtrend"
order_type = mt5.ORDER_TYPE_BUY if parent_trend == "uptrend" else mt5.ORDER_TYPE_SELL
    
service = Mt5Service(config['server'], config['account'], config['password'])
strategy = MovingAverage(parent_trend)

# Connect to the trading account
service.connect()

sl = 65300.0
tp = 64800.0
service.place_order_market(symbol, order_type, volume, sl, tp)