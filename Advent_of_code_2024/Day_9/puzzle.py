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
MAX=130

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def uncompress(a):
    unLen = 9*len(a)
    uncompressed = array.array('i',[0 for c in range(unLen)])
    index = 0
    ptr = 0
    useType = 0  # 0 = index 1 = -1
    spaceList = []
    dataList= []
    for n in a:
        if useType == 0: # data
            store = index
            dataList.append((ptr, n, index))
        else: # space
            store = -1
            spaceList.append((ptr, n))
        for rep in range(n):
            uncompressed[ptr] = store
            ptr = ptr+1
        useType = 1 - useType
        if useType == 0: index = index + 1
    # print(f"{uncompressed[0:100]}")
    return uncompressed, dataList, spaceList

def compress(unc):
    spacePtr = 0
    while unc[spacePtr] != -1: spacePtr = spacePtr+1
    dataPtr = len(unc)-1
    while unc[dataPtr] < 1: dataPtr = dataPtr-1
    print(f"space={spacePtr}   data={dataPtr}")
    while dataPtr > spacePtr:
        unc[spacePtr] = unc[dataPtr]
        unc[dataPtr] = 0
        while spacePtr < dataPtr and unc[spacePtr] != -1: spacePtr = spacePtr+1
        if spacePtr >= dataPtr: 
            print(f"After compression, last is at {spacePtr}"); return (unc, spacePtr)
        while dataPtr > spacePtr and unc[dataPtr] < 1: dataPtr = dataPtr - 1

def doPart1(db):
    s = 0
    a = array.array('i',[int(c) for c in db[0]])
    #for n in a:print(f"{n}")
    unc, dataList, spaceList = uncompress(a)
    (unc, length) = compress(unc)
    print(f"startL: {unc[0:50]}  endL:{unc[49850:49899]}")
    s = 0
    for i,n in enumerate(unc):
        if n>0: s = s + i*n
    return s
   

def doPart2(db):
    s = 0
    a = array.array('i',[int(c) for c in db[0]])
    #for n in a:print(f"{n}")
    unc, dataList, spaceList = uncompress(a)
    dataList.reverse()
    for (Dptr, Dlen, Dindex) in dataList:
        # print(f"({Dptr},{Dlen},{Dindex})    unc: {unc}")

        #find Leftmost space to hold it
        spIndex = 0
        while spIndex < len(spaceList):
            sp = spaceList[spIndex]
            if sp[1] >= Dlen and sp[0] < Dptr:
                Sptr= sp[0]; Slen=sp[1]
                # print(f"Move ({Dptr},{Dlen},{Dindex}) to Space index {spIndex}   ptr:{Sptr} len:{Slen}")
                #delete current data
                for i in range(Dlen):
                    unc[Dptr+i] = 0
                    unc[Sptr+i] = Dindex
                #Update space info
                if Dlen==Slen: # delete it
                    del(spaceList[spIndex])
                else:
                    Slen=Slen-Dlen # space remaining
                    Sptr = Sptr + Dlen
                    spaceList[spIndex]=(Sptr, Slen)
                spIndex=len(spaceList)
            else:
                spIndex = spIndex + 1

    s = 0
    for i,n in enumerate(unc):
        if n>0: s = s + i*n
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")



