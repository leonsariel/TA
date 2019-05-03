from datetime import datetime
import backtrader as bt


import pandas as pd



data = pd.read_csv('short.csv')
data = data.set_index(pd.to_datetime(data['Date'].apply(str) + ' ' + data['Timestamp']))

# data preprocessing
del data['Date']
del data['Timestamp']
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

open = data["Open"].values
high = data["High"].values
low = data["Low"].values
close = data["Close"].values
volume = data["Volume"].values
data["openinterest"] = 0

print(data.head())


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

data0 = bt.feeds.PandasData(dataname=data)

# data0 = bt.feeds.GenericCSVData(
#     dataname='EURUSD.csv',
#
#     # fromdate=datetime.datetime(2012, 1, 1),
#     # todate=datetime.datetime(2012, 12, 31),
#
#     nullvalue=0.0,
#
#     dtformat=('%Y%m%d'),
#
#     datetime=0,
#     high=2,
#     low=3,
#     open=4,
#     close=5,
#     volume=6,
#     openinterest=-1
# )




cerebro.adddata(data0)

cerebro.run()
cerebro.plot()