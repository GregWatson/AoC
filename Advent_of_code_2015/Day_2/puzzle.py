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
    for line in db:
        m = re.match(r'(\d+)x(\d+)x(\d+)',line)
        if m:
            h,w,l = int(m.group(1)),int(m.group(2)),int(m.group(3))
            smallest = h*w
            if h >= w and h >= l: smallest = w*l
            if w >= h and w >= l: smallest = h*l
            area = 2*(h*w + h*l + w*l) + smallest
            tot += area
            print(f"{h} {w} {l} {smallest} {area} {tot}")
    return tot



def do_part2(db):
    tot = 0
    for line in db:
        m = re.match(r'(\d+)x(\d+)x(\d+)',line)
        if m:
            h,w,l = int(m.group(1)),int(m.group(2)),int(m.group(3))
            smallest_perim = 2*min([h+w, h+l, l+w])
            ribbon = smallest_perim + h*w*l
            tot += ribbon
            # print(f"{h} {w} {l} {smallest} {area} {tot}")
    return tot



#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



