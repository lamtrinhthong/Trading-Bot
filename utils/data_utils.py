import MetaTrader5 as mt5
import pandas as pd

def get_data(symbol, timeframe, n):
    """Fetches the latest n bars of the given symbol and timeframe."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
