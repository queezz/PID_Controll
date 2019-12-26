import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from customTypes import ThreadType

def csvPlot(ttype: ThreadType, startTime: datetime.datetime):
    plt.figure()
    df = pd.read_csv("data/{}/out_{:%Y%m%d%H%M%S}.csv".format(ttype.value, startTime), header=0)
    plt.title("{}_{}".format(ttype.value, startTime))
    plt.xlabel("Time [s]")
    plt.ylabel(setYLabel(ttype))
    xy = ttype.getCalcArray(np.array(df))
    plt.plot(xy[:, 0], xy[:, 1])
    plt.savefig('data/images/{}/out_{:%Y%m%d%H%M%S}.png'.format(ttype.value, startTime))

def setYLabel(ttype: ThreadType):
    unit = ttype.getUnit()
    return "{} [{}]".format(ttype.value, unit)

if __name__ == "__main__":
    pass
