#import argparse
import sys
import re
import functools
import array
import copy
# import math

input_file_name = 'input.txt'
print_on = False

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def exec(l, regs, pc):
        print(f"{pc} {l} {regs}")
        m = re.match(r'(hlf|tpl|inc) (a|b)',l)
        if m:
            i, reg = m.group(1), m.group(2)
            if i == 'hlf': regs[reg] = regs[reg]>>1
            elif i == 'tpl': regs[reg] = regs[reg]*3
            elif i == 'inc': regs[reg] += 1
            pc += 1
            return regs, pc
        m = re.match(r'jmp ([+-]\d+)',l)
        if m:
            pc += int(m.group(1))
            return regs, pc
        m = re.match(r'(jio|jie) (a|b), ([+-]\d+)',l)
        if m:
            i, reg, jmp = m.group(1), m.group(2), int(m.group(3))
            if i == 'jio' and regs[reg] == 1:  pc += jmp
            elif i == 'jie' and regs[reg] % 2 == 0:  pc += jmp
            else: pc += 1
            return regs, pc
        print(f"NO MATCH on {l}")
        return regs, 100


def do_part1(db):
    regs = {'a':0, 'b':0}
    pc = 0
    i_count = 0
    while pc >= 0 and pc < len(db):
         regs, pc = exec(db[pc], regs, pc)
         i_count += 1
    print(f"Done: executed {i_count} instructions.")
    return regs['b']

def do_part2(db):
    regs = {'a':1, 'b':0}
    pc = 0
    i_count = 0
    while pc >= 0 and pc < len(db):
         regs, pc = exec(db[pc], regs, pc)
         i_count += 1
    print(f"Done: executed {i_count} instructions.")
    return regs['b']
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 2 is {p2}.")



