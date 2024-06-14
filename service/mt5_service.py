import MetaTrader5 as mt5
import pandas as pd

class Mt5Service:
    def __init__(self, server, login, password):
        self.server = server
        self.login = login
        self.password = password
        self.connected = False

    def connect(self):
        mt5.initialize()
        if mt5.login(self.login, password=self.password, server=self.server):
            self.connected = True
            print(f"Connected to {self.server}")
        else:
            self.connected = False
            print(f"Failed to connect to {self.server}, error code: {mt5.last_error()}")

    def disconnect(self):
        mt5.shutdown()
        self.connected = False
        print("Disconnected from MT5")

    def get_account_info(self):
        if not self.connected:
            print("Not connected to MT5")
            return None
        
        account_info = mt5.account_info()
        if account_info is None:
            print(f"Failed to get account info, error code: {mt5.last_error()}")
            return None
        
        return account_info._asdict()

    def get_symbol_info(self, symbol):
        if not self.connected:
            print("Not connected to MT5")
            return None
        
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"Failed to get symbol info for {symbol}, error code: {mt5.last_error()}")
            return None
        
        return symbol_info._asdict()

    def place_order_market(self, symbol, order_type, volume, sl=None, tp=None):
        if not self.connected:
            print("Not connected to MT5")
            return None
        
        price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "comment": "python script order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order placement failed, error code: {mt5.last_error()}")
            return None
        
        return result

    def get_open_positions(self):
        if not self.connected:
            print("Not connected to MT5")
            return None
        
        positions = mt5.positions_get()
        if positions is None:
            print(f"Failed to get open positions, error code: {mt5.last_error()}")
            return None
        
        return [position._asdict() for position in positions]
    
    def get_data(self, symbol, timeframe, number_of_candles):
        # Requesting historical data
        bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, number_of_candles)
        df = pd.DataFrame(bars)[['time', 'open', 'high', 'low', 'close']]
        df['time'] = pd.to_datetime(df['time'], utc=True, unit='s').dt.tz_convert('Asia/Bangkok')

        return df
    
    def get_data_between_dates(self, symbol, timeframe, date_from, date_to):
        # Requesting historical data
        bars = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
        df = pd.DataFrame(bars)[['time', 'open', 'high', 'low', 'close']]
        df['time'] = pd.to_datetime(df['time'], unit='s')

        return df
    
    def close_position_by_ticket(self, ticket):
        if not self.connected:
            print("Not connected to MT5")
            return None
        
        position = mt5.positions_get(ticket=ticket)
        if not position:
            print(f"Position with ticket {ticket} not found, error code: {mt5.last_error()}")
            return None
        
        position = position[0]._asdict()
        symbol = position['symbol']
        volume = position['volume']
        order_type = mt5.ORDER_TYPE_SELL if position['type'] == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "position": ticket,
            "comment": "close position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to close position, error code: {mt5.last_error()}")
            return None
        return result
    
    def close_all_positions(self):
        if not self.connected:
            print("Not connected to MT5")
            return None
        
        positions = mt5.positions_get()
        print("Open Positions:")
        if positions is None:
            print(f"Failed to get open positions, error code: {mt5.last_error()}")
            return None
        
        for position in positions:
            position = position._asdict()

            symbol = position['symbol']
            volume = position['volume']
            order_type = mt5.ORDER_TYPE_SELL if position['type'] == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            ticket = position['ticket']

            request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "position": ticket,
            "comment": "close position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            }
        
            result = mt5.order_send(request)
            if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Failed to close position, error code: {mt5.last_error()}")

