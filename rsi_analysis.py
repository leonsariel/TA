import pandas as pd
from datetime import datetime

import talib as ta
import pandas as pd
import numpy as np

data = pd.read_csv('data/EURUSD.csv')
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

data["max"] = ta.MAX(close, timeperiod=10)
data["min"] = ta.MIN(close, timeperiod=10)

data['max_shift'] = data["max"].shift(-10)
data["min_shift"] = data["min"].shift(-10)

data["rsi"] = ta.RSI(close, timeperiod=14)
data["sma_10"] = ta.SMA(close, timeperiod=10)
rsi = data["rsi"]

previous_rsi = data["previous_rsi"] = data["rsi"].shift()
next_rsi = data["next_rsi"] = data["rsi"].shift(-1)

data["rsi_touch_point"] = np.where(
    ((previous_rsi >= 70) & (rsi < 70)) | ((previous_rsi <= 30) & (rsi > 30)), 1, 0)

data["rsi_sell"] = np.where(
    ((previous_rsi >= 70) & (data["rsi_touch_point"] == 1)), -1, 0)

data["rsi_buy"] = np.where(
    ((previous_rsi <= 30) & (data["rsi_touch_point"] == 1)), 1, 0)

total_sell = list(data["rsi_sell"]).count(-1)
total_buy = list(data["rsi_buy"]).count(1)
print("total sell signal: ", total_sell)
print("total buy signal: ", total_buy)

data["sma_shift"] = data["sma_10"].shift(-10)

a = data[(data.rsi_touch_point == 1) & (data.Close - data["min_shift"] > 0.0005) & (data.previous_rsi >= 70)]
b = data[(data.rsi_touch_point == 1) & (data["max_shift"] - data.Close > 0.0005) & (data.previous_rsi <= 30)]

a_count = len(a)
b_count = len(b)


print("rate is: ",(a_count+b_count)/(total_buy+total_sell))

a.to_csv("sell.csv")
data.to_csv("all.csv")
