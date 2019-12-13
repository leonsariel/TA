from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib as ta
from backtesting.test import SMA, EURUSD

import pandas as pd

from datetime import datetime
from datetime import timedelta
import random
import datetime

df = pd.read_csv('data/USDJPY1h.csv')
df = df.set_index(pd.to_datetime(df['Date'].apply(str) + ' ' + df['Timestamp']))
df = df[:1000]

# df preprocessing
del df['Date']
del df['Timestamp']
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
open = df["Open"].values
high = df["High"].values
low = df["Low"].values
close = df["Close"].values


class SmaCross(Strategy):
    def init(self):
        Close = self.data.Close
        self.ma1 = self.I(SMA, Close, 10)
        self.ma2 = self.I(SMA, Close, 20)

        # example of using talib data
        self.sma = self.I(ta.SMA, self.data.Close, 20)
        self.atr = self.I(ta.ATR, self.data.High, self.data.Low, self.data.Close, 20)

        self.high20 = self.I(ta.MAX, self.data.High, 20)
        self.low20 = self.I(ta.MIN, self.data.Low, 20)

        self.sell_sl = self.data.Low + self.atr * 2
        self.buy_sl = self.data.High - self.atr * 2

    def next(self):
        pass
        # if crossover(self.ma1, self.ma2):
        #     self.buy()
        # elif crossover(self.ma2, self.ma1):
        #     self.sell()





bt = Backtest(df, SmaCross,
              cash=10000, commission=.002, margin=0.01)
bt.run()
bt.plot()
