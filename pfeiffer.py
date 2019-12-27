import math
import numpy as np

''' pressure gauge in plasma chamber '''
def maskPres2(voltages: np.ndarray):
    # TODO: 閾値の設定
    return [i for i in voltages if i[1] >= 0.005]

def calcPres2(voltage: float, scale: int):
    pres = voltage * (10**scale)
    return pres

if __name__ == "__main__":
    pass