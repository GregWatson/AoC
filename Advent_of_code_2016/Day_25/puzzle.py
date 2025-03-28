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
NUMX=38
NUMY=24
MINSIZE=85
MAXSIZE=94

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    db = [ l.strip().split() for l in lines ]
    # for l in db: print(f"{l}")
    return db

def exec(db, reg):
    ip = 0
    outlast = None
    outCount = 0
    while ip < len(db):
        instr = db[ip]
        # print(f"ip={ip} {reg} {instr}")
        if instr[0] == 'cpy':
            if instr[1] in reg:
                reg[instr[2]] = reg[instr[1]]
            else:
                reg[instr[2]] = int(instr[1])
        elif instr[0] == 'inc':
            reg[instr[1]] += 1
        elif instr[0] == 'dec':
            reg[instr[1]] -= 1
        elif instr[0] == 'jnz':
            if instr[1] in reg:
                if reg[instr[1]] != 0:
                    ip += int(instr[2])
                    continue
            elif int(instr[1]) != 0:
                if instr[2] in reg:
                    ip += reg[instr[2]]
                else:
                    ip += int(instr[2])
                continue
        elif instr[0] == 'tgl':
            if instr[1] in reg:
                tgl = ip + reg[instr[1]]
            else:
                tgl = ip + int(instr[1])
            if tgl >= 0 and tgl < len(db):
                if db[tgl][0] == 'inc':
                    db[tgl][0] = 'dec'
                elif db[tgl][0] == 'dec':
                    db[tgl][0] = 'inc'
                elif db[tgl][0] == 'tgl':
                    db[tgl][0] = 'inc'
                elif db[tgl][0] == 'cpy':
                    db[tgl][0] = 'jnz'
                elif db[tgl][0] == 'jnz':
                    db[tgl][0] = 'cpy'
        elif instr[0] == 'out':
            if instr[1] in reg:
                out = reg[instr[1]]
            else:
                out = int(instr[1])
            print(f"{out}-",end='')
            if outlast is None:
                outlast = out
            elif outlast == out:
                return -1
            else:
                outlast = out
                outCount += 1
            if outCount > 10:
                break
        ip += 1
    return reg['a']

def doPart1(db):
    a = 1
    while exec(db, {'a':a, 'b':0, 'c':0, 'd':0}) == -1:
        a += 1
        print(f"\nTrying {a}")
    return a

def doPart2(db):
    c = exec(db, {'a':12, 'b':0, 'c':0, 'd':0})
    return c

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

#p2 = doPart2(db)
#print(f"Part 2 is {p2}.")


