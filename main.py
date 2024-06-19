"""
This module provides functionalities to display trading positions.

It includes functions to handle and display a list of trading positions,
formatting the output into a readable table format.

Functions:
    display_positions(positions): Displays the given positions in a table format.
    main(): The main entry point for the script.

Imports:
    json: Used for JSON handling (if applicable).
"""
import json
import time
import MetaTrader5 as mt5
# import pandas as pd
from service.mt5_service import Mt5Service
# from strategies.stochastic_oscillator import Stochastic
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
TREND_M15   = TREND_DOWN
TREND_M5    = TREND_UP

TAKE_PROFIT = 2375.0

def display_positions(positions):
    """
    Displays a list of trading positions in a formatted table.

    Args:
        positions (list): A list of position objects. Each position object is expected 
                          to have the attributes ticket, price_open, sl, tp, and profit.
                          
    Returns:
        None
    """
    if len(positions) < 1:
        print("There is no open position!")
        return

    # display these positions
    print("-----------------------Open positions-----------------------")
    # Define columns to print
    columns = ['Ticket', 'Price Open', 'Stop Loss', 'Take Profit', 'Profit']

    # Print header
    print("{:<10} {:<12} {:<12} {:<12} {:<10}".format(*columns))

    # Print each row
    for position in positions:
        print(f"{position.ticket:<10} {position.price_open:<12} {position.sl:<12} {position.tp:<12} {position.profit:<10}")

def main():
    """
    The main entry point for the script.

    This function initializes the program, handles any necessary setup, and 
    coordinates the execution of the program's main tasks. It typically 
    orchestrates the flow of the script, calling other functions and handling 
    the overall logic of the program.

    Args:
        None

    Returns:
        None
    """
    # Set up logging
    logging_utils.setup_logging()
    logger = logging_utils.get_logger(__name__)
    logger.info('Bot started')

    # Load configuration
    with open("C:/Thong/Python/trading_bot/config/config.json", encoding='utf-8') as config_file:
        config = json.load(config_file)

    symbol = config['symbol']
    number_of_candles = 100
    short_window = 10
    volume = 0.01
    time_frame = mt5.TIMEFRAME_M5
    parent_trend = TREND_M15
    order_type = mt5.ORDER_TYPE_BUY if parent_trend == TREND_UP else mt5.ORDER_TYPE_SELL
    service = Mt5Service(config['server'], config['account'], config['password'])
    strategy = MovingAverage(parent_trend)

    # Connect to the trading account
    service.connect()
     
    latest_candle_time = service.get_latest_candle_time(symbol, time_frame)
    while True:
        open_positions = service.get_open_positions()
        display_positions(open_positions)
        
        # Detect new candle
        if latest_candle_time == service.get_latest_candle_time(symbol, time_frame):
            time.sleep(2)
            continue

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
            sl = strategy.get_sl(counter_trend, 300)
            tp = 64800.0

            service.place_order_market(symbol, order_type, volume, sl, tp)
            print("The new order is placed")

            service.modify_sl_all_positions(sl)

if __name__ == "__main__":
    main()
