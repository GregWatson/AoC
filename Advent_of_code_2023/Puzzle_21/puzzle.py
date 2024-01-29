#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False
g = []
x_max = 0
y_max = 0
SCALE = 1
ONE_BLOCK_STEPS = 132
SQ_HEIGHT = 2*ONE_BLOCK_STEPS + 1
TOT_STEPS = ((SCALE-1)>>1) * SQ_HEIGHT + ONE_BLOCK_STEPS

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

# grid is [y][x] array of the lowest number of steps it 
# took to get to [y][x] from S
def get_grid(db, y_max, x_max):
    g = [ array.array('i', [-1 for x in range(x_max)]) for y in range(y_max) ]
    for y in range(y_max):
        for x in range(x_max):
            if db[y][x]=='#':
                g[y][x]=TOT_STEPS+99 
    return g

# find the start (S). return as x,y
def find_S(db):
    for y,row in enumerate(db):
        x = row.find('S')
        if x != -1: return(x,y)
    else:
        print(f"Unable to find Start S")
        sys.exit(1)

def loc_add(locs, x, y, steps_left):
    global g
    global x_max
    global y_max
    if x<0 or y<0 or x>=x_max or y >= y_max: return
    if steps_left <= g[y][x]: return
    locs.append((x,y,steps_left))

# locs is list of active locations (x,y,steps_left)
def do_part1(db, x_max, y_max, locs):
    global g
    it = 0
    while locs:
        it += 1
        if it%10000 == 0: 
            # print_g(g, db,x_max)
            print(f"{len(locs)}         \r",end='')
        x,y,steps_left = locs.pop()
        if x<0 or y<0 or x>=x_max or y >= y_max: next
        if steps_left > g[y][x]:
            g[y][x] = steps_left
            if steps_left == 0: next
        else: 
            next # already visited this [y][x] with more steps left.
        # try all 4 around
        loc_add(locs, x-1,y,steps_left-1)
        loc_add(locs, x+1,y,steps_left-1)
        loc_add(locs, x,y-1,steps_left-1)
        loc_add(locs, x,y+1,steps_left-1)

def print_g(g,db,x_max):
    c = 0
    for y,row in enumerate(g):
        for x in range(x_max):
            if db[y][x]=='#': print('#',end='')
            elif g[y][x]>-1: 
                if g[y][x] % 2 == 0 :
                    print('O',end='')
                    #print(f"{g[y][x]}",end='')
                    c += 1
                else: 
                    print('.',end='')
            else: 
                print('.',end='')
        print("")
    print(f"c:{c}")

def count_gardens_reached(g,x_max):
    # steps_left must be even (regardless of max_steps)
    c = 0
    for y,row in enumerate(g):
        for x in range(x_max):
            if g[y][x]>-1 and g[y][x] <= TOT_STEPS and (g[y][x] % 2 == 0) : c+= 1
    return c

def scale_db(db, scale):
    if scale == 1: return db
    wide_db = [l * scale for l in db]
    scaled_db = [wide_db[y % len(wide_db)] for y in range (len(wide_db) * scale) ]
    return scaled_db
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
db = scale_db(db, SCALE)
y_max = len(db)
x_max = len(db[0])
g = get_grid(db,y_max, x_max)
x,y = x_max >> 1, y_max >> 1
print(f"Tot steps is {TOT_STEPS}. grid is Y 0:{y_max-1} and X 0:{x_max-1}. Start at {x},{y}")

do_part1(db, x_max, y_max, locs=[(x,y,TOT_STEPS)])

print_g(g,db,x_max)
c = count_gardens_reached(g,x_max)
print(f"Total gardens reached = {c}")
print(f"SCALE = {SCALE}  ONE_BLOCK_STEPS = {ONE_BLOCK_STEPS}  SQ_HEIGHT = {SQ_HEIGHT}   TOT_STEPS = {TOT_STEPS}")
