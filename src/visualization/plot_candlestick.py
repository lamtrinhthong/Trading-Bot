import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class CandlestickPlotter:
    @staticmethod
    def plot(candlesticks):
        dates = [candle.timestamp for candle in candlesticks]
        open_prices = [candle.open_price for candle in candlesticks]
        high_prices = [candle.high_price for candle in candlesticks]
        low_prices = [candle.low_price for candle in candlesticks]
        close_prices = [candle.close_price for candle in candlesticks]

        fig, ax = plt.subplots()
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        for i in range(len(candlesticks)):
            color = 'green' if close_prices[i] > open_prices[i] else 'red'
            ax.plot([dates[i], dates[i]], [low_prices[i], high_prices[i]], color=color)
            ax.plot([dates[i], dates[i]], [open_prices[i], close_prices[i]], color=color, linewidth=5)

        plt.show()
