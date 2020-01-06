import math
import numpy as np

''' permeation pressure gauge '''
def maskIonPres(voltages: np.ndarray):
    mask = np.where(voltages[:, 1] > 0.06)
    return voltages[mask]

def calcIonPres(voltage: float, scale: int):
    pres = voltage * (10**scale)
    return pres

if __name__ == "__main__":
    pass