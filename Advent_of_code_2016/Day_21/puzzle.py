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
LEN=8
NOP=0
ROTR=1
SWAP=2
RRLETTER=3
SWAPLETTER=4
REV=5
MOVE=6
UNDORRLETTER=7

LETROTMAP=(7,7,2,6,1,5,0,4)

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def parsedb(db):
    code=[]
    for l in db:
        m = re.match(r'rotate right (\d+) step',l)
        if m:
            rotnum=int(m.group(1))
            code.append((ROTR, rotnum))
            continue
        m = re.match(r'swap position (\d+) with position (\d+)',l)
        if m:
            s1=int(m.group(1))
            s2=int(m.group(2))
            code.append((SWAP, s1, s2))
            continue
        m = re.match(r'rotate based on position of letter (\w)',l)
        if m:
            code.append((RRLETTER, m.group(1)))
            continue
        m = re.match(r'rotate left (\d+) step',l)
        if m:
            rotnum=int(m.group(1))
            code.append((ROTR, LEN-rotnum))
            continue
        m = re.match(r'swap letter (\w) with letter (\w)',l)
        if m:
            code.append((SWAPLETTER, m.group(1), m.group(2)))
            continue
        m = re.match(r'reverse positions (\d) through (\d)',l)
        if m:
            s1=int(m.group(1))
            s2=int(m.group(2))
            code.append((REV, s1, s2))
            continue
        m = re.match(r'move position (\d) to position (\d)',l)
        if m:
            s1=int(m.group(1))
            s2=int(m.group(2))
            code.append((MOVE, s1, s2))
            continue
        print(f"Unknown instr {l}")
    return code

def rotRight(r,s):
    rr = r%LEN
    s1=s+s
    s1=s1[LEN-rr:2*LEN-rr]
    print(f"Rot {r} of {s} is {s1}")
    return s1
def swap(i1, i2,s):
    c=s[i2]
    s1=list(s)
    s1[i2]=s[i1]
    s1[i1]=c
    s1=''.join(s1)
    print(f"Swap pos {i1} with {i2} of {s} is {s1}")
    return s1
def rev(i1,i2,s):
    b4 = ''
    if i1>0: b4=s[0:i1]
    after=''
    if i2<LEN-1: after=s[i2+1:]
    mid=list(s[i1:i2+1])
    mid.reverse()
    print(f"b4 is {b4} reversed mid is {mid} after is {after}")
    newS=b4 + "".join(mid) + after
    print(f"Rev index {i1} thru {i2} of {s} is {newS}")
    return newS
def move(i1,i2,s):
    l = list(s)
    c=s[i1]
    del(l[i1])
    l.insert(i2,c)
    return "".join(l)

def doInstr(i,s):
    code=i[0]
    if code==ROTR: return rotRight(i[1],s)
    if code==SWAP: return swap(i[1],i[2], s)
    if code==RRLETTER: 
        pos=s.index(i[1])
        r=1+pos
        if pos >=4 : r=r+1
        print(f"RR based on pos of letter {i[1]} which is index {pos} so rot amount is {r}")
        return rotRight(r,s)
    if code==SWAPLETTER:
        i1=s.index(i[1])
        i2=s.index(i[2])
        if i1==i2: return s
        return swap(i1,i2,s)
    if code==REV: return rev(i[1],i[2],s)
    if code==MOVE: return move(i[1],i[2],s)
    if code==UNDORRLETTER:
        i1=s.index(i[1])
        rr=LETROTMAP[i1]
        return rotRight(rr,s)
    print(f"Unknown opcode {code}")
    sys.exit(1)

def revDB(db):
    db.reverse()
    code = []
    for i in db:
        if i[0]==ROTR: 
            code.append((ROTR, LEN-i[1]))
            continue
        if i[0]==SWAP:
            code.append((SWAP, i[2], i[1]))
            continue
        if i[0]==RRLETTER:
            code.append((UNDORRLETTER, i[1]))
            continue
        if i[0]==SWAPLETTER:
            code.append(i)
            continue
        if i[0]==REV:
            code.append(i)
            continue
        if i[0]==MOVE:
            code.append((MOVE, i[2], i[1]))
            continue
        print(f"Unknown opcode {i[0]}")
        sys.exit(1)
    return code

def doPart1(pwd,db):
    s=pwd
    for instr in db:
        s = doInstr(instr, s)
    return s


def doPart2(pwd, db):
    s=pwd
    rdb = revDB(db)
    for instr in rdb:
        s = doInstr(instr, s)
    return s
        



#---------------------------------------------------------------------------------------
# Load input
db = load_db()
db1 = parsedb(db)

#p1 = doPart1('abcdefgh',db1)
#print(f"Part 1 is {p1}")

p2 = doPart2('fbgdceah',db1)
print(f"Part 2 is {p2}.")



