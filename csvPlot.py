import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from customTypes import ThreadType

def csvPlot(ttype: ThreadType, step: int):
    plt.figure()
    df = pd.read_csv("data/{}/out_{}.csv".format(ttype.value, step), header=0)
    plt.title("{}_{}".format(ttype.value, step))
    plt.xlabel("Time [s]")
    plt.ylabel(setYLabel(ttype))
    xy = ttype.getCalcArray(np.array(df))
    plt.plot(xy[:, 0], xy[:, 1])
    plt.savefig('data/images/{}/out_{}.png'.format(ttype.value, step))

def setYLabel(ttype: ThreadType):
    unit = ttype.getUnit()
    return "{} [{}]".format(ttype.value, unit)

if __name__ == "__main__":
    pass
