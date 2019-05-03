import pandas as pd
import backtrader as bt
import matplotlib as plt
from datetime import datetime
import backtrader as bt
import talib as ta
import pandas as pd
import numpy as np

data = pd.read_csv('EURUSD.csv')
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

data["rsi14"] = ta.RSI(close, timeperiod=14)
data["sma_10"] = ta.SMA(close, timeperiod=10)
rsi = data["rsi14"]
previous_rsi = rsi.shift()
next_rsi = rsi.shift(-1)

data["rsi_touch_point"] = np.where(
    ((previous_rsi >= 70) & (rsi <= 70)) | ((previous_rsi <= 30) & (rsi < 30)), 1, 0)

data["rsi_sell"] = np.where(
    ((previous_rsi >= 70) & (data["rsi_touch_point"]==1)), -1, 0)

data["rsi_buy"] = np.where(
    ((previous_rsi <= 30) & (data["rsi_touch_point"]==1)), 1, 0)



rsi_touch_point = data["rsi_touch_point"].values
a = data[rsi_touch_point == 0].sum()

print("total sell signal: ",list(data["rsi_sell"]).count(-1))
print("total buy signal: ",list(data["rsi_buy"]).count(1))
# print(list(data["rsi_touch_point"]).count(0))

#print(data["sma_10"])
a = data[(data.rsi_touch_point == 1) & (data.Close - data.sma_10>0.0003) & (data.rsi14.shift()>=70)]
b = data[(data.rsi_touch_point == 1) & (data.sma_10 - data.Close>0.0003) & (data.rsi14.shift()<=30)]
print(len(a))
print(len(b))

count = 0
for index, row in data.iterrows():
    # get data by row

    if (row['rsi_touch_point'] > 0) and (row['Close']>row['sma_10'] and (row['rsi_sell']==-1)):
        count += 1
# print("this is count",count)


