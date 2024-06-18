import pandas as pd

class MovingAverage:

    def __init__(self, parent_trend):
        self.parent_trend = parent_trend

    def calculate_moving_average(self, df, period):
        df['ma'] = df['close'].rolling(window=period, min_periods=1).mean()

        return df
    
    def get_counter_trend(self, df):
        # Define counter trend logic
        if self.parent_trend == 'uptrend':
            # Counter trend: price crosses below the short moving average
            df['counter_trend'] = df['close'] < df['ma']
        elif self.parent_trend == 'downtrend':
            # Counter trend: price crosses above the short moving average
            df['counter_trend'] = df['close'] > df['ma']
        else:
            df['counter_trend'] = False
        
        # Identify the groups of counter trend
        df['counter_trend_group'] = (df['counter_trend'] != df['counter_trend'].shift()).cumsum()

        # Filter the dataframe to get only counter trend rows
        counter_trend_df = df[df['counter_trend']]
        
        # Find the group with the most recent counter trend sequence
        if not counter_trend_df.empty:
            nearest_counter_trend_group = counter_trend_df['counter_trend_group'].iloc[-1]
            nearest_counter_trend_df = counter_trend_df[counter_trend_df['counter_trend_group'] == nearest_counter_trend_group]
        else:
            nearest_counter_trend_df = pd.DataFrame()  # Return empty DataFrame if no counter trend found

        return nearest_counter_trend_df
    
    def is_current_counter_trend(self, df):
        # Check if the current row is in a counter trend
        is_in_counter_trend = df['counter_trend'].iloc[-1]

        return is_in_counter_trend
    
    def get_sl(self, df_counter_trend):
        if self.parent_trend == 'uptrend':
            return df_counter_trend['low'].min() - 1 if not df_counter_trend.empty else None
        elif self.parent_trend == 'downtrend':
            return df_counter_trend['high'].max() + 1 if not df_counter_trend.empty else None