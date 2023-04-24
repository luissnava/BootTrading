import ccxt
from utils import ccxt_ohlcv_to_dataframe

from sklearn.cluster import KMeans

import plotly.graph_objects as go 
from plotly.subplots import make_subplots

exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '5m'
limit = 1000
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit)
df = ccxt_ohlcv_to_dataframe(ohlcv)

def get_features(df):

	df["H/O"] = df["high"]/df["open"]
	df["L/O"] = df["low"]/df["open"]
	df["C/O"] = df["close"]/df["open"]

	return df[["H/O", "L/O", "C/O"]]

features = get_features(df)

k = 6

model = KMeans(n_clusters = k, random_state = 42)
model.fit(features)

df['cluster'] = model.labels_

# model.predict(new_features)

df.sort_values(by = 'cluster', inplace = True)
df.reset_index(inplace = True)
df['clust_index'] = df.index

df["clust_change"] = df["cluster"].diff()
change_indices = df[df["clust_change"] != 0]


fig = make_subplots(
	rows = 1, cols = 1,
	)

fig.add_trace(
	go.Candlestick(
		x = df['clust_index'],
		open = df['open'],
		close = df['close'],
		high = df['high'],
		low = df['low'],
		)
	)

for row in change_indices.iterrows():
	fig.add_shape(
		type = 'line',
		yref = 'y',
		xref = 'x',
		x0 = row[1]['clust_index'],
		y0 = df['low'].min(),
		x1 = row[1]['clust_index'],
		y1 = df['high'].max(),
		line = dict(color = 'black', width = 3)
	)


fig.update_layout(xaxis_rangeslider_visible = False, showlegend = False)
fig.show()