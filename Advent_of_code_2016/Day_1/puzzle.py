#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = True
db = "L1, L3, L5, L3, R1, L4, L5, R1, R3, L5, R1, L3, L2, L3, R2, R2, L3, L3, R1, L2, R1, L3, L2, R4, R2, L5, R4, L5, R4, L2, R3, L2, R4, R1, L5, L4, R1, L2, R3, R1, R2, L4, R1, L2, R3, L2, L3, R5, L192, R4, L5, R4, L1, R4, L4, R2, L5, R45, L2, L5, R4, R5, L3, R5, R77, R2, R5, L5, R1, R4, L4, L4, R2, L4, L1, R191, R1, L1, L2, L2, L4, L3, R1, L3, R1, R5, R3, L1, L4, L2, L3, L1, L1, R5, L4, R1, L3, R1, L2, R1, R4, R5, L4, L2, R4, R5, L1, L2, R3, L4, R2, R2, R3, L2, L3, L5, R3, R1, L4, L3, R4, R2, R2, R2, R1, L4, R4, R1, R2, R1, L2, L2, R4, L1, L2, R3, L3, L5, L4, R4, L3, L1, L5, L3, L5, R5, L5, L4, L2, R1, L2, L4, L2, L4, L1, R4, R4, R5, R1, L4, R2, L4, L2, L4, R2, L4, L1, L2, R1, R4, R3, R2, R2, R5, L1, L2".split(', ')
newdirs = { 'N': {'L':'W', 'R':'E'},
            'W': {'L':'S', 'R':'N'},
            'S': {'L':'E', 'R':'W'},
            'E': {'L':'N', 'R':'S'}
           }
def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def do_instr(x,y,dir, i):
    d = i[0:1]
    nx = x
    ny = y
    if not d in 'LR':
        sys.exit(1)
    new_dir = newdirs[dir][d]
    dist = int(i[1:])
    if new_dir == 'N' : ny = y - dist
    elif new_dir == 'S' : ny = y + dist
    elif new_dir == 'W' : nx = x - dist
    elif new_dir == 'E' : nx = x + dist
    return (nx, ny, new_dir)

def do_instr2(x,y,dir, i, seen):
    d = i[0:1]
    nx = x
    ny = y
    if not d in 'LR':
        sys.exit(1)
    new_dir = newdirs[dir][d]
    dist = int(i[1:])
    while dist > 0:
        if   new_dir == 'N' : ny = ny - 1
        elif new_dir == 'S' : ny = ny + 1
        elif new_dir == 'W' : nx = nx - 1
        elif new_dir == 'E' : nx = nx + 1
        coords= (nx,ny)
        if coords in seen:
            return(nx,ny,new_dir,True)
        seen.add(coords)
        dist -= 1
    return (nx, ny, new_dir, False)


def do_part1(db):
    print(f"{db}")
    x = 0
    y = 0
    dir  = 'N'
    for i in db:
        x,y,dir = do_instr(x,y,dir,i)
    print(f"x is {x}  y is {y}")
    return abs(x) + abs(y)

def do_part2(db):
    seen = set()
    x, y = 0,0
    dir  = 'N'
    for i in db:
        seen.add((x,y))
        x,y,dir,done = do_instr2(x,y,dir,i,seen)
        if done:
            print(f"x is {x}  y is {y}")
            return abs(x) + abs(y)
    print("No answer")
    return 0

#---------------------------------------------------------------------------------------
# Load input

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")

