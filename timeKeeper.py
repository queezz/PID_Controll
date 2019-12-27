from datetime import datetime

def time_keeper():
    help()
    while(True):
        an = input("input command: ")
        if an == "pon":
            t = datetime.now()
            print("plasma start time: {}".format(t))
        elif an == "poff":
            t = datetime.now()
            print("plasma stop time: {}".format(t))
        elif an == "gin":
            t = datetime.now()
            print("gas inflow start time: {}".format(t))
        elif an == "gout":
            t = datetime.now()
            print("gas inflow stop time: {}".format(t))
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
    print("     `exit`: exit from this problem")
    print("     `help`: show help")
    print("")
    print("example: ")
    print("     `$ inpur command: pon`")
    print("     `$ plasma start time: 2019-12-27 17:05:37.226898`")
    print("----------------------------")
    print("")

time_keeper()
