import matplotlib.pyplot as plt
from .plot_candlestick import CandlestickPlotter

class WavePlotter:
    @staticmethod
    def plot_wave(wave):
        CandlestickPlotter.plot(wave.candlesticks)
