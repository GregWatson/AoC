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
PR=0
CO=1
CU=2
RU=3
PL=4
el_names = ['PR','CO','CU','RU','PL']

class Floors():
    def __init__(self):
        self.gens = array.array('I', [0] * 4)
        self.chips = array.array('I', [0] * 4)
        self.el = 0 # elevator
    
    def place_gen(self,element,floor):
        if (self.gens[floor] & (1 << element)):
            print(f"Err tried to place gen {element} at floor {floor} but already present: gen is {self.gens}")
            sys.exit(1)
        self.gens[floor] |= (1 << element)

    def remove_gen(self,element,floor):
        if not (self.gens[floor] & (1 << element)):
            print(f"Err tried to remove gen {element} from floor {floor} but not present: gen is {self.gens}")
            sys.exit(1)
        self.gens[floor] ^= (1 << element)
        
    def floor_has_gen(self,element,floor):
        return (self.gens[floor] & (1 << element)) != 0

    def place_chip(self,element,floor):
        if (self.chips[floor] & (1 << element)):
            print(f"Err tried to place chip {element} at floor {floor} but already present: chip is {self.chips}")
            sys.exit(1)
        self.chips[floor] |= (1 << element)

    def remove_chip(self,element,floor):
        if not (self.chips[floor] & (1 << element)):
            print(f"Err tried to remove chip {element} from floor {floor} but not present: chip is {self.chips}")
            sys.exit(1)
        self.chips[floor] ^= (1 << element)
        
    def floor_has_chip(self,element,floor):
        return (self.chips[floor] & (1 << element)) != 0

    def show(self):
        s = ''
        for fl in [3,2,1,0]:
            s += "%1d" % fl
            if self.el == fl: s += ' E '
            else: s += '   '
            for el in range(5):
                if self.floor_has_chip(el,fl): s+= 'C:'+el_names[el] + ' '
                else: s += '     '
                if self.floor_has_gen(el,fl): s+= 'G:' + el_names[el] + ' '
                else: s += '     '
            s += "\n"
        return s

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def setup(f):
    f.place_gen(PR,0)
    f.place_chip(PR,0)
    for el in [CO, CU,RU,PL]:
        f.place_gen(el,1)
        f.place_chip(el,2)

def do_part1(db):
    o = 0
    f = Floors()
    setup(f)
    print(f"{f.show()}")

    return o



def do_part2(db):
    o=0
    return o

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")



