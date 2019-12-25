import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from customTypes import ThreadType

def csvPlot(ttype: ThreadType, step: int):
    plt.figure()
    df = pd.read_csv("data/{}/out_{}.csv".format(ttype.value, step))
    plt.title("{}_{}".format(ttype.value, step))
    plt.xlabel("Time [s]")
    plt.ylabel(setYLabel(ttype))
    plt.plot(df["Time"], df[ttype.value])
    plt.savefig('data/images/{}/out_{}.png'.format(ttype.value, step))

def setYLabel(ttype: ThreadType):
    unit = ttype.getUnit()
    return "{} [{}]".format(ttype.value, unit)

if __name__ == "__main__":
    pass
