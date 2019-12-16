import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from threadType import ThreadType

def csvPlot(threadType: ThreadType):
    if threadType == ThreadType.TEMPERATURE:
        df = pd.read_csv("data/Temperature/out_1.csv")
        plt.plot(df["Time"], df["Temperature"])
        plt.show()
    elif threadType == ThreadType.PRESSURE1:
        pass
    elif threadType == ThreadType.PRESSURE2:
        pass
    else:
        return

if __name__ == "__main__":
    csvPlot(ThreadType.TEMPERATURE)
