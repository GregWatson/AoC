#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools

input_file_name = 'input.txt'
print_on = False


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getNewRow(prevRow):
    oldS = "." + prevRow + "."
    newS = ""
    while len(oldS) >= 3:
        #print(f"{(oldS[0:3])}")
        tmpS= oldS[0:3]
        if (tmpS=="^^." or tmpS==".^^" or tmpS=="^.." or tmpS=="..^") : newS = newS + "^"
        else: newS= newS +"."
        oldS = oldS[1:]
    return newS

def doPart1(db,loopCount):
    myDB = db[:]
    prevRow = db[0]
    for i in range(loopCount):
        # print(f"Prev row is {prevRow}")
        newRow = getNewRow(prevRow)
        myDB.append(newRow)
        prevRow = newRow
    safeCount = 0
    for l in myDB:
        for c in l:
            if (c == '.') : safeCount = safeCount+1
    return safeCount

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db, 39)
print(f"Part 1 is {p1}")

p2 = doPart1(db, 399999)
print(f"Part 2 is {p2}.")



