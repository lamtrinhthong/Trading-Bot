from src.api.mt5_service import Mt5Service
from src.api.binance_service import BinanceService
import pandas as pd

class DataLoader:

    @staticmethod
    def load_from_api(service_type, symbol, timeframe, number_of_candles=None, date_from=None, date_to=None):
        """
        Function to load data from an API service (Mt5Service or BinanceService).
        
        Parameters:
        - service_type: str, 'mt5' or 'binance' to indicate which service to use
        - symbol: str, symbol or pair to fetch data for (e.g., 'EURUSD', 'BTCUSDT')
        - timeframe: int, timeframe for data (e.g., 1 for M1, 1440 for D1)
        - number_of_candles: int, optional, number of recent candles to fetch
        - date_from: int, optional, start date/time in seconds since epoch
        - date_to: int, optional, end date/time in seconds since epoch
        
        Returns:
        - pd.DataFrame or None: DataFrame containing data from the API response, or None if request failed
        """
        if service_type == 'mt5':
            mt5_service = Mt5Service(server='your_mt5_server', login='your_mt5_login', password='your_mt5_password')
            mt5_service.connect()
            
            if number_of_candles:
                df = mt5_service.get_data(symbol, timeframe, number_of_candles)
            elif date_from and date_to:
                df = mt5_service.get_data_between_dates(symbol, timeframe, date_from, date_to)
            else:
                mt5_service.disconnect()
                return None
            
            mt5_service.disconnect()
            return df
    
        elif service_type == 'binance':
            return None
        
        else:
            print(f"Unsupported service type: {service_type}")
            return None
