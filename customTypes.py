<<<<<<< HEAD
from enum import Enum
import numpy as np
from thermocouple import calcTemp, maskTemp
from ionizationGauge import maskIonPres
from pfeiffer import maskPfePres, calcPfePres

class ThreadType(Enum):
    PLASMA = "Plasma"
    TEMPERATURE = "Temperature"
    PRESSURE1 = "Pressure1"
    PRESSURE2 = "Pressure2"

    @classmethod
    def getEnum(cls, index: int):
        if index == 0:
            return cls.PLASMA
        elif index == 1:
            return cls.TEMPERATURE
        elif index == 2:
            return cls.PRESSURE1
        elif index == 3:
            return cls.PRESSURE2
        else:
            return

    def getGPIO(self):
        if self == self.PLASMA:
            return 0
        elif self == self.TEMPERATURE:
            return 17
        else:
            return

    def getUnit(self):
        if self == self.PLASMA:
            return "mA"
        elif self == self.TEMPERATURE:
            return "℃"
        elif self == self.PRESSURE1 or self == self.PRESSURE2:
            return "Torr"
        else:
            return ""

    def getCalcArray(self, data: np.ndarray):
        if self == self.PLASMA:
            # TODO: calc
            return data
        elif self == self.TEMPERATURE:
            return maskTemp(data)
        elif self == self.PRESSURE1:
            return maskIonPres(data)
        elif self == self.PRESSURE2:
            return maskPfePres(data)
        else:
            return data

    def getCalcValue(self, data: float):
        if self == self.PLASMA:
            # TODO: calc
            return data
        elif self == self.TEMPERATURE:
            return calcTemp(data)
        elif self == self.PRESSURE1:
            return data
        elif self == self.PRESSURE2:
            return calcPfePres(data)
        else:
            return data

class ScaleSize(Enum):
    SMALL = -400
    MEDIUM = -1000
    LARGE = -2500
    FULL = 0

    @classmethod
    def getEnum(cls, index: int):
        if index == 0:
            return cls.SMALL
        elif index == 1:
            return cls.MEDIUM
        elif index == 2:
            return cls.LARGE
        elif index == 3:
            return cls.FULL
        else:
            return

if __name__=="__main__":
    pass
=======
from enum import Enum
import numpy as np
from thermocouple import calcTemp, maskTemp
from ionizationGauge import maskIonPres
from pfeiffer import maskPfePres, calcPfePres

threadnames = ["Prasma", "Temperature","Pressure1","Pressure2"]

class ThreadType(Enum):
    PRASMA,TEMPERATURE,PRESSURE1,PRESSURE2 = threadnames 

    @classmethod
    def getEnum(cls, index: int):
        if index == 0:
            return cls.PRASMA
        elif index == 1:
            return cls.TEMPERATURE
        elif index == 2:
            return cls.PRESSURE1
        elif index == 3:
            return cls.PRESSURE2
        else:
            return

    def getGPIO(self):
        if self == self.PRASMA:
            return 0
        elif self == self.TEMPERATURE:
            return 17
        else:
            return

    def getUnit(self):
        if self == self.PRASMA:
            return "mA"
        elif self == self.TEMPERATURE:
            return "℃"
        elif self == self.PRESSURE1 or self == self.PRESSURE2:
            return "Torr"
        else:
            return ""

    def getCalcArray(self, data: np.ndarray):
        if self == self.PRASMA:
            # TODO: calc
            return data
        elif self == self.TEMPERATURE:
            return maskTemp(data)
        elif self == self.PRESSURE1:
            return maskIonPres(data)
        elif self == self.PRESSURE2:
            return maskPfePres(data)
        else:
            return data

    def getCalcValue(self, data: float):
        if self == self.PRASMA:
            # TODO: calc
            return data
        elif self == self.TEMPERATURE:
            return calcTemp(data)
        elif self == self.PRESSURE1:
            return data
        elif self == self.PRESSURE2:
            return calcPfePres(data)
        else:
            return data

class ScaleSize(Enum):
    SMALL = -400
    MEDIUM = -1000
    LARGE = -2500
    FULL = 0

    @classmethod
    def getEnum(cls, index: int):
        if index == 0:
            return cls.SMALL
        elif index == 1:
            return cls.MEDIUM
        elif index == 2:
            return cls.LARGE
        elif index == 3:
            return cls.FULL
        else:
            return

if __name__=="__main__":
    pass
>>>>>>> 3a4576ac061d1f190976018dac5adc0d1f46e468
