import math
import numpy as np

''' pressure gauge in plasma chamber '''
def maskPfefPres(voltages: np.ndarray):
    # TODO: 閾値の設定
    return [i for i in voltages if i[1] > 0.5]

def calcPfefPres(voltage: float):
    # V → Torr
    exponent = 1.667 * voltage - 11.46
    pres = 10**exponent
    return pres

if __name__ == "__main__":
    a = float(input())
    print(calcPfefPres(a))