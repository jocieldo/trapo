#! /usr/bin/env python
# -*- config: utf-8 -*-

"""
display traffic from logs
"""

import os
import sys
import glob
import numpy as np
import pandas as pd
from scipy import signal
import datetime



class EdgeDetector:
    """ analyze signal and get edges """
    TIME_OUT = 100 # 20ms * 150 = 1.1sec
    nothing = -1
    flat = 0
    rise = 1
    fall = 2
    beta = 9

    def __init__(self, initial_mean, initial_var, alpha=0.001):
        self.no_signal = True
        self.time_out = self.TIME_OUT
        self.var = initial_var
        self.mean = initial_mean
        self.alpha = alpha
        self.threshold = np.sqrt(self.var)*self.beta+self.mean
        self.threshold_log = []

    """
    car: 40km/h, 6m
     pass time from s1 to s2 is 1/(40000/3600) = 0.09sec
     pass time s2 is 6/(40000/3600) = 0.54sec
     total time is 0.63sec
    
    man: 4km/h, 0.5m
     pass time from s1 to s2 is 1/(4000/3600) = 0.9sec
     pass time s2 is 0.5/(4000/3600) = 0.45sec
     total time is 1.35sec
    
    consider the blank of 2.0 sec as nothing
    2.0 sec is 100 samples
    """


    """
    detect_edge
    return nothing, flat, rise or fall
              _________           __________  2 sec
    _________|         |_________|          |_______________
    nothing rise flat fall flat rise flat fall flat nothing
    """
    def put(self, signal):
        state = self.flat
        self.threshold_log.append(self.threshold)
        if signal < self.threshold:
            if self.no_signal == False:
                self.no_signal = True
                state = self.fall
            else:
                if self.time_out == 0:
                    state = self.nothing
                else:
                    self.time_out = self.time_out - 1

            """ advance variance and mean if not outlier """
            self.var = (1.0-self.alpha)*self.var+self.alpha*(1.0-self.alpha)*(signal-self.mean)**2
            self.mean = (1.0-self.alpha)*self.mean+self.alpha*signal
            self.threshold = np.sqrt(self.var)*self.beta+self.mean
        else:
            self.time_out = self.TIME_OUT
            if self.no_signal == True:
                self.no_signal = False
                state = self.rise

        return state


    def get_threshold(self):
        return self.threshold


    def get_threshold_log(self):
        return self.threshold_log





"""
extractObjects
usage:
    rise:1, fall:2, flat:0
    (sensor1, sensor2)

    man_car = [(1, 0), (2, 0), (0, 1), (0, 2), (0, 1), (1, 0), (0, 2), (2, 0)]
    man = [(1,0), (2,0), (0,1), (0,2)]
    cluster = man_car
    obj = extractObjects(cluster)
    for o in obj:
        print(o)

    exit(0)
"""
def extractObjects(timestamp, cluster):
    unknown = "unknown"

    left = "left"
    right = "right"
    direction = unknown

    car = "car"
    man = "man"
    obj = unknown

    BEGIN = {(0, 1):left, (1, 0):right}
    SIGNATURE1 = {(left, (0, 2)):man, (right, (2, 0)):man,
                 (left, (1, 0)):car, (right, (0,1)):car}
    SIGNATURE2 = {car:{left:((0, 2),(2, 0)), right:((2, 0),(0, 2))},
                  man:{left:((1, 0),(2, 0)), right:((0, 1),(0, 2))}}

    objects = []
    starttime = 0

    def confirmTerminal():
        for s in SIGNATURE2[obj][direction]:
            if s in cluster:
                i = cluster.index(s)
                tms = timestamp.pop(i)
                cluster.remove(s)
                delays.append(tms - starttime)
            else:
                return False
        return True

    while len(cluster) >= 4:
        t = timestamp.pop(0)
        c = cluster.pop(0)
        if c in BEGIN:
            direction = BEGIN[c]
            starttime = t
            delays = []
            delays.append(0)
        else:
            #print "don't extract object"
            break

        for (t, c) in zip(timestamp, cluster):
            if (direction, c) in SIGNATURE1:
                obj = SIGNATURE1[(direction, c)]
                cluster.remove(c)
                delays.append(t - starttime)
                timestamp.remove(t)
                break

        if not confirmTerminal():
            break

        objects.append([direction, obj, delays])

    return objects




def get_signature(serial, datetime, signal1, signal2):
    """
    sig1 is right sensor
    sig2 is left sensor
    
    car
             ____
     sig1 __|    |_____
               ____
     sig2 ____|    |_____
    
    raw code: (0,0), (0,0), (1,0), (0,0), (0,1), (0,0), (2,0), (0,2), (0,0)
    compress code :  (1,0), (0,1), (2,0), (0,2)

    man
             __ 
     sig1 __|  |_______
                  __
     sig2 _______|  |__

    raw code: (0,0), (1,0), (0,0), (2,0), (0,0), (0,1), (0,0), (0,2), (0,0)
    compress code :  (1,0), (2,0), (0,1), (0,2)

    # (sig1, sig2)
    # 0: flat or nothing
    # 1: rise
    # 2: fall
    """

    obj = []
    obj_serial = []
    detect = 0
    pre_s1 = 9999
    pre_s2 = 9999
    num = 1
    detect_time = datetime[0]
    signatures = []

    ed1 = EdgeDetector(np.median(signal1[0:100000]), np.var(signal1[0:100000]))
    ed2 = EdgeDetector(np.median(signal2), np.var(signal2))
    __progress = 0
    for (t, sig1, sig2, dt) in zip(serial, signal1, signal2, datetime):

        # display progress bar
        __progress += 1
        if __progress == 50*60*60:
            __progress = 0
            print('@', file=sys.stderr, end='', flush=True)

        s1 = ed1.put(sig1)
        s2 = ed2.put(sig2)

        if s1 == EdgeDetector.nothing and s2 == EdgeDetector.nothing:
            if detect != 0:
                signatures.append([t, detect_time, obj_serial[:], obj[:]])

                obj = []
                obj_serial = []
                pre_s1 = 9999
                pre_s2 = 9999
                detect = 0
            continue

        if s1 == EdgeDetector.rise and s2 == EdgeDetector.rise and detect == 0:
            pass
            #print("detect at the same time")

        if s1 == EdgeDetector.rise and detect == 0:
            detect = 1  # move object from right to left
            detect_time = dt

        if s2 == EdgeDetector.rise and detect == 0:
            detect = 2  # move object from left to right
            detect_time = dt

        if detect != 0:
            if s1 == EdgeDetector.nothing:
                s1 = EdgeDetector.flat
            if s2 == EdgeDetector.nothing:
                s2 = EdgeDetector.flat
            if pre_s1 == s1 and pre_s2 == s2:
                continue
            if s1 == EdgeDetector.flat and s2 == EdgeDetector.flat:
                continue

            obj_serial.append(t)
            obj.append((s1, s2))
            pre_s1 = s1
            pre_s2 = s2


    print('\n', file=sys.stderr, end='', flush=True)

    return signatures




def get_objects(signature):
    objects = []
    for (t, dt, serial, obj) in signature:
        res = extractObjects(serial, obj)
        if len(res) != 0:
            objects.append((dt, res))

    return objects




def get_csv_from_directory(directories):
    """ get csv files from directories """

    for dirname in directories:
        if not dirname:
            continue

        if not os.path.isdir(dirname):
            print("no directory:", dirname)
            continue

        if dirname[-1] != '/':
            dirname += '/'
        files = glob.glob(dirname+'*.CSV')

    return files




def read_files(files):
    datetime = []
    serial = []
    sensor1 = []
    sensor2 = []
    # marge files into a massive list
    for file in files:
        print('.', file=sys.stderr, end='', flush=True)
        df = pd.read_csv(file, names=["datetime", "serial", "sensor1", "sensor2"], skiprows=1)
        datetime.extend(list(df["datetime"]))
        serial.extend(list(df["serial"]))
        sensor1.extend(list(df["sensor1"]))
        sensor2.extend(list(df["sensor2"]))

    print('\n', file=sys.stderr, end='', flush=True)
    
    return serial, datetime, sensor1, sensor2




def output_csv(objects, filename=None):
    if filename:
        try:
            f = open(filename, 'w')
        except IOError:
            print("can't open %s\n" % filename, file=sys.stderr, end='', flush=True)
            exit(0)
    else:
        f = sys.stdout
        print('                 traffic                 ', file=f)
        print('-----------------------------------------', file=f)


    dir_char = {'left':'        >', 'right':'        <'}
    print('       date,     time, direction, object', file=f)
    for obj in objects:
        if isinstance(obj[0], datetime.datetime):
            date = obj[0].strftime('%Y-%m-%d')
            time = obj[0].strftime('%H:%M:%S')
        if isinstance(obj[0], str):
            date, time = obj[0].split('T')
        for o in obj[1]:
            print(' '+date, time, dir_char[o[0]], '   '+o[1], sep=', ', file=f)
    if not filename:
        print('-----------------------------------------', file=f)



def output_hourly(objects, filename=None):
    if filename:
        try:
            f = open(filename, 'w')
        except IOError:
            print("can't open %s\n" % filename, file=sys.stderr, end='', flush=True)
            exit(0)
    else:
        f = sys.stdout
        print()
        print('                     hourly traffic                       ', file=f)
        print('----------------------------------------------------------', file=f)

    count_hourly = {}
    for obj in objects:
        if isinstance(obj[0], datetime.datetime):
            current_time = obj[0].strftime('%Y-%m-%d,   %H')
        if isinstance(obj[0], str):
            date, time = obj[0].split('T')
            current_time = date + ',   ' + time.split(':')[0]
        if current_time not in count_hourly:
            count_hourly[current_time] = {'car':0, 'man':0, 'left':0, 'right':0}
        for o in obj[1]:
            count_hourly[current_time][o[1]] += 1
            count_hourly[current_time][o[0]] += 1

    print('       date, hour,      car,      man, to right,  to left', file=f)
    for hour in sorted(count_hourly.keys()):
        print(' ' + hour, end="", file=f)
        for obj in ('car', 'man', 'left', 'right'):
            print(',%9d' %  count_hourly[hour][obj], end="", file=f)
        print(file=f)
    if not filename:
        print('----------------------------------------------------------', file=f)




def main():
    if len(sys.argv) != 2:
        print('Usage: counter.py log_directory', file=sys.stderr)
        exit()

    if not os.path.isdir(sys.argv[1]):
        print('no directory:', sys.argv[1])
        exit()
    csvdir = sys.argv[1]
    if csvdir[-1]=='/':
        csvdir = csvdir[:-1]

    log_files = get_csv_from_directory([csvdir])
    (serial, dt, sensor1, sensor2) = read_files(log_files)
    med1 = signal.medfilt(sensor1, 17)
    med2 = signal.medfilt(sensor2, 17)
    signature = get_signature(serial, dt, med1, med2)
    detected_objects = sorted(get_objects(signature))
    output_csv(detected_objects, filename=csvdir+'-traffic.csv')
    output_hourly(detected_objects, filename=csvdir+'-hourly-traffic.csv')


if __name__ == '__main__':
    main()

