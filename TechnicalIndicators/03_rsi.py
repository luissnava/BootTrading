import ccxt
from pprint import pprint
import pandas_ta as ta
from utils import ccxt_ohlcv_to_dataframe

# Based on https://stackoverflow.com/a/62043926/4468246s
def relative_strength_index(source, period):
    """ Calculates the 'period' relative strength index for 'source'

        Parameters
        --
        `source` is a list ordered from oldest to most recent 
        `period` is an integer denoting the period over which to calculate ema

        Returns 
        --
        a numeric array of the relative strength index
    """
    source = list(source)
    rsi = [None]

    close_price0 = float(source[0])
    gain_avg0 = loss_avg0 = 0

    for price in source[1:]:
        close_price = float(price)
        if close_price > close_price0:
            gain = close_price - close_price0
            loss = 0
        else:
            gain = 0
            loss = close_price0 - close_price

        close_price0 = close_price
        gain_avg = (gain_avg0 * (period - 1) + gain) / period
        loss_avg = (loss_avg0 * (period - 1) + loss) / period
        if loss_avg == 0:
            rsi.append(100)
        else:
            rsi.append(100 - 100 / (1 + gain_avg / loss_avg))
        gain_avg0 = gain_avg
        loss_avg0 = loss_avg

    return rsi


exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = ccxt_ohlcv_to_dataframe(ohlcv)

# pprint(df)

df['rsi_ours'] = relative_strength_index(df['close'], 14)
df['rsi_target'] = df.ta.rsi(length=14)

print(df.drop(columns=['time', 'open', 'high', 'low']))
