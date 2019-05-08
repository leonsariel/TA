import talib as ta
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.widgets import Cursor
from mpldatacursor import datacursor


data = pd.read_csv('EURUSD.csv')
data = data.set_index(pd.to_datetime(data['Date'].apply(str) + ' ' + data['Timestamp']))
data = data[300:750]

# data preprocessing
del data['Date']
del data['Timestamp']
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
open = data["Open"].values
high = data["High"].values
low = data["Low"].values
close = data["Close"].values

data["rsi14"] = ta.RSI(close, timeperiod=14)
data["rsi20"] = ta.RSI(close, timeperiod=20)

# moving average
data["sma20"] = ta.SMA(close, timeperiod=20)
data["sma30"] = ta.SMA(close, timeperiod=30)
data["sma50"] = ta.SMA(close, timeperiod=50)

# Converting date to pandas datetime format
data['Date'] = pd.to_datetime(data.index)
data["Date"] = data["Date"].apply(mdates.date2num)
ohlc = data[['Date', 'Open', 'High', 'Low', 'Close']].copy()


fig = plt.figure()

# add cross line for censor
ax = fig.add_subplot(111, facecolor='#FFFFCC')
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)


candle = candlestick_ohlc(ax1, ohlc.values, width=.005, colorup='green', colordown='red')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
sma20 = ax1.plot(data.index,data["sma20"])
sma30 = ax1.plot(data.index,data["sma30"])
sma50 = ax1.plot(data.index,data["sma50"])



horiz_line_data_20 = np.array([30 for i in range(len(data))])
ax2.plot(data.index, horiz_line_data_20)

horiz_line_data_80 = np.array([70 for i in range(len(data))])
ax2.plot(data.index, horiz_line_data_80)

rsi14 = ax2.plot(data.index,data["rsi14"])
rsi20 = ax2.plot(data.index,data["rsi20"])
datacursor(rsi14)




ax3.plot(data.index, horiz_line_data_20)
ax3.plot(data.index, horiz_line_data_80)

rsi20 = ax3.plot(data.index,data["rsi20"])
datacursor(rsi20)





plt.show()