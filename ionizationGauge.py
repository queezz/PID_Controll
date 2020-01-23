import numpy as np

''' permeation pressure gauge '''
def maskIonPres(voltages: np.ndarray,**kws):
    m = kws.get('IGrange',1e-3)
    mask = np.where(voltages[:, 1] > 0.01)
    voltages[:, 1] = voltages[:,1]*m
    tmp = voltages[mask]
    return tmp

def calcIGPres(voltage,**kws):
    """ convert 0-10 V output into Torr """
    return 

if __name__ == "__main__":
    pass
