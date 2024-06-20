class Candlestick:

    def __init__(self, timestamp, open_price, high_price, low_price, close_price):
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.timestamp = timestamp

    def is_bullish(self):
        return self.close_price > self.open_price

    def is_bearish(self):
        return self.close_price < self.open_price
    
    def __repr__(self):
        return f"Candlestick(timestamp={self.timestamp}, open={self.open_price}, high={self.high_price}, low={self.low_price}, close={self.close_price})"

    def get_high(self):
        return self.high_price
    
    def get_low(self):
        return self.low_price
