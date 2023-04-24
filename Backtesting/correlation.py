import ccxt
import pandas as pd
import numpy as np
import ccxt
from utils import ccxt_ohlcv_to_dataframe
import matplotlib.pyplot as plt
import seaborn as sns


exchange = ccxt.binance()
timeframe = '1d'
limit = 1000

symbol1 = 'BTC/USDT'
symbol2 = 'ETH/USDT'

btc = exchange.fetch_ohlcv(symbol1, timeframe, limit)
eth = exchange.fetch_ohlcv(symbol2, timeframe, limit)

btc = ccxt_ohlcv_to_dataframe(btc)
eth = ccxt_ohlcv_to_dataframe(eth)

y = btc['close']/btc['close'].shift(1)
x = eth['close']/eth['close'].shift(1)

y.dropna(inplace = True)
x.dropna(inplace = True)


# sns.displot(x = y, color='#F2AB6D', bins=50, kde=True)
# plt.title('BITCOIN')
# sns.displot(x = x, color='#F2AB6D', bins=50, kde=True)
# plt.title('ETHEREUM')
# plt.show()

constants = np.polyfit(x = x, y = y, deg = 1)

f = np.poly1d(constants)

yh = f(x)
yb = sum(y)/len(y)
sst = sum((y - yb)**2)
ssreg = sum((yh - yb) ** 2)
R2 = ssreg/sst


plt.plot(x.values, f(x), color = 'black', label = f)
sns.scatterplot(x  = x, y = y)
plt.text(min(x), min(y), 'R2: ' + str(round(R2, 2)))
plt.title('BTC / ETH | Market Returns Correlation')
plt.xlabel('ETH market return')
plt.ylabel('BTC market return')



plt.show()