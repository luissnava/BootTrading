import ccxt
from pprint import pprint
import pandas_ta as ta
import pandas as pd
from utils import ccxt_ohlcv_to_dataframe


def simple_moving_average(source, period):
    """ Calculates the 'period' simple moving average for 'source'

        Parameters
        --
        `source` is a list ordered from oldest to most recent 
        `period` is an integer denoting the period over which to calculate sma

        Returns 
        --
        a numeric array of the simple moving average
    """
    sma = []
    source = list(source)
        
    # fill up the first 'period' - 1  entries entries with None
    for i in range(period - 1):
        sma.append(None)

    # For each element from index 'period' onwards, calculate the 
    # average of the last 'period' elements and append it to the list
    for i in range(period, len(source) + 1):
        sma.append(sum(source[(i - period):i]) / period)
    
    return sma #pd.Series(sma, name = 'sma')


exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = ccxt_ohlcv_to_dataframe(ohlcv)

# pprint(df)

df['sma_ours'] = simple_moving_average(df['close'], 10)
df['sma_target'] = df.ta.sma(length=10)

print(df.drop(columns=['time', 'open', 'high', 'low']))