#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string

input_file_name = 'input.txt'
print_on = False

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def has_abba(s):
    m = re.match(r'.*(\w)(\w)\2\1.*',s)
    if m and (m.group(1) != m.group(2)): return True
    return False

def get_supers(l):
    supers = []
    in_super = True
    s = ''
    for c in l:
        if in_super:
            if c == '[':
                supers.append(s)
                s = ''
                in_super = False
            else:
                s += c
        else:
            if c == ']':
                in_super = True
    if len(s):
        supers.append(s)
    return supers

def get_abas(l):
    abas = []
    for s in l:
        if len(s) < 3: continue
        for i,c in enumerate(s):
            if i <= (len(s)-3):
                if (s[i+2] == c) and (s[i+1] != c):
                    print(f"{s} {i} ")
                    abas.append(s[i:i+3])
    return abas
            
def do_part1(db):
    c = 0
    for l in db:
        m = re.findall(r'\[([^\]]*)\]',l)
        bad = False
        for s in m:
            if has_abba(s):
                bad = True
                #print(f"{s} has abba")
        if bad: continue
        if has_abba(l):
            c += 1
            # print(f"{c} {l}")
    return c

def do_part2(db):
    c = 0
    for l in db:
        bad = True
        hypers = re.findall(r'\[([^\]]*)\]',l)
        supers = get_supers(l)
        abas = get_abas(supers)
        print(f"supers: {supers}    abas:{abas}")
        if not len(abas): continue
        for aba in abas:
            bab = aba[1]+aba[0]+aba[1]
            for s in hypers:
                if bab in s: bad = False
        if not bad: c+=1
    return c

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")



