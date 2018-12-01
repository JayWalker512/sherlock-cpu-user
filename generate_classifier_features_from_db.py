#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:57:38 2018

@author: jaywalker
"""
from __future__ import print_function
from common import *
import sqlite3
import csv
import sys

#Takes a value in range [0,max] and returns a one-hot encoded vector where the field corresponding to 'value' = 1
def oneHot(value, max):
    vec = []
    for i in range(0,max+1):
        if i == value:
            vec.append(1)
        else:
            vec.append(0)
    
    return vec;

def main(argv):
    sqldb = sqlite3.connect(argv[1]) #maybe make this a parameter?
    sqlcursor = sqldb.cursor()
    
    with open('cpu_classifier_features.tsv', 'wb') as tsvFile:
        tsvWriter = csv.writer(tsvFile, delimiter='\t', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        
        countOfUsersQuery = "select max(cast (user as int)) from sherlock"
        numUsersInDataset = int(sqlcursor.execute(countOfUsersQuery).fetchone()[0]) + 1 #include the zero'th user
        print("Number of users in dataset: " + str(numUsersInDataset))
        
        timestampRanges = getWindowsByHour(1459468800000, 1467331200000)
        print("Number of windows to iterate over: " + str(len(timestampRanges)))
        
        for window in timestampRanges:
            dayOfWeekOneHot = oneHot(int(timestampMillisToDayOfWeek(window[0])), 6)
            hourOfDayOneHot = oneHot(int(timestampMillisToHourOfDay(window[0])), 23)
            featuresWindow = [] #just the set of features we're calculating in this window
            for i in range(0, numUsersInDataset):
                featuresUser = []
                featuresUser.append(0) #cpu < 10
                featuresUser.append(0) #cpu >= 10 < 75
                featuresUser.append(0) # cpu > 75
                for n in dayOfWeekOneHot:
                    featuresUser.append(n)
                for n in hourOfDayOneHot:
                    featuresUser.append(n)
                    
                featuresUser.append(window[0])
                featuresUser.append(window[1])
                featuresUser.append(i) #user id
                featuresWindow.append(featuresUser)
            
            feature1Query = "select count(cpu_total),user from sherlock where timestamp >= \""+str(window[0])+"\" and timestamp <= \""+str(window[1])+"\" and cast(cpu_total as float) < 10.0 group by user"
            results = sqlcursor.execute(feature1Query).fetchall()
            #print(results)
            for k in results:
                featuresWindow[int(k[1])][0] = k[0]
            
            
            feature2Query = "select count(cpu_total),user from sherlock where timestamp >= \""+str(window[0])+"\" and timestamp <= \""+str(window[1])+"\" and cast(cpu_total as float) >= 10.0 and cast(cpu_total as float) < 75.0 group by user"
            results = sqlcursor.execute(feature2Query).fetchall()
            #print(results)
            for k in results:
                featuresWindow[int(k[1])][1] = k[0]
            
            feature3Query = "select count(cpu_total),user from sherlock where timestamp >= \""+str(window[0])+"\" and timestamp <= \""+str(window[1])+"\" and cast(cpu_total as float) > 75.0 group by user"
            results = sqlcursor.execute(feature3Query).fetchall()
            #print(results)
            for k in results:
                featuresWindow[int(k[1])][2] = k[0]
            
            for rowToWrite in featuresWindow:
                print(rowToWrite)
                tsvWriter.writerow(rowToWrite)
    
        
if __name__ == "__main__":
    main(sys.argv)