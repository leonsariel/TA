import talib as ta
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.widgets import Cursor
from mpldatacursor import datacursor
from datetime import datetime
from datetime import timedelta
from matplotlib.widgets import Button
import random


import datetime



data = pd.read_csv('data/EURUSD.csv')
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

rsi = data["rsi14"]
previous_rsi = rsi.shift()
next_rsi = rsi.shift(-1)
data["previous_rsi"] = rsi.shift()
data["next_rsi"] = rsi.shift(-1)

data["rsi_touch_point"] = np.where(
    ((previous_rsi > 70) & (rsi <= 70)) | ((previous_rsi < 30) & (rsi >= 30)), 1, 0)

data["rsi_sell"] = np.where(
    ((previous_rsi >= 70) & (data["rsi_touch_point"] == 1)), -1, 0)

data["rsi_buy"] = np.where(
    ((previous_rsi <= 30) & (data["rsi_touch_point"] == 1)), 1, 0)

# data.to_csv("hello.csv")

data['result'] = 0


def yes(event):
    a = random.randint(1,1000)
    currentDT = datetime.datetime.now()
    name = str(currentDT)
    name = name[-6:-1]
    plt.savefig("yes/{}.png".format(name+ str(a)))
    global result
    result = 1
    plt.close()


def no(event):
    # data[index, "result"] = -1
    a = random.randint(1,1000)
    currentDT = datetime.datetime.now()
    name = str(currentDT)
    name = name[-6:-1]
    plt.savefig("no/{}.png".format(name+ str(a)))
    global result
    result = -1
    plt.close()


def exit_chart(event):
    global result
    result = -100
    plt.close()


def onclick(event):
    return event.ydata


count = 1
for index, row in data.iterrows():
    if count > 100 and count < (len(data) - 100):
        if row["rsi_buy"] != 0 or row["rsi_sell"] != 0:
            previous_index = index + timedelta(minutes=-15 * 100)
            next_index = index + timedelta(minutes=15 * 100)
            temp_data = data[previous_index:next_index]
            count += 1

            ohlc = temp_data[['Date', 'Open', 'High', 'Low', 'Close']].copy()

            fig = plt.figure(figsize=(15, 7))

            # add cross line for censor
            ax = fig.add_subplot(111, facecolor='#FFFFCC')
            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)

            plt.axvline(x=index)

            candle = candlestick_ohlc(ax1, ohlc.values, width=.005, colorup='green', colordown='red')
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

            ax1.axvline(index, color='k', linestyle='-.')

            sma20 = ax1.plot(temp_data.index, temp_data["sma20"])
            sma30 = ax1.plot(temp_data.index, temp_data["sma30"])
            sma50 = ax1.plot(temp_data.index, temp_data["sma50"])

            horiz_line_temp_data_20 = np.array([30 for i in range(len(temp_data))])
            ax2.plot(temp_data.index, horiz_line_temp_data_20)

            horiz_line_temp_data_80 = np.array([70 for i in range(len(temp_data))])
            ax2.plot(temp_data.index, horiz_line_temp_data_80)

            rsi14 = ax2.plot(temp_data.index, temp_data["rsi14"])
            rsi20 = ax2.plot(temp_data.index, temp_data["rsi20"])
            datacursor(rsi14)

            datacursor(rsi20)

            ax_no = plt.axes([0.61, 0.05, 0.1, 0.075])
            b_no = Button(ax_no, 'No')
            b_no.on_clicked(no)

            ax_yes = plt.axes([0.5, 0.05, 0.1, 0.075])
            b_yes = Button(ax_yes, 'Yes')
            a = b_yes.on_clicked(yes)

            ax_exit = plt.axes([0.8, 0.05, 0.1, 0.075])
            b_exit = Button(ax_exit, 'Exit')
            b_exit.on_clicked(exit_chart)

            a = fig.canvas.mpl_connect('button_press_event', onclick)

            plt.show()

            if result != -100:
                a = row.index
                a = str(a)
                row.result = result
            else:
                break
    else:
        count += 1

data.to_csv("result.csv")
