from enum import Enum

class ThreadType(Enum):
    TEMPERATURE = "Temperature"
    PRESSURE1 = "Pressure1"
    PRESSURE2 = "Pressure2"

class ScaleSize(Enum):
    SMALL = -400
    MEDIUM = -1000
    FULL = 0

if __name__=="__main__":
    pass