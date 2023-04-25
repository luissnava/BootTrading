import ccxt

print(ccxt.exchanges)

kucoin = ccxt.kucoin({
	'apiKey': 'YOUR_APIKEY',
	'secret': 'YOUR_SECRET',
	'timeout': 3000,
	'enableRateLimit':True,
	})

okex = ccxt.okex()
bitmex = ccxt.bitmex()
huobipro = ccxt.huobipro()


exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class()

symbol = 'BTC/USDT'
timeframe = '1h'

binance_ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
kucoin_ohlcv = kucoin.fetch_ohlcv(symbol, timeframe)
okex_ohlcv = okex.fetch_ohlcv(symbol, timeframe)
huobi_ohlcv = huobipro.fetch_ohlcv(symbol, timeframe)

print('\nBinance Data Format: ')
print(binance_ohlcv[0])
print('\nKucoin Data Format: ')
print(kucoin_ohlcv[0])
print('\nOkex Data Format: ')
print(okex_ohlcv[0])
print('\nHuobi Data Format: ')
print(huobi_ohlcv[0])

print('\nDefault Number of Candles: \n Binance {} Kucoin {} Okex {} Huobi {} \n'.format(
  len(binance_ohlcv), len(kucoin_ohlcv), len(okex_ohlcv), len(huobi_ohlcv)))
