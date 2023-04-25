from pyjuque.Bot import defineBot
from BBStrategy import BBStrategy

import pandas as pd
import time

apikey = "bkfHQs0AcAY1QQjooCeqS1UrdOD70nAQJf5XJzlf9U3YBqjHU4vkYeoFMbpF75sL"
secret = "qHHbqzOi522ZeXWZfBEJwsJDQLJqibbZwTKOemDZx7kPsOI2BO2uQgyIurOrRhLL"
bot_config = {
	'name' : 'bot_spot',
	
	'exchange' : {
		'name' : 'binance',
		'params' : {
			'api_key': apikey,
			'secret': secret,
		},
	},

	'symbols' : ['ADA/USDT', 'XRP/USDT','TRX/USDT'],

	'starting_balance' : 10,

	'strategy': {
		'class': BBStrategy,
		'params': {
			'bb_len' : 20,
			'n_std' : 2.0,
			'rsi_len' : 14,
			'rsi_overbought': 60,
			'rsi_oversold' : 40,
		}
	},
	'timeframe' : '5m',

	'entry_settings' : {

		'initial_entry_allocation': 90,

		'signal_distance': 0.001
	},

	'exit_settings' : {

		'take_profit' : 2,

		'stop_loss_value': 1
	},

	'display_status' : True
}



def main():
	bot_controller = defineBot(bot_config)

	while True:
		try:
			bot_controller.executeBot()
		except KeyboardInterrupt as e:
			return e

		time.sleep(5)

if __name__ == '__main__':
	main()