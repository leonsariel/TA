from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, EURUSD


import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt

from datetime import datetime
from datetime import timedelta
from matplotlib.widgets import Button
import random
import datetime

data = pd.read_csv('data/USDJPY1h.csv')
data = data.set_index(pd.to_datetime(data['Date'].apply(str) + ' ' + data['Timestamp']))
data = data[:10000]

# data preprocessing
del data['Date']
del data['Timestamp']
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
open = data["Open"].values
high = data["High"].values
low = data["Low"].values
close = data["Close"].values

print(data.tail())


class SmaCross(Strategy):
    def init(self):
        Close = self.data.Close
        self.ma1 = self.I(SMA, Close, 10)
        self.ma2 = self.I(SMA, Close, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


bt = Backtest(data, SmaCross,
              cash=10000, commission=.002)
bt.run()
bt.plot()
