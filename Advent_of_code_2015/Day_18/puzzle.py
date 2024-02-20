#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def load_init_config(db):
    lights = [ array.array('i', [0]*100) for y in range(100) ]
    for y,l in enumerate(db):
        if len(l)>=100:
            for x in range(100):
                lights[y][x] = 1 if l[x] == '#' else 0
    return lights

def get_num_on(l,x,y):
    s = 0
    for xd in range(3):
        for yd in range(3):
            tx = x + xd - 1
            ty = y + yd - 1
            if xd == 1 and yd == 1 or (tx < 0 or tx > 99 or ty < 0 or ty > 99): 
                continue
            s += l[ty][tx]
            if s > 8:
                print("ERROR")
                sys.exit(1)
    return s

def do_cycle(l):
    newl = [ array.array('i', [0]*100) for y in range(100) ]
    for y in range(100):
        for x in range(100):
            num_on = get_num_on(l,x,y)
            if num_on == 3 or (l[y][x]==1 and num_on ==2):
                newl[y][x] = 1
            
    return newl

def count_lights_on(l):
    s = 0
    for y in range(100):
        for x in range(100):
            if l[y][x] == 1: s += 1
    return s

def print_lights(l):
    s = 0
    for y in range(100):
        lc = 0
        for x in range(100):
            if l[y][x] == 1: 
                print('#',end='')
                lc += 1
            else: print('.',end='')
        s += lc
        print(f" lc={lc}   tot={s}")
    print('')

def do_part1(db):
    tot= 0
    lights = load_init_config(db)
    for t in range(100):
        lights = do_cycle(lights)
        print(f"{t}")
        print_lights(lights)

    tot = count_lights_on(lights)        
    return tot



def do_part2(db):
    tot= 0
    lights = load_init_config(db)
    for t in range(100):
        lights[0][0] = 1
        lights[99][0] = 1
        lights[99][99] = 1
        lights[0][99] = 1
        lights = do_cycle(lights)
        print(f"{t}")
        print_lights(lights)

    lights[0][0] = 1
    lights[99][0] = 1
    lights[99][99] = 1
    lights[0][99] = 1

    tot = count_lights_on(lights)        
    return tot




#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



