import pandas as pd

class MovingAverage:

    def calculate_moving_average(self, df, period):
        df['ma'] = df['close'].rolling(window=period, min_periods=1).mean()

        return df
    
    def get_counter_trend(self, df, trend_H4):
        # Define counter trend logic
        if trend_H4 == 'uptrend':
            # Counter trend: price crosses below the short moving average
            df['counter_trend'] = df['close'] < df['ma']
        elif trend_H4 == 'downtrend':
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
