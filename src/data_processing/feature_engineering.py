import pandas as pd

class FeatureEngineering:
    @staticmethod
    def add_moving_average(df, window_size, column_name='close'):
        df[f'ma_{window_size}'] = df[column_name].rolling(window=window_size).mean()
        return df

    @staticmethod
    def add_relative_strength_index(df, window_size, column_name='close'):
        delta = df[column_name].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window_size).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window_size).mean()
        rs = gain / loss
        df[f'rsi_{window_size}'] = 100 - (100 / (1 + rs))
        return df

    @staticmethod
    def add_macd(df, short_window=12, long_window=26, signal_window=9, column_name='close'):
        short_ema = df[column_name].ewm(span=short_window, adjust=False).mean()
        long_ema = df[column_name].ewm(span=long_window, adjust=False).mean()
        df['macd'] = short_ema - long_ema
        df['macd_signal'] = df['macd'].ewm(span=signal_window, adjust=False).mean()
        return df
