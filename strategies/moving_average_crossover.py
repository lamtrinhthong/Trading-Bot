import pandas as pd
import numpy as np

def moving_average_crossover(df, short_window=50, long_window=200):
    """Generates trading signals based on moving average crossover strategy."""
    signals = pd.DataFrame(index=df.index)
    signals['price'] = df['close']
    signals['short_mavg'] = df['close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = df['close'].rolling(window=long_window, min_periods=1).mean()
    signals['signal'] = 0
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1, 0)
    signals['positions'] = signals['signal'].diff()
    return signals
