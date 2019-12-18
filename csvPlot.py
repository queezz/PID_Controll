import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from customTypes import ThreadType

def csvPlot(ttype: ThreadType):
    if ttype == ThreadType.TEMPERATURE:
        df = pd.read_csv("data/Temperature/out_1.csv")
        plt.plot(df["Time"], df["Temperature"])
        plt.show()
    elif ttype == ThreadType.PRESSURE1:
        pass
    elif ttype == ThreadType.PRESSURE2:
        pass
    else:
        return

if __name__ == "__main__":
    csvPlot(ThreadType.TEMPERATURE)
