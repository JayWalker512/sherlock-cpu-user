#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 20:08:31 2018

@author: jaywalker
"""
from __future__ import print_function
import sys
import csv
import io

def extractFields(tsvRow, fieldIndices=[]):
    extracted = []
    for i in fieldIndices:
        extracted.append(tsvRow[i])
        
    return extracted

def main(argv):
    #extractedRows = []
    with io.open(argv[1], encoding="ISO-8859-1") as tsvFile:
        tsvReader = csv.reader(tsvFile, delimiter='\t', quotechar='\"')
        
        with open('cpu_fields.tsv', 'wb') as tsvFile:
            tsvWriter = csv.writer(tsvFile, delimiter='\t', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        
            listOfUsers = []
            for row in tsvReader:
                #0: userid
                #1: timestamp
                #8: cpu total #order doesn't match the documentation. Shocking :/
                er = extractFields(row, [8,1,0])
                if ((str(er[0])).lower() != "null"):
                    userId = "-1"
                    try:
                        userId = listOfUsers.index(er[2])
                    except Exception:
                        listOfUsers.append(er[2])
                        userId = listOfUsers.index(er[2])
                        
                    er[2] = userId
                    #extractedRows.append(er)
                    #print(er)    
                    tsvWriter.writerow(er)
        
        
if __name__ == "__main__":
    main(sys.argv)