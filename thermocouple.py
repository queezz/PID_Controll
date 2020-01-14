import math
import numpy as np
import tc

AMBIENT = 20.9

''' thermocouple at membrane '''
def maskTemp(voltages: np.ndarray):
    mask = np.where(voltages[:, 1] < 0.015)
    tmp = voltages[mask]
    #tmp[:, 1] = [calcTemp(i) for i in tmp[:, 1]]
    tmp[:,1] = np.array([tc.Thermocouple.mv_to_typek(i) for i in tmp[:,1]/1e-3]) + AMBIENT
    return tmp

def calcTemp(voltage: float):
    ambient = 20.9
    # V -> μV
    v = voltage * (1e6)

    t = 0.0
    for i in range(2, -3, -1):
        kx = 1
        jx = 10**i
        while(kx>0):
            t += jx
            if t>1372:
                break
            vta = calcElec(t)
            kx = v-vta
        t -= jx
    return t + ambient

#  calculate electromotive force
def calcElec(tm: float):
    i = 0
    j = 0
    a = [0]*10
    b = [0]*10
    c = [0]*2
    a = [
            3.9450128025E01,
            2.3622373598E-2,
            -3.2858906784E-4,
            -4.9904828777E-6,
            -6.7509059173E-8,
            -5.7410327428E-10,
            -3.1088872894E-12,
            -1.0451609365E-14,
            -1.9889266878E-17,
            -1.6322697486E-20,
        ]
    b = [
            3.8921204975E01,
            1.8558770032E-02,
            -9.9457592874E-05,
            3.1840945719E-07,
            -5.6072844889E-10,
            5.6075059059E-13,
            -3.2020720003E-16,
            9.7151147152E-20,
            -1.2104721275E-23,
            -1.7600413686E01,
        ]
    c = [-1.183432E-04, 1.185976E02]

    if tm < -270:
        pass
    elif tm < 0:
        for i in range(1, 11):
            j += a[i-1]*(tm**i)
    elif tm==0:
        j=0
    elif tm <= 1372:
        for i in range(1, 10):
            j += b[i-1]*(tm**i)
        j += b[9]+c[1]*math.exp(c[0]*pow(tm-126.9686,2))
    else:
        pass
    return j

def run():
    """ to run from command line, use following:
    python -c 'import thermocouple as tc; tc.run()'
    """
    print("input mv:")
    a = float(input())
    a /= (10**3)
    print(calcTemp(a))
    
if __name__ == "__main__":
    pass
