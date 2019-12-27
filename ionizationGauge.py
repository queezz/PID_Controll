import math
import numpy as np

''' permeation pressure gauge '''
def maskIonPres(voltages: np.ndarray):
    # TODO: 閾値の設定
    return [i for i in voltages if i[1] >= 0.005]

def calcIonPres(voltage: float, scale: int):
    pres = voltage * (10**scale)
    return pres

if __name__ == "__main__":
    pass