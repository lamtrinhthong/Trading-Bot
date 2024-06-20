class Wave:
    def __init__(self, candlesticks):
        self.candlesticks = candlesticks

    def length(self):
        return len(self.candlesticks)

    def high(self):
        return max(candle.high_price for candle in self.candlesticks)

    def low(self):
        return min(candle.low_price for candle in self.candlesticks)
