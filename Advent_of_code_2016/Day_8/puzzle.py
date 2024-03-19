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
SCREENY = 6
SCREENX = 50

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]
            
def do_part1(db):
    c = 0
    screen = [ array.array('I', [0]*SCREENX) for y in range(SCREENY)]
    for l in db:
        m = re.match(r'rect (\d+)x(\d+)',l)
        if m:
            a,b=int(m.group(1)), int(m.group(2))
            for y in range(b):
                for x in range(a): screen[y][x]=1
            continue

        m = re.match(r'rotate (row y|column x)=(\d+) by (\d+)',l)
        if m:
            t,a,b = m.group(1),int(m.group(2)), int(m.group(3))
            if t == 'row y':
                row = copy.copy(screen[a])
                for x in range(SCREENX): screen[a][(x+b)%SCREENX] = row[x]
            else:
                col = []
                for y in range(SCREENY): col.append(screen[y][a])
                for y in range(SCREENY): screen[(y+b)%SCREENY][a] = col[y]

        count = 0
        for y in range(SCREENY):
            for x in range(SCREENX):
                c = ' '
                if screen[y][x]: 
                    c = '#'
                    count += 1
                print(f"{c}",end='')
            print(" ",)

        print("")
    return count

def do_part2(db):
    c = 0

    return c

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")



