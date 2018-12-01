#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:45:46 2018

@author: jaywalker
"""
from __future__ import print_function
import sys
import csv
import io
import sqlite3

def getDictListFromTSV(filename, columnNames):
    with io.open(filename, encoding="ISO-8859-1") as tsvFile:
        tsvReader = csv.DictReader(tsvFile, delimiter='\t', quotechar='\"', fieldnames=columnNames, restval='')
        tsvDictList = [dict(row) for row in tsvReader]
        return tsvDictList

def getHeaderListFromTSV(filename, delimiter):
    with io.open(filename, encoding="ISO-8859-1") as tsvFile:
        try:
            buff = []
            while True:
                line = tsvFile.read(1)
                buff.append(line)
                    
                if line == "":
                    break
                        
            bufferString = ''.join([str(x) for x in buff])
            return bufferString.split('\t')

        except (KeyboardInterrupt, Exception) as e:
            sys.stdout.flush()
            print(e)
            print(sys.exc_info())
            pass

def main(argv):
    tsvFilename = argv[1]
    tsvHeaderFilename = argv[2]
    print("Importing rows from file " + tsvFilename + " using headers in " + tsvHeaderFilename)
    
    headersList = getHeaderListFromTSV(tsvHeaderFilename, '\t')
    #print("Headers are: "+str(headersList))
    #tsvFile = getDictListFromTSV(tsvFilename, headersList) #this will OOM in no time
    
    #create the SQL database with the chosen fields present
    #...
    sqldb = sqlite3.connect('export.db') #maybe make this a parameter?
    sqlcursor = sqldb.cursor()
    fieldNamesString = ''.join([str(x) + ", " for x in headersList])
    fieldNamesString = fieldNamesString[:-2] #chop off the last comma and space so the list is correctly formatted
    createTableString = "CREATE TABLE sherlock (" + fieldNamesString + ");" 
    #yes I know using Python's string manipulation here is insecure
    #but we literally don't have a table yet so what does it matter?
    #the 'secure' method was not inserting the strings correctly :/
    sqlcursor.execute(createTableString)
    
    #build a string like (?,?,?) for parameter substitution of field names
    rowValuesInsertStringPartial = "("
    rowFieldsInsertStringPartial = "("
    for i in range(0,len(headersList)):
        rowValuesInsertStringPartial = rowValuesInsertStringPartial + "?,"
        rowFieldsInsertStringPartial = rowFieldsInsertStringPartial + headersList[i] + ","
        
    rowValuesInsertStringPartial = rowValuesInsertStringPartial[:-1] + ")" #chop off the last comma and space and append closing parenthesis
    rowFieldsInsertStringPartial = rowFieldsInsertStringPartial[:-1] + ")"
    fullRowInsertString = "INSERT INTO sherlock " + rowFieldsInsertStringPartial + " VALUES " + rowValuesInsertStringPartial
    #print(fullRowInsertString)    
    
    with io.open(tsvFilename, encoding="ISO-8859-1") as tsvFile:
        tsvReader = csv.reader(tsvFile, delimiter='\t', quotechar='\"')#, fieldnames=headersList)
        iteration=0
        for row in tsvReader:
            #here is where we insert into the SQL database by field name
            sqlcursor.execute(fullRowInsertString, row)
            if iteration % 100000 == 0:
                sqldb.commit()
            iteration += 1
            
    sqldb.commit()
    sqldb.close()

if __name__ == "__main__":
    main(sys.argv)