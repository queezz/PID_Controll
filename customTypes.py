from enum import Enum

class ThreadType(Enum):
    TEMPERATURE = "Temperature"
    PRESSURE1 = "Pressure1"
    PRESSURE2 = "Pressure2"

    @classmethod
    def getEnum(cls, index: int):
        if index == 0:
            return cls.TEMPERATURE
        elif index == 1:
            return cls.PRESSURE1
        elif index == 2:
            return cls.PRESSURE2
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