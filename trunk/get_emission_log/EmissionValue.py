# coding: utf-8

import time
#from PIL import Image
#import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys

from PyJEM import TEM3

def emission_log(count, sleeptime=1):
    """
    | A function that acquires the current emission value and writes it to the log file.
    | arg1: number of trials
    | arg2: Emission acquisition sleep time (s)
    | output: None
    """
    _gun_instance = TEM3.GUN3()
    file = open("log.txt", "w")
    x = []
    y = []
    for i in range(count):
        value = _gun_instance.GetEmissionCurrentValue()
        x.append(i)
        y.append(value)
        print("Emission: " + str(value))

        ##logfileへの書き込み
        date = datetime.datetime.today()
        write_data = date.strftime("%Y/%m/%d_%H:%M:%S ") + "EmissionValue: " + str(value) + "\n"
        file.write(write_data)
        time.sleep(interval_time)
    file.close()

    plt.plot(x, y, "-")
    plt.xlabel("Count")
    plt.ylabel("EmissionValue")
    plt.title("EmissionCurrentValue")
    plt.show()

def open_log(fileName):
    file = open(fileName, "r")
    for row in file:
        print(row)

    file.close()


if __name__ == '__main__':
    count = int(input("Number of trials: "))
    if count == None:
        print("Please set the number of trials.")
        count = 1
    interval_time = int(input(("Interval time: ")))
    if interval_time ==  None:
        interval_time = 1
        
    emission_log(count,time)
    
#    sys.exit()
