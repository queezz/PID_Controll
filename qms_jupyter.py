# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
get_ipython().run_line_magic('pylab', 'inline')
import pandas as pd
import numpy as np
from datetime import datetime
import os


# %%
d=os.path.expanduser("~")
d=os.path.join(d,"Desktop", "Data")
d = os.path.join(d, "Qms")


# %%
a = os.listdir(d)
sorted(a)


# %%
""" csv """
<<<<<<< HEAD
base_time = datetime(2019, 12, 27, 20, 21, 38)
start_time = datetime(2019, 12, 27, 20, 17, 24)
d_time = (start_time - base_time).total_seconds()
q_csv = pd.read_csv(d + "/S1_191227_201724.csv", header=36, encoding='utf-8')
column_csv = pd.read_csv(d + "/S1_191227_201724.csv", header=None, encoding='utf-8', skiprows=lambda x: x not in [7])
print(q_csv.columns)
print(column_csv)
print(q_csv)

=======
base_time = datetime(2019, 12, 27, 20, 21, 38)  # pyqt start time
start_time = datetime(2019, 12, 27, 20, 17, 24) # qms start time
d_time = (start_time - base_time).total_seconds()
q_csv = pd.read_csv(d + "/S1_191227_201724.csv", header=36, encoding='utf-8')
print(q_csv.columns)
print(q_csv)


>>>>>>> 3a4576ac061d1f190976018dac5adc0d1f46e468
# %%
""" calculate time """
def calc_time(time: str):
    hour, minute, second = time.split(':')
    tmp = int(hour)*60*60 + int(minute)*60 + float(second)
    return tmp + d_time
calc_time('000:55:45.719')


# %%
data = np.array(q_csv)
data[:, 1] = [calc_time(i) for i in data[:, 1]]
<<<<<<< HEAD
print(data[-1, 1])

data_column  = np.array(column_csv)
data_column = np.array(column_csv)[0, 1:15]
print(data_column)

=======

""" plot qms """
>>>>>>> 3a4576ac061d1f190976018dac5adc0d1f46e468
def plot_qms(data: np.ndarray, gray_start: datetime=None, gray_end: datetime=None, red_start: datetime=None, red_end: datetime=None):
    import matplotlib.pyplot as plt
    # total pressure
    plt.title("total pressure")
    plt.xlabel("Time [s]")
<<<<<<< HEAD
    plt.ylabel("total pressure [A]")
=======
    plt.ylabel("total pressure [Pa]")
>>>>>>> 3a4576ac061d1f190976018dac5adc0d1f46e468
    plt.yscale('log')
    plt.axvspan(gray_start, gray_end, color="gray", alpha=0.3)
    plt.axvspan(red_start, red_end, color="red", alpha=0.3)
    plt.plot(data[:, 1], data[:, 4])
    plt.figure()

<<<<<<< HEAD
    plt.title("pressure")
    plt.xlabel("Time [s]")
    plt.ylabel("pressure [A]")
    plt.yscale('log')
    cmap = plt.get_cmap("tab20")

    for i in range(1, 15):
        plt.axvspan(gray_start, gray_end, color=cmap(15), alpha=0.3)
        plt.axvspan(red_start, red_end, color=cmap(17), alpha=0.3)
        plt.plot(data[:, 1], data[:, i+4], color=cmap(i), label="{}".format(data_column[i-1]))
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=18)

plot_qms(data)

=======
    for i in range(1, 15):
        plt.title("{} pressure".format(i))
        plt.xlabel("Time [s]")
        plt.ylabel("{} pressure [Pa]".format(i))
        plt.yscale('log')
        plt.axvspan(gray_start, gray_end, color="gray", alpha=0.3)
        plt.axvspan(red_start, red_end, color="red", alpha=0.3)
        plt.plot(data[:, 1], data[:, i+4])
        plt.figure()

plot_qms(data)
>>>>>>> 3a4576ac061d1f190976018dac5adc0d1f46e468
