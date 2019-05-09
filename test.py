import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

freqs = np.arange(2, 20, 3)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
t = np.arange(0.0, 1.0, 0.001)
s = np.sin(2 * np.pi * freqs[0] * t)
l, = plt.plot(t, s, lw=2)


def yes(self, event):
    data[data.index = index, "result"] = 1
    plt.close()


def no(self, event):
    data[data.index = index, "result"] = -1
    plt.close()


axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Yes')
a = bnext.on_clicked(yes)
bprev = Button(axprev, 'No')
bprev.on_clicked(no)

plt.show()
