import MetaTrader5 as mt5
import json
from strategies.moving_average_crossover import moving_average_crossover
from utils.data_utils import get_data
from utils.trade_utils import execute_trade

def main():
    # Load configuration
    with open("config/config.json") as config_file:
        config = json.load(config_file)
    
    # Initialize the MetaTrader 5 connection
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    # Login to your account
    authorized = mt5.login(config['account'], config['password'], config['server'])
    if not authorized:
        print("Failed to connect at account #{}, error code: {}".format(config['account'], mt5.last_error()))
        quit()
    
    # Fetch data
    df = get_data(config['symbol'], getattr(mt5, f'TIMEFRAME_{config["timeframe"]}'), 500)
    
    # Generate trading signals
    signals = moving_average_crossover(df, config['short_window'], config['long_window'])
    
    # Execute trade
    if signals['positions'].iloc[-1] == 1:
        result = execute_trade(config['symbol'], "buy", config['lot_size'])
        print("Buy order executed:", result)
    elif signals['positions'].iloc[-1] == -1:
        result = execute_trade(config['symbol'], "sell", config['lot_size'])
        print("Sell order executed:", result)
    
    # Close the connection
    mt5.shutdown()

if __name__ == "__main__":
    main()
