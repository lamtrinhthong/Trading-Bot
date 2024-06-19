import json
import time
import MetaTrader5 as mt5
import pandas as pd
from service.mt5_service import Mt5Service
from strategies.stochastic_oscillator import Stochastic
from strategies.moving_average import MovingAverage
from utils import logging_utils

# Define constants
DF_SYMBOL       = "time"
DF_OPEN         = "open"
DF_HIGH         = "high"
DF_LOW          = "low"
DF_CLOSE        = "close"
DF_MA           = "ma"
DF_STO_D        = "%D"
DF_STO_K        = "%K"

TREND_DOWN  = "downtrend"
TREND_UP    = "uptrend"

TREND_D1    = TREND_DOWN
TREND_H4    = TREND_UP
TREND_H1    = TREND_UP
TREND_M15   = TREND_UP
TREND_M5    = TREND_UP

TAKE_PROFIT = 2375

def display_positions(positions):
    if len(positions) < 1:
        print("There is no open position!")
        return

    # display these positions
    print("-----------------Open positions---------------------")
    print(positions)

def main():
    # Set up logging
    logging_utils.setup_logging()
    logger = logging_utils.get_logger(__name__)
    logger.info('Bot started')

    # Load configuration
    with open("C:/thong.lam/python/workspace/trading-bot/config/config.json") as config_file:
        config = json.load(config_file)

    symbol = "XAUUSDm"
    number_of_candles = 100
    short_window = 10
    volume = 0.1
    time_frame = mt5.TIMEFRAME_M5
    parent_trend = TREND_M15
    order_type = mt5.ORDER_TYPE_BUY if parent_trend == TREND_UP else mt5.ORDER_TYPE_SELL
    
    service = Mt5Service(config['server'], config['account'], config['password'])
    strategy = MovingAverage(parent_trend)

    # Connect to the trading account
    service.connect()
     
    latest_candle_time = service.get_latest_candle_time(symbol, time_frame)
    while True:
        
        # Detect new candle
        if latest_candle_time == service.get_latest_candle_time(symbol, time_frame):
            time.sleep(2)
            continue

        open_positions = service.get_open_positions()
        display_positions(open_positions)

        # Update new latest candle time
        latest_candle_time = service.get_latest_candle_time(symbol, time_frame)

        # Requesting historical data
        df = service.get_data(symbol, time_frame, number_of_candles)

        # Calculate Moving Average
        df = strategy.calculate_moving_average(df, short_window)

        # Define the counter trend
        counter_trend = strategy.get_counter_trend(df)

        # Place order
        if df["counter_trend"].iloc[-3] and df["counter_trend"].iloc[-2] != df["counter_trend"].iloc[-3]:
            sl = strategy.get_sl(counter_trend)
            tp = TAKE_PROFIT

            result = service.place_order_market(symbol, order_type, volume, sl, tp)
            print("The new order is placed")

            service.modify_sl_all_positions(sl)

if __name__ == "__main__":
    main()
