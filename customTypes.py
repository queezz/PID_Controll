from enum import Enum
import numpy as np
from thermocouple import calcTemp

class ThreadType(Enum):
    PRASMA = "Prasma"
    TEMPERATURE = "Temperature"
    PRESSURE1 = "Pressure1"
    PRESSURE2 = "Pressure2"

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
            return data
        elif self == self.TEMPERATURE:
            return np.array([[i[0], calcTemp(i[1]), i[2]] for i in data])
        elif self == self.PRESSURE1:
            return data
        elif self == self.PRESSURE2:
            return data
        else:
            return data

    def getCalcValue(self, data: float):
        if self == self.PRASMA:
            return data
        elif self == self.TEMPERATURE:
            return calcTemp(data)
        elif self == self.PRESSURE1:
            return data
        elif self == self.PRESSURE2:
            return data
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