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
MAX=140

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getRulesUpdates(db):
    rulesForPage = {}
    updates=[]
    for l in db:
        m = re.match(r'(\d+)\|(\d+)',l)
        if m:
            p1=int(m.group(1))
            p2=int(m.group(2))
            if p1 in rulesForPage:
                rulesForPage[p1].append((p1,p2))
            else:  rulesForPage[p1] = [(p1,p2)]
            if p2 in rulesForPage:
                rulesForPage[p2].append((p1,p2))
            else:  rulesForPage[p2] = [(p1,p2)]
            continue
        m = re.match(r'\d+,\d.*',l)
        if m: 
            nums = list(map(int, l.split(",")))
            updates.append(nums)
    return rulesForPage, updates

def updateIsGood(u, rulesForPage):
    for ix,n in enumerate(u): 
        for rule in rulesForPage[n]:
            if rule[0]==n: # n is before other
                other = rule[1]
                if other in u:
                    if u.index(other) < ix: return 0
            else: # n after other
                other = rule[0]
                if other in u:
                    if u.index(other) > ix: return 0
    return int(u[len(u)>>1])

def fix(u, rulesForPage):
    for ix,n in enumerate(u): 
        for rule in rulesForPage[n]:
            if rule[0]==n: # n is before other
                other = rule[1]
                if other in u:
                    if u.index(other) > ix: continue
                else: continue
            else: # n after other
                other = rule[0]
                if other in u:
                    if u.index(other) < ix: continue
                else: continue
            newFix = u[:]
            # swap them
            #print(f"swap {n}<->{other} ", end='')
            newFix[ix] = other
            newFix[u.index(other)] = n
            return newFix
    return u



def  fixUpdate(u, rulesForPage):
    # print("")
    tryFix = u[:]
    while True:
        tryFix = fix(tryFix, rulesForPage)
        m = updateIsGood(tryFix, rulesForPage)
        if m: return m


def doPart1(db):
    s = 0
    rulesForPage, updates= getRulesUpdates(db)
    for u in updates:
        s = s + updateIsGood(u, rulesForPage)
    return s
   

def doPart2(db):
    s = 0
    rulesForPage, updates= getRulesUpdates(db)
    for u in updates:
        if updateIsGood(u, rulesForPage) == 0:
            #print(f"{u}")
            s = s + fixUpdate(u, rulesForPage)
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")



