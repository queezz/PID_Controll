from datetime import datetime
import logging
from logging import getLogger, StreamHandler, Formatter

def time_keeper():
    now = datetime.now()
    formatter = Formatter('%(asctime)s:%(levelname)s:%(message)s')
    logging.basicConfig(filename="data/log/{:%Y%m%d%H%M%S}.log".format(now), level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    logger =logging.getLogger("{:%Y%m%d%H%M%S}".format(now))

    help()
    while(True):
        an = input("input command: ")
        if an == "pon":
            t = datetime.now()
            logger.info("plasma start")
            print("plasma start time: {}".format(t))
        elif an == "poff":
            t = datetime.now()
            logger.info("plasma stop")
            print("plasma stop time: {}".format(t))
        elif an == "gin":
            t = datetime.now()
            logger.info("gas inflow start time")
            print("gas inflow start time: {}".format(t))
        elif an == "gout":
            t = datetime.now()
            logger.info("gas inflow stop time")
            print("gas inflow stop time: {}".format(t))
        elif an == "vgopen":
            t = datetime.now()
            logger.info("connect membrane chamber and plasma chamber")
            print("connect membrane chamber and plasma chamber: {}".format(t))
        elif an == "vgclose":
            t = datetime.now()
            logger.info("disconnect membrane chamber and plasma chamber")
            print("disconnect membrane chamber and plasma chamber: {}".format(t))
        elif an == "-h" or an == "--help" or an == "help":
            help()
        elif an == "exit":
            t = datetime.now()
            print("exit: {}".format(t))
            break
        else:
            continue
        print("")

def help():
    print("")
    print("-------time keeper--------")
    print("help:")
    print("     `pon`: plasma on time")
    print("     `poff`: plasma off time")
    print("     `gin`: gas inflow start time")
    print("     `gout`: gas inflow stop time")
    print("     `vgopen`: connect membrane chamber and plasma chamber")
    print("     `vgclose`: disconnect membrane chamber and plasma chamber")
    print("     `exit`: exit from this problem")
    print("     `help`: show help")
    print("")
    print("example: ")
    print("     `$ input command: pon`")
    print("     `$ plasma start time: 2019-12-27 17:05:37.226898`")
    print("----------------------------")
    print("")

if __name__ == "__main__":
    time_keeper()
