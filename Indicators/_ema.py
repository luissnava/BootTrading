import ccxt
from pprint import pprint
import pandas_ta as ta
import pandas as pd
from utils import ccxt_ohlcv_to_dataframe


# Based on Answer 2: https://cmsdk.com/python/calculate-exponential-moving-average-in-python.html
def exponential_moving_average(source, period):
    """ 
    Calculates the 'period' exponential moving average for 'source'
    Parameters
    --
    `source` is a list ordered from oldest to most recent 
    `period` is an integer denoting the period over which to calculate ema
    Returns 
    --
    a numeric array of the exponential moving average
    """
    ema = []
    source = list(source)
    # fill up the first 'period' - 1  entries entries with None
    for i in range(period - 1):
        ema.append(None)
    # get 'period' sma first and calculate the next 'period' ema
    sma = sum(source[:period]) / period
    multiplier = 2 / float(1 + period)
    ema.append(sma)
    # EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (source[period] - sma) * multiplier) + sma)
    # (source[period] * 2 - sma * 2 + 2 * sma / (1+period) )/(1 + period)
    # now calculate the rest of the values
    j = period
    for i in source[period+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        ema.append(tmp)
        j = j + 1
    return ema # pd.Series(data = ema, name = 'ema')


exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = ccxt_ohlcv_to_dataframe(ohlcv)

# pprint(df)

df['ema_ours'] = exponential_moving_average(df['close'], 10)
df['ema_target'] = df.ta.ema(length=10)

print(df.drop(columns=['time', 'open', 'high', 'low']))