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

# data["ema100"] = ta.EMA(close, timeperiod=100)

# Converting date to pandas datetime format
data['Date'] = pd.to_datetime(data.index)
data["Date"] = data["Date"].apply(mdates.date2num)
ohlc = data[['Date', 'Open', 'High', 'Low', 'Close']].copy()

data["ma"] = ta.EMA(close, timeperiod=100)
data["atr"] = ta.ATR(high, low, close, timeperiod=20)
data["atr_up"] = data["ma"] + ta.ATR(high, low, close, timeperiod=20)
data["atr_down"] = data["ma"] - ta.ATR(high, low, close, timeperiod=20)
data.dropna()

data["direction"] = np.where(((data["Low"] < data["ma"]) & (data["High"] < data["ma"])), -1,
                             np.where(((data["Low"] > data["ma"]) & (data["High"] > data["ma"])), 1, 0))

data["last_ma"] = data["ma"].shift(periods=1)

# cross over point and chanrao is 0, consecutive not including crossover points
data['consecutive'] = data.direction.groupby((data.direction != data.direction.shift()).cumsum()).transform(
    'size') * data.direction

data['previous_consecutive'] = data["consecutive"].shift(1)

data.direction.groupby((data.direction != data.direction.shift()))
data.to_csv("data.csv")


def yes(event):
    a = random.randint(1, 1000)
    currentDT = datetime.datetime.now()
    name = str(currentDT)
    name = name[-6:-1]
    plt.savefig("yes/{}.png".format(name + str(a)))
    global result
    result = 1
    plt.close()


def no(event):
    # data[index, "result"] = -1
    a = random.randint(1, 1000)
    currentDT = datetime.datetime.now()
    name = str(currentDT)
    name = name[-6:-1]
    plt.savefig("no/{}.png".format(name + str(a)))
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
        if row["consecutive"] == 0 and (row["previous_consecutive"]>=10 or row["previous_consecutive"]<=-10):
            previous_index = index + timedelta(minutes=-60 * 200)
            next_index = index + timedelta(minutes=60 * 200)
            temp_data = data[previous_index:next_index]
            count += 1

            ohlc = temp_data[['Date', 'Open', 'High', 'Low', 'Close']].copy()

            fig = plt.figure(figsize=(15, 7))

            # add cross line for censor
            ax = fig.add_subplot(111, facecolor='#FFFFCC')
            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            ax1 = fig.add_subplot(111)


            plt.axvline(x=index)

            candle = candlestick_ohlc(ax1, ohlc.values, width=.005, colorup='green', colordown='red')
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

            ax1.axvline(index, color='k', linestyle='-.')

            ema100 = ax1.plot(temp_data.index, temp_data["ma"])
            # sma30 = ax1.plot(temp_data.index, temp_data["sma30"])
            # sma50 = ax1.plot(temp_data.index, temp_data["sma50"])

            # horiz_line_temp_data_20 = np.array([30 for i in range(len(temp_data))])
            # ax2.plot(temp_data.index, horiz_line_temp_data_20)
            #
            # horiz_line_temp_data_80 = np.array([70 for i in range(len(temp_data))])
            # ax2.plot(temp_data.index, horiz_line_temp_data_80)

            # rsi14 = ax2.plot(temp_data.index, temp_data["rsi14"])
            # rsi20 = ax2.plot(temp_data.index, temp_data["rsi20"])
            # datacursor(rsi14)
            #
            # datacursor(rsi20)

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

# data.to_csv("result.csv")
