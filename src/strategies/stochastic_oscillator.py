class Stochastic:

    def calculate_stochastic(self, df, n, m):
        # Calculate %K
        df['Low_n'] = df['low'].rolling(window=n).min()
        df['High_n'] = df['high'].rolling(window=n).max()
        df['%K'] = 100 * (df['close'] - df['Low_n']) / (df['High_n'] - df['Low_n'])

        # Calculate %D
        df['%D'] = df['%K'].rolling(window=m).mean()

        return df