import sys
sys.path.append('..')
import RPi.GPIO as GPIO
import time
import AIO

def chika():
    GPIO.output(17, True)

def nonchika():
    GPIO.output(17, False)

def main():
    try:
        aio = AIO.AIO_32_0RA_IRC(0x49, 0x3e)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        while(True):
            voltage = aio.analog_read_volt(0, aio.DataRate.DR_860SPS)
            print('CH{:d}: {:2.3f}V'.format(1, voltage))
            if voltage>0.7:
                chika()
            else:
                nonchika()
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
