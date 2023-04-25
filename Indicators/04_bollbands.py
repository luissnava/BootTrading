from utils import ccxt_ohlcv_to_dataframe
import pandas_ta as ta
import pandas as pd
import numpy as np
import ccxt

def standard_deviation_rolling(source, period = 20):
    std = []
    source = list(source)

    for i in range(period - 1):
        std.append(None)

    for i in range(period, len(source) + 1):
        std.append(np.std(source[(i-period):i], ddof = 1))

    return pd.Series(data = std, name = 'std')

def bollinger_bands(source, period = 20, n_deviations = 2):
    standard_deviation = standard_deviation_rolling(source = source, period = period)
    mid = ta.sma(source, period)

    deviations = n_deviations * standard_deviation

    bb_upper = mid + deviations
    bb_lower = mid - deviations

    return pd.DataFrame({'BBL': bb_lower, 'MID': mid, 'BBU':bb_upper})

exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = ccxt_ohlcv_to_dataframe(ohlcv)

my_bollinger_bands = bollinger_bands(source = df['close'], period = 20, n_deviations = 20)
ta_bollinger_bands = df.ta.bbands(length = 20, std = 20)

print("Ours")
print(my_bollinger_bands)

print("Target")
print(ta_bollinger_bands)