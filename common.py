#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 22:19:39 2018

@author: jaywalker
"""

import time
import math

#references:
#https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
#https://docs.python.org/2/library/time.html

#millis per hour: 3600000
#millis per day: 86400000

def timestampMillisToDayOfWeek(timestampMillis):
    return time.strftime("%w", time.strptime(time.ctime(math.floor(timestampMillis/1000.0))))
    
def timestampMillisToHourOfDay(timestampMillis):
    return time.strftime("%H", time.strptime(time.ctime(math.floor(timestampMillis/1000.0))))

def getWindowsByHour(startTimestamp, endTimestamp):
    listOfTimestamps = []
    tsInc = 3600000 #millis per hour
    for i in range(startTimestamp, endTimestamp, tsInc):
        listOfTimestamps.append([i, i+tsInc])
        
    return listOfTimestamps