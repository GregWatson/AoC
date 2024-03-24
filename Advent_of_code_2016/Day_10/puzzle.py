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
outputs = [[] for i in range(21)]

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def get_bots(db):
    bots = [{'has':[], 'gives_low':None, 't1':None, 't2':None, 'gives_high':None} for i in range(210) ]
    has2 = []
    for l in db:
        m = re.match(r'value (\d+) goes to bot (\d+)',l)
        if m:
            v,b=int(m.group(1)), int(m.group(2))
            bots[b]['has'].append(v)
            if len(bots[b]['has']) == 2: has2.append(b)
            if len(bots[b]['has']) > 2:
                print(f"Error too many chips at bot {b}")
                sys.exit(1)
            continue
        m = re.match(r'bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+).*',l)
        if m:
            b,t1,lo, t2,hi=int(m.group(1)), m.group(2),int(m.group(3)),m.group(4),int(m.group(5))
            bots[b]['t1'] = t1
            bots[b]['t2'] = t2
            bots[b]['gives_low'] = lo
            bots[b]['gives_high'] = hi
            continue
        print(f"Unparsed input {l}")
        sys.exit(1)
    return bots, has2

def run_bots(bots, has2):
    global outputs
    b = has2.pop()
    print(f"has2 len={len(has2)}   Proc bot {b}   has:{bots[b]['has']}  low to {bots[b]['t1']} {bots[b]['gives_low']}   high to {bots[b]['t2']} {bots[b]['gives_high']} ")
    assert(len(bots[b]['has'])>1)
    lo = min(bots[b]['has'][0:2])
    hi = max(bots[b]['has'][0:2])
    glo = bots[b]['gives_low']
    ghi = bots[b]['gives_high']
    bots[b]['has'] = bots[b]['has'][2:]
    if bots[b]['t1'] == 'output': outputs[glo].append(lo)
    else: bots[glo]['has'].append(lo)
    if len(bots[glo]['has']) == 2: has2.append(glo)
    if bots[b]['t2'] == 'output': outputs[ghi].append(hi)
    else: bots[ghi]['has'].append(hi)
    if len(bots[ghi]['has']) == 2: has2.append(ghi)
    return b, lo, hi

def do_part1(db):
    o = 0
    bots,has2 = get_bots(db)
    b, lo,hi = run_bots(bots, has2)
    while lo != 17 or hi != 61:
        b, lo,hi = run_bots(bots, has2)

    return b



def do_part2(db):
    global outputs
    outputs = [[] for i in range(21)]
    bots,has2 = get_bots(db)
    b, lo,hi = run_bots(bots, has2)
    while (len(outputs[0]) < 1) or (len(outputs[1]) < 1) or (len(outputs[2]) < 1):
        b, lo,hi = run_bots(bots, has2)
    o = outputs[0][0] * outputs[1][0] * outputs[2][0]
    return o

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")



