import pandas as pd
from datetime import datetime

import talib as ta
import pandas as pd
import numpy as np

data = pd.read_csv('data/USDJPY1h.csv')
data = data.set_index(pd.to_datetime(data['Time'].apply(str)))

# data preprocessing
del data['Time']

data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
open = data["Open"].values
high = data["High"].values
low = data["Low"].values
close = data["Close"].values
volume = data["Volume"].values

data["ma"] = ta.SMA(close, timeperiod=120)
data["atr"] = ta.ATR(high, low, close, timeperiod=20)
data["atr_up"] = data["ma"] + ta.ATR(high, low, close, timeperiod=20)
data["atr_down"] = data["ma"] - ta.ATR(high, low, close, timeperiod=20)
data.dropna()

data["direction"] = np.where(((data["Low"] < data["ma"]) & (data["High"] < data["ma"])), -1,
                             np.where(((data["Low"] > data["ma"]) & (data["High"] > data["ma"])), 1, 0))

data["last_ma"] = data["ma"].shift(periods=1)

data['consecutive'] = data.direction.groupby((data.direction != data.direction.shift()).cumsum()).transform(
    'size') * data.direction

data.direction.groupby((data.direction != data.direction.shift()))
data.to_csv("data.csv")
#
# count = 1
# start_price = 0
# end_price = 0
# pre_consecutive = 0
# start_list = []
# end_list = []
# consecutive_list = []
# position = False
# for index, row in data.iterrows():
#     if row.consecutive != pre_consecutive and pre_consecutive >= 10 and position==False:
#         if row.direction == 0:
#             start_price = round(row.last_ma, 6)
#             position = True
#     end_price = round(row.last_ma, 6)

    #     consecutive_list.append(int(row.consecutive))
    #     start_list.append(start_price)
    #     end_list.append(end_price)
    #
    #     pre_consecutive = row.consecutive
    # end_price = round(row.ma, 6)

# for index, row in data.iterrows():
#     if row.consecutive != pre_consecutive:
#         start_price = round(row.last_ma, 6)
#         # alist.append(start_close-end_close)
#         consecutive_list.append(int(row.consecutive))
#         start_list.append(start_price)
#         end_list.append(end_price)
#
#         pre_consecutive = row.consecutive
#     end_price = round(row.ma, 6)

# end_list = end_list[2:]
# start_list = start_list[1:-1]
# diff_list = []
#
# for (start, end, count) in zip(start_list, end_list, consecutive_list):
#     diff_list.append(round((end - start) * 10000,2))
#
# print(start_list[0:10])
# print(end_list[0:10])
# print(diff_list[0:10])


# consecutive_list = consecutive_list[1:-1]
#
# final_list = []
# result = []
#
# for (start, end, diff, count) in zip(start_list, end_list, diff_list, consecutive_list):
#
#     if ((count > 0 and diff > 0) or (count < 0 and diff < 0)):
#         result.append(1)
#         r = 1
#     else:
#         result.append(0)
#         r = 0
#     final_list.append([start, end, diff, count, r])
#
# pingping_list = []
# win = 0
# loss = 0
# for index, i in enumerate(final_list):
#     start, end, diff, count, result = i
#     if count >= 10 or count < -10:
#         pingping_list.append(final_list[index + 1])
#
#
# init_list = []
# init = 1000
# for i in pingping_list:
#     start, end, diff, count, result = i
#     if result == 1:
#
#
#         win = win + abs(diff)
#         init = init + win
#         init_list.append(init)
#     else:
#         loss = loss + abs(diff)
#         init = init - loss
#         init_list.append(init)
#
# my_df = pd.DataFrame(pingping_list)
# my_df.to_csv('analyst.csv', index=False, header=False)
# print(win,loss,win/loss)
#
# import matplotlib.pyplot as plt

# plt.plot(init_list)
# plt.ylabel('some numbers')
# plt.show()
