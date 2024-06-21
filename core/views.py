import MetaTrader5 as mt5
from django.shortcuts import render
from src.api.mt5_service import Mt5Service

service = Mt5Service("Exness-MT5Trial7", 124880048, "Trinhthong0?")

def mt5_data_view(request):
    # Connect to the trading account
    service.connect()

    symbol = "XAUUSDm"
    number_of_candles = 100
    time_frame = mt5.TIMEFRAME_D1

    data = service.get_data(symbol, time_frame, number_of_candles)
    service.disconnect()

    # Convert DataFrame to a JSON structure for Plotly
    json_data = data.to_json(orient='records')

    return render(request, 'mt5_data.html', {'data': json_data})
