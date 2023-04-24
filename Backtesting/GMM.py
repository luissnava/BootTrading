import ccxt
import pandas as pd 
import pandas_ta as ta 
from sklearn import mixture as mix 
import seaborn as sns
import matplotlib.pyplot as plt
from utils import ccxt_ohlcv_to_dataframe



exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '5m'
limit = 1000
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit)
df = ccxt_ohlcv_to_dataframe(ohlcv)


model = mix.GaussianMixture(
	n_components = 3,
	covariance_type = 'spherical',
	n_init = 50,
	random_state = 42,
	)
df['market_return'] = df['close']/df['close'].shift(1)
df['rsi'] = ta.rsi(close = df['close'], length = 14)
df['roc'] = ta.roc(close = df['close'], length = 14)
df.dropna(inplace = True)

features = df[['rsi', 'roc', 'market_return']]

model.fit(features)

df['regime'] = model.predict(features)

order = set(df['regime'])

fig = sns.FacetGrid(data = df, hue = 'regime', hue_order = order, aspect = 2, height = 3)
fig.map(plt.scatter, 'date', 'close', s =4).add_legend()

plt.title('Regimes')
plt.xlabel('Datetime')
plt.ylabel('close')
plt.show()