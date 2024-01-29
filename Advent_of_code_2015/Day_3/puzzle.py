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

def do_part1(db):
    tot = 0
    x_min, y_min, x_max, y_max = 0,0,0,0
    x,y=20,4049
    h = [ array.array('i',[0]*200) for y in range(5000)]
    h[y][x] = 1
    for c in db[0]:
        if c in '<>^v':
            if c == '>': x += 1
            elif c == '<': x -= 1
            elif c == '^': y -= 1
            else:          y += 1
            
            if x < x_min: x_min = x
            if x > x_max: x_max = x
            if y < y_min: y_min = y
            if y > y_max: y_max = y
            h[y][x] += 1
    print(f"\n{x_min} {x_max} {y_min} {y_max}")

    for y in range(len(h)):
        for x in range(200):
            if h[y][x] > 0: tot += 1

    return tot



def do_part2(db):
    tot = 0
    x_min, y_min, x_max, y_max = 0,0,0,0
    rx_min, ry_min, rx_max, ry_max = 0,0,0,0
    x,y=18,31
    rx,ry=x,y
    h = [ array.array('i',[0]*200) for y in range(200)]
    h[y][x] = 2
    turn = 1 # 0 =santa, 1 = robosanta
    for c in db[0]:
        if c in '<>^v':
            turn = turn + 1
            if turn % 2 == 0:
                if c == '>': x += 1
                elif c == '<': x -= 1
                elif c == '^': y -= 1
                else:          y += 1
                
                if x < x_min: x_min = x
                if x > x_max: x_max = x
                if y < y_min: y_min = y
                if y > y_max: y_max = y
                h[y][x] += 1
                print(f"santa at {x},{y}")
            else:
                if c == '>': rx += 1
                elif c == '<': rx -= 1
                elif c == '^': ry -= 1
                else:          ry += 1
                
                if rx < rx_min: rx_min = rx
                if rx > rx_max: rx_max = rx
                if ry < ry_min: ry_min = ry
                if ry > ry_max: ry_max = ry
                h[ry][rx] += 1
                print(f"robo-santa at {rx},{ry}")


    print(f"\nSanta: {x_min} {x_max} {y_min} {y_max}")
    print(f"Robo Santa: {rx_min} {rx_max} {ry_min} {ry_max}")

    for y in range(len(h)):
        for x in range(200):
            if h[y][x] > 0: tot += 1

    return tot
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



