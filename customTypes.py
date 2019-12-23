from enum import Enum

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

    def getIndex(self):
        if self == self.PRASMA:
            return 0
        elif self == self.TEMPERATURE:
            return 1
        elif self == self.PRESSURE1:
            return 2
        elif self == self.PRESSURE2:
            return 3
        else:
            return

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