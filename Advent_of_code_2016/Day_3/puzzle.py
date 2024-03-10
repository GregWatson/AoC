import sys
import re
import functools
import array
import copy

def load_db():
    with open('input.txt') as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def do_part1(db):
    tot = 0
    for l in db:
        m = re.match(r' *(\d+) +(\d+) +(\d+)',l)
        if m:
            (a,b,c) = (int(m.group(1)), int(m.group(2)),int(m.group(3)))
            if (a < (b + c)) and ( b<(a+c)) and (c<(a+b)) :
                tot+=1
    return tot

def do_part2(db):
    tot = 0
    r = 0
    for l in db:
        m = re.match(r' *(\d+) +(\d+) +(\d+)',l)
        if m:
            (a,b,c) = (int(m.group(1)), int(m.group(2)),int(m.group(3)))
            if r % 3 == 0:
                n = [ [a], [b], [c] ]
            else:
                n[0].append(a)
                n[1].append(b)
                n[2].append(c)
            print(f"{r}, {n}")
            if r % 3 == 2:
                for l in n:
                    print(f"Check {l}")
                    if (l[0]< (l[1] + l[2])) and  l[1]<(l[0]+l[2]) and (l[2]<(l[0]+l[1])) :
                        tot+=1

            r += 1
    return tot

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"saw {len(db)} lines")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")

