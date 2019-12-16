import math
def calcTemperature(self, voltage):
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
                vta = calcT(t)
                kx = v-vta
            t -= jx
        return t

def calcT(self, tm):
        i = 0
        j = 0
        a = [0]*10
        b = [0]*10
        c = [0]*2
        a[0]= 3.9450128025E01
        a[1]= 2.3622373598E-2
        a[2]=-3.2858906784E-4
        a[3]=-4.9904828777E-6
        a[4]=-6.7509059173E-8
        a[5]=-5.7410327428E-10
        a[6]=-3.1088872894E-12
        a[7]=-1.0451609365E-14
        a[8]=-1.9889266878E-17
        a[9]=-1.6322697486E-20
        b[0]= 3.8921204975E01
        b[1]= 1.8558770032E-02
        b[2]=-9.9457592874E-05
        b[3]= 3.1840945719E-07
        b[4]=-5.6072844889E-10
        b[5]= 5.6075059059E-13
        b[6]=-3.2020720003E-16
        b[7]= 9.7151147152E-20
        b[8]=-1.2104721275E-23
        b[9]=-1.7600413686E01
        c[0]=-1.183432E-04
        c[1]= 1.185976E02

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

if __name__ == "__main__":
    pass