from utils import ccxt_ohlcv_to_dataframe
from _ema import exponential_moving_average
import ccxt
from pandas import DataFrame

def macd(source, period_fast = 12, period_slow = 26, period_signal = 9):
    fastma = exponential_moving_average(source = source, period = period_fast)
    slowma = exponential_moving_average(source = source, period = period_slow)
    macd = []
    first_index = 0
    for i in range(len(slowma)):
        if fastma[i] != None and slowma[i] != None:
            macd.append(fastma[i] - slowma[i])
        else:
            first_index = i + 1
            macd.append(None)
    signal = exponential_moving_average(
        source = macd[first_index:], 
        period = period_signal)
    l_m = len(macd)
    l_s = len(signal)
    for i in range(0, l_m - l_s):
        signal.insert(0, None)
    histogram = []
    for i in range(len(slowma)):
        if macd[i] != None and signal[i] != None:
            histogram.append(macd[i] - signal[i])
        else:
            histogram.append(None)
    return macd, histogram, signal


exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit = 1000)
df = ccxt_ohlcv_to_dataframe(ohlcv)

m, h, s = macd(source = df['close'])
my_macd = DataFrame({'macd':m, 'histogram':h, 'signal':s})
macd_ta = df.ta.macd()

print("Ours")
print(my_macd)

print("Target")
print(macd_ta)