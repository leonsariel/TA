# _*_ coding: utf-8 _*_
__author__ = 'Di Meng'
__date__ = '8/4/2018 3:59 PM'

import pandas as pd
import numpy as np
import talib
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt


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

ATR14 = talib.ATR(high, low, close, timeperiod=14)
ATR20 = talib.ATR(high, low, close, timeperiod=20)
ATR30 = talib.ATR(high, low, close, timeperiod=30)

data = data.drop_duplicates(keep=False)

price = close

# count of reaching target1, target2,target3,and stop loss in next 30 bar, if target1 is reached first, stop loss won't count again
result = [0, 0, 0, 0]

# previous points
p_X, p_A, p_B, p_C, p_D = 0, 0, 0, 0, 0



for i in range(100, len(price)):
    # find max min
    max_point = list(argrelextrema(price[:i], np.greater, order=8)[0])
    min_point = list(argrelextrema(price[:i], np.less, order=8)[0])
    peak_index = max_point + min_point + [len(price[:i]) - 1]
    peak_index.sort()

    atr14 = ATR14[i]
    atr20 = ATR20[i]
    atr30 = ATR30[i]

    # list for last 5 points xabcd
    # current_index = peak_index[-6:]
    # current_pattern = price[current_index]
    # X, A, B, C, D, current = (i for i in current_pattern)

    current_index = peak_index[-5:]
    current_pattern = price[current_index]
    X, A, B, C, D = (i for i in current_pattern)

    peaks = price[peak_index]

    start = min(current_index)
    end = max(current_index)

    XA = current_pattern[1] - current_pattern[0]
    AB = current_pattern[2] - current_pattern[1]
    BC = current_pattern[3] - current_pattern[2]
    CD = current_pattern[4] - current_pattern[3]

    AD = abs(current_pattern[1] - current_pattern[4])

    target1 = AD * 0.382
    target2 = AD * 0.618
    target3 = A

    # in M shape, bullish
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if X == p_X and D != p_D:
            continue
        else:

            AB_range = np.array([0.618, 0.786]) * abs(XA)
            BC_range = np.array([0.618, 1]) * abs(AB)

            CD_range_XA = 0.768 * abs(XA)
            CD_range_AB = 1.27 * abs(AB)
            CD_range_equal_AB = abs(AB)

            target1 = D + target1
            target2 = D + target2
            target3 = A

            # stop loses is set 1 atr14 behind X point
            stop_loss = X - atr14

            CD_range = [min(CD_range_XA, CD_range_AB, CD_range_equal_AB),
                        max(CD_range_XA, CD_range_AB, CD_range_equal_AB)]

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                    CD_range[1]:
                if X == p_X and D != p_D:
                    continue
                plt.plot(np.arange(start - 30, i + 30), price[start - 30:i + 30])
                plt.scatter(current_index, current_pattern, c="b")

                plt.plot(current_index, current_pattern, c="r")

                # plot target line
                plt.axhline(y=price[i] + 0.0003, color='r', linestyle='-', label='hello')
                plt.axhline(y=target1, color='g', linestyle='-', label='hello')
                plt.axhline(y=target2, color='g', linestyle='-', label='hello')
                plt.axhline(y=target3, color='g', linestyle='-', label='hello')
                plt.axhline(y=stop_loss, color='c', linestyle='-', label='hello')

                print("this is i: ", price[i])


                plt.show()

                for k in range(1, 31):

                    compared_price = price[i + k]
                    if compared_price >= target1:
                        result[0] = 1 + result[0]
                        break
                    elif compared_price <= stop_loss:
                        result[-1] = result[-1] + 1
                        break
        p_X, p_A, p_B, p_C, p_D = X, A, B, C, D

    # in W shape, bearish
    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        if X == p_X and D != p_D:
            continue
        else:
            AB_range = np.array([0.618, 0.786]) * abs(XA)
            BC_range = np.array([0.618, 1]) * abs(AB)

            CD_range_XA = 0.768 * abs(XA)
            CD_range_AB = 1.27 * abs(AB)
            CD_range_equal_AB = abs(AB)

            target1 = D - target1
            target2 = D - target2
            target3 = A

            stop_loss = X + atr14

            CD_range = [min(CD_range_XA, CD_range_AB, CD_range_equal_AB),
                        max(CD_range_XA, CD_range_AB, CD_range_equal_AB)]

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and \
                    CD_range[0] < abs(CD) < CD_range[1]:
                plt.plot(np.arange(start - 30, i + 30), price[start - 30:i + 30])
                plt.scatter(current_index, current_pattern, c="b")
                plt.plot(current_index, current_pattern, c="r")

                plt.axhline(y=price[i] - 0.0003, color='r', linestyle='-', label='hello')
                plt.axhline(y=target1, color='g', linestyle='-', label='hello')
                plt.axhline(y=target2, color='g', linestyle='-', label='hello')
                plt.axhline(y=target3, color='g', linestyle='-', label='hello')
                plt.axhline(y=stop_loss, color='c', linestyle='-', label='hello')
                plt.show()

                for k in range(1, 31):

                    compared_price = price[i + k]
                    if compared_price <= target1:
                        result[0] = 1 + result[0]
                        break
                    elif compared_price >= stop_loss:
                        result[-1] = result[-1] + 1
                        break

        p_X, p_A, p_B, p_C, p_D = X, A, B, C, D

print(result)

