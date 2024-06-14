import json
import time
import MetaTrader5 as mt5
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
DF_ORDER_FLAG   = "order_flag"

TREND_DOWN  = "downtrend"
TREND_UP    = "uptrend"

TREND_D1    = TREND_DOWN
TREND_H4    = TREND_UP

def main():
    # Set up logging
    logging_utils.setup_logging()
    logger = logging_utils.get_logger(__name__)
    logger.info('Bot started')

    # Load configuration
    with open("C:/Thong/Python/trading_bot/config/config.json") as config_file:
        config = json.load(config_file)
    
    service = Mt5Service(config['server'], config['account'], config['password'])
    strategy = MovingAverage(TREND_H4)

    # Connect to the trading account
    service.connect()

    symbol = "XAUUSDm"
    number_of_candles = 100
    short_window = 10
    volume = 0.1
    time_frame = mt5.TIMEFRAME_H1

    while True:
        # Requesting historical data
        df = service.get_data(symbol, time_frame, number_of_candles)

        # Calculate Moving Average
        df = strategy.calculate_moving_average(df, short_window)

        # Define the counter trend
        counter_trend = strategy.get_counter_trend(df)

        # Check the current state is in counter trend or not
        is_in_counter_trend = strategy.is_current_counter_trend(df)

        if not is_in_counter_trend:
            print("Not in counter trend, keep waiting!")
            time.sleep(30)
            continue
            
        print("In counter trend, waiting for finishing the counter trend!")
        sl = strategy.get_sl(counter_trend)
        
        # Wait before the next iteration
        time.sleep(30)

if __name__ == "__main__":
    main()
