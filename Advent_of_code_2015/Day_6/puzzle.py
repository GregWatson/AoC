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
    # toggle 936,774 through 937,775
    # turn off 116,843 through 533,934
    # turn on 950,906 through 986,993
    tot= 0
    lights = [ array.array('i', [0]*1000) for y in range(1000) ]
    for l in db:
        m = re.match(r'([^0-9]+) (\d+),(\d+) through (\d+),(\d+)',l)
        if m:
            x1,y1,x2,y2 = int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
            t = m.group(1)
            print(f"{t}, {x1},{y1} - {x2},{y2}")
        else:
            print(f"Unknown format {l}")
            sys.exit(1)
        y = y1;
        while y <= y2:
            x = x1;
            while x <= x2:
                if t == 'turn on': lights[y][x] = 1
                elif t == 'turn off': lights[y][x] = 0
                elif t == 'toggle': lights[y][x] = 1 - lights[y][x]
                else:
                    print(f"Unknown t format {t}")
                    sys.exit(1)
                x += 1
            y += 1

    tot = 0
    for y in range(len(lights)):
        for x in range(1000):
            tot += lights[y][x]

    return tot



def do_part2(db):
    tot = 0
    # toggle 936,774 through 937,775
    # turn off 116,843 through 533,934
    # turn on 950,906 through 986,993
    tot= 0
    lights = [ array.array('i', [0]*1000) for y in range(1000) ]
    for l in db:
        m = re.match(r'([^0-9]+) (\d+),(\d+) through (\d+),(\d+)',l)
        if m:
            x1,y1,x2,y2 = int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
            t = m.group(1)
            print(f"{t}, {x1},{y1} - {x2},{y2}")
        else:
            print(f"Unknown format {l}")
            sys.exit(1)
        y = y1;
        while y <= y2:
            x = x1;
            while x <= x2:
                if t == 'turn on': lights[y][x] += 1
                elif t == 'turn off': 
                    if lights[y][x] > 0: lights[y][x] -= 1

                elif t == 'toggle': lights[y][x] += 2
                else:
                    print(f"Unknown t format {t}")
                    sys.exit(1)
                x += 1
            y += 1

    tot = 0
    for y in range(len(lights)):
        for x in range(1000):
            tot += lights[y][x]

    return tot
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



