#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = True
EPSILON = 1e-15

class Equation():
    def __init__(self,x,y,z,vx,vy,vz):
        self.x=x; self.y=y; self.z=z  # start point
        self.vx=vx; self.vy=vy; self.vz=vz; #speed vector
        self.m = vy/vx        # as in y=mx+b (slope)
        self.b = y - self.m*x # as in y=mx+b (y intercept)

    def same_2Dgradient_as(self,e):
        if (self.m > 0 and e.m < 0) or (self.m < 0 and e.m > 0): return False
        # have same +ve or -ve slope
        d = abs(abs(self.m) - abs(e.m)) # difference between slopes
        return d <= EPSILON

    def get_intersection_with(self,e):
        x = (e.b - self.b)/(self.m - e.m)
        y = e.m * x + e.b
        return x,y

    def str(self):
        return(f"Y = {self.m}*X + {self.b}")

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_equations(db):
    eqs = []
    for i,l in enumerate(db):
        m = re.match(r'(\d+), (\d+), (\d+) @ (-?\d+), (-?\d+), (-?\d+)',l)
        if m:
            eq = Equation(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)) )
            eqs.append(eq)
            print(f"{i}  {eq.str()}")
        else:
            print(f"Unknown data format line: {l}")
    if print_on: print(f"Loaded {len(eqs)} equations")
    return eqs

# return true if collision point for e1 and e2 (which is(x,y)) occurs after start
def collision_after_start(x,e1,e2):
    e1_ok = (e1.vx > 0 and x >= e1.x) or (e1.vx < 0 and x <= e1.x)
    e2_ok = (e2.vx > 0 and x >= e2.x) or (e2.vx < 0 and x <= e2.x)
    return e1_ok and e2_ok

def point_in_2Dbox(x,y,box): # box ix x0,x1,y0,y1
    return x >= box[0] and x <= box[1] and y >= box[2] and y <= box[3]

# see if hail collide
def hail_collides(e1, e2, box):
    if e1.same_2Dgradient_as(e2):
        if print_on: print(f"Same slopes: {e1.str()} and {e2.str()}")
        return False
    # find intersection
    x,y = e1.get_intersection_with(e2)
    if collision_after_start(x,e1,e2):
        if point_in_2Dbox(x,y,box):
            return True

def do_part1(eqs, box):
    c = 0
    for i1 in range(len(eqs)-1):
        for i2 in range(i1+1, len(eqs)):
            e1=eqs[i1]; e2=eqs[i2]
            if hail_collides(e1,e2,box): c += 1
    return c

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
x_max = len(db[0])
y_max = len(db)

eqs = get_equations(db)
box=(200000000000000, 400000000000000,200000000000000, 400000000000000)
p1 = do_part1(eqs, box)
print(f"Part 1 is {p1}")

for e in eqs[0:4]: print(f"{e.str()}")
#print_map(map)
#p2 = do_part2(map)
#print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")
######################################################################
#
# Part2 - see p.py for using sympy to solve 9 simultaneous equations
#
######################################################################