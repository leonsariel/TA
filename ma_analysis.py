import pandas as pd
from datetime import datetime
import talib as ta
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


def back_test(current_row, data, tp_atr_ratio, sl_atr_ratio):
    # close_max = data['Close'].max()
    # close_min = data['Close'].min()

    result = 0

    for index, row in data.iterrows():

        if current_row.position == 1:  # long position stop lost
            if row.Close <= current_row.sma - sl_atr_ratio * row.atr:
                if row.Close < current_row.Close:
                    result = -1
                    break

        if current_row.position == 1:  # long position take profit
            if row.Close >= row.sma + tp_atr_ratio * row.atr:
                if row.Close > (current_row.Close + 0.0005):
                    result = 1
                    break

        if current_row.position == -1:  # short position stop lost
            if row.Close >= current_row.sma + sl_atr_ratio * row.atr:
                if row.Close > current_row.Close:
                    result = -1
                    break

        if current_row.position == -1:  # short position take profit
            if row.Close <= row.sma - tp_atr_ratio * current_row.atr:
                if row.Close < (current_row.Close - 0.0005):
                    result = 1
                    break


        # if row==data[-1]:
        #     if current_row.position == -1:
        #         if row.Close <= row.sma - tp_atr_ratio * current_row.atr:
        #             if row.Close < (current_row.Close - 0.0003):
        #                 result = 1
        #                 break

    return result


########################
# 研究baseline， 以及确定stop loss， take profit 的最好参数
# baseline: sma, ema
# stoploss: 1 ATR - 1.5 ATR
# takeprofit: 1ATR - 1.5 ATR
########################


data = pd.read_csv('data/EURUSD.csv')
data = data.set_index(pd.to_datetime(data['Date'].apply(str) + ' ' + data['Timestamp']))

#########################
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
data["atr"] = ta.ATR(high, low, close, timeperiod=14)
sma = data["sma"] = ta.SMA(close, timeperiod=20)

data["atr_up"] = data["sma"] + 1 * data["atr"]
data["atr_down"] = data["sma"] - 1 * data["atr"]

pip = 0.0001
threshold = pip * 10
spread = 0.0003

########################

# yin = -1
# yang = 1
# not cross baseline, or range(open-close) less than threshold, = 0
# need to add threshold to delete dead market
data['position'] = np.where(
    ((data["High"] > data["sma"]) & (data["Low"] < data["sma"]) & (data["Open"] > data["Close"]) & (
            data["Open"] - data["Close"] > threshold)), -1,
    np.where(((data["High"] > data["sma"]) & (data["Low"] < data["sma"]) & (data["Open"] < data["Close"]) & (
            data["Close"] - data["Open"] > threshold)), 1, 0))

print(data['position'].value_counts())

# test if take profit or stop lose
count = 1
# 看后面多少根bar符合条件的var
index_range = 31

result = []

for index, row in data.iterrows():
    count += 1
    if count > 100 and count < (len(data) - 100):

        # long test
        if row["position"] == 1 or row["position"] == -1:
            # 设定范围在后面30根bar
            end_index = index + timedelta(minutes=15 * index_range)
            next_index = index + timedelta(minutes=15)
            temp_data = data[next_index:end_index]
            a = back_test(row, temp_data, 1.4, 1)
            result.append(a)

print("win: ", result.count(1))
print("loss: ", result.count(-1))
print("others: ", result.count(0))
print("winning ratio: ", result.count(1)/( result.count(1)+ result.count(-1)+ result.count(0)))
# data.to_csv("result.csv")


# total_rows = 124,562
#
