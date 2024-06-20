import matplotlib.pyplot as plt
from .plot_wave import WavePlotter

class ElliottWavePlotter:
    @staticmethod
    def plot_elliott_wave(elliott_wave):
        WavePlotter.plot_wave(elliott_wave)
        plt.title(f'Elliott Wave ({elliott_wave.wave_type})')
        plt.show()
