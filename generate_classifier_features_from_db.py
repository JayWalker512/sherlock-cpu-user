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
        
        for userId in range(13,numUsersInDataset):
            for window in timestampRanges:
                feature1Query = "select count(cast (cpu_total as float)) from sherlock where timestamp >= \""+str(window[0])+"\" and timestamp <= \""+str(window[1])+"\" and cpu_total < 10.0 and user = " + str(userId)
                feature1 = sqlcursor.execute(feature1Query).fetchone()[0]
                feature2Query = "select count(cast (cpu_total as float)) from sherlock where timestamp >= \""+str(window[0])+"\" and timestamp <= \""+str(window[1])+"\" and cpu_total >= 10.0 and cpu_total < 75.0 and user = " + str(userId)
                feature2 = sqlcursor.execute(feature2Query).fetchone()[0]
                feature3Query = feature2Query = "select count(cast (cpu_total as float)) from sherlock where timestamp >= \""+str(window[0])+"\" and timestamp <= \""+str(window[1])+"\" and cpu_total >= 75.0 and user = " + str(userId)
                feature3 = sqlcursor.execute(feature3Query).fetchone()[0]
                dayOfWeekOneHot = oneHot(int(timestampMillisToDayOfWeek(window[0])), 6)
                hourOfDayOneHot = oneHot(int(timestampMillisToHourOfDay(window[0])), 23)
                
                rowToWrite = []
                rowToWrite.append(feature1)
                rowToWrite.append(feature2)
                rowToWrite.append(feature3)
                for n in dayOfWeekOneHot:
                    rowToWrite.append(n)
                for n in hourOfDayOneHot:
                    rowToWrite.append(n)
                    
                #last column is the userId
                rowToWrite.append(userId)
                print(rowToWrite)

                tsvWriter.writerow(rowToWrite)
        
        
if __name__ == "__main__":
    main(sys.argv)