import random
import matplotlib.pyplot as plt

my_list = [1] * 50 + [-1] * 50

# Profit-loss ratio
ratio = 2

base = 1000
risk = 0.02

win = 0
lost = 0
result_list = []
for i in range(0, 400):
    result = random.choice(my_list)
    profit_amount = base * (1 + risk * ratio)
    loss_amout = base - base * risk
    if result == 1:
        win += 1
        base = profit_amount
    else:
        lost += 1
        base = loss_amout
    result_list.append(base)

print("total wins equals: ", win)
print("final profit: ", base)


plt.plot(result_list)

plt.show()