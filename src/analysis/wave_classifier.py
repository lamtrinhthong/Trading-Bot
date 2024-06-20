from sklearn.ensemble import RandomForestClassifier
import numpy as np

class WaveClassifier:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, features, labels):
        self.model.fit(features, labels)

    def predict(self, features):
        return self.model.predict(features)

    def predict_wave_type(self, wave):
        features = self.extract_features(wave)
        return self.predict(features)

    @staticmethod
    def extract_features(wave):
        # Example feature extraction
        return np.array([
            wave.length(),
            wave.high() - wave.low(),
            # Add more features as needed
        ])
