import pandas_ta as ta 
import pandas as pd 
from pyjuque.Strategies import StrategyTemplate
class BBStrategy(StrategyTemplate):
    def __init__(self, bb_len = 20, n_std = 2.0, rsi_len = 14, rsi_overbought = 60, rsi_oversold = 40, last_price = None, price_change_percentage_24h = None):
        self.bb_len = bb_len
        self.n_std = n_std
        self.rsi_len = rsi_len
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.last_price = last_price
        self.price_change_percentage_24h = price_change_percentage_24h
        self.long_entry_price = None
        self.long_stop_loss = None
        self.long_profit_target = None

    def setUp(self, df):
        bb = ta.bbands(
            close = df['close'],
            length = self.bb_len,
            std = self.n_std
            )

        df['lbb'] = bb.iloc[:,0]
        df['mbb'] = bb.iloc[:,1]
        df['ubb'] = bb.iloc[:,2]

        df['rsi'] = ta.rsi(close = df['close'], length = self.rsi_len)

        self.dataframe = df

    def checkLongSignal(self, i = None):
        df = self.dataframe

        if i == None:
            i = len(df)

        if (df['rsi'].iloc[i] < self.rsi_overbought) and \
            (df['rsi'].iloc[i] > self.rsi_oversold) and \
            (df['low'].iloc[i-1] < df['lbb'].iloc[i-1]) and \
            (df['low'].iloc[i] > df['lbb'].iloc[i]) and \
            (self.last_price is not None) and \
            (self.price_change_percentage_24h is not None) and \
            (self.last_price * 0.98 > df['close'].iloc[i]) and \
            (self.last_price * 0.96 < df['close'].iloc[i]) and \
            (self.price_change_percentage_24h > -5):
            return True

        return False
    
    def checkLongExit(self,i=None):
        df = self.dataframe

        if i == None:
            i = len(df) -1
        
        if self.position == "LONG":
            # Si el precio alcanza el stop loss, cerramos la posición.
            if df['low'].iloc[i] < self.long_entry_price * (1 - self.long_stop_loss):
                return "SL"
            # Si el precio alcanza el take profit, cerramos la posición.
            elif df['high'].iloc[i] > self.long_entry_price * (1 + self.long_profit_target):
                return "TP"
            # Si el precio no ha llegado ni al take profit ni al stop loss, mantenemos la posición abierta.
            else:
                return None

        return None

    
    def checkShortSignal(self, i = None):
        df = self.dataframe

        if i == None:
            i = len(df)

        if (df['rsi'].iloc[i] < self.rsi_overbought) and \
			(df['rsi'].iloc[i] > self.rsi_oversold) and \
			(df['high'].iloc[i-1] > df['ubb'].iloc[i-1]) and \
			(df['high'].iloc[i] < df['ubb'].iloc[i]):
            last_touch_index = (df['high'] > df['ubb']).values.nonzero()[0][-2]
            price_change = (df['close'].iloc[i] - df['close'].iloc[last_touch_index]) / df['close'].iloc[last_touch_index] 
            if price_change <= -0.005:
                return True
        return False

    def checkShortExit(self, i=None):
        df = self.dataframe

        if i is None:
            i = len(df) - 1

        if self.position == "SHORT":
            # Si el precio alcanza el stop loss, cerramos la posición.
            if df['high'].iloc[i] > self.short_entry_price * (1 + self.stop_loss):
                return "SL"
            # Si el precio alcanza el take profit, cerramos la posición.
            elif df['low'].iloc[i] < self.short_entry_price * (1 - self.take_profit):
                return "TP"
            # Si el precio no ha llegado ni al take profit ni al stop loss, mantenemos la posición abierta.
            else:
                return None

        return None
