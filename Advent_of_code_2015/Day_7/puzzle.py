#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False
NOOP = 0
AND = 1
OR = 2
SET = 3
LSHIFT = 4
RSHIFT = 5
NOT = 6
op2str = ['NOOP','AND','OR','SET','LSHIFT','RSHIFT','NOT']
str2op = {'NOOP':0,'AND':1,'OR':2,'SET':3,'LSHIFT':4,'RSHIFT':5,'NOT':6}


class Logic():
    def __init__(self,s):
        m = re.match(r'NOT (\w+).*',s)
        if m:
            self.op = NOT
            self.val1 = m.group(1)
            self.val2 = None
            return
        m = re.match(r'(\w+) (LSHIFT|RSHIFT|AND|OR) (\w+).*',s)
        if m:
            self.op = str2op[m.group(2)]
            self.val1 = m.group(1)
            self.val2 = m.group(3)
            return
        m = re.match(r'(\w+).*',s)
        if m:
            self.op = SET
            self.val1 = m.group(1)
            self.val2 = None
            return

        print(f"Unknown logic string <{s}>")
        sys.exit(1)

    def valueof(self,cct, wire_or_int):
        if wire_or_int.isdigit(): return int(wire_or_int)
        return cct[wire_or_int].eval(cct)
        
    def eval(self, cct):

        if self.op == NOOP:
            return self.val1
        
        elif self.op == SET:
            value =  self.valueof(cct, self.val1)

        elif self.op == NOT:
            value =  0xffff ^ self.valueof(cct, self.val1)

        elif self.op == AND:
            value =  self.valueof(cct, self.val1) & self.valueof(cct, self.val2)

        elif self.op == OR:
            value =  self.valueof(cct, self.val1) | self.valueof(cct, self.val2)

        elif self.op == LSHIFT:
            value =  self.valueof(cct, self.val1) << self.valueof(cct, self.val2)

        elif self.op == RSHIFT:
            value =  self.valueof(cct, self.val1) >> self.valueof(cct, self.val2)

        else: 
            print(f"Bad op {self.op}")
            sys.exit(1)

        self.op = NOOP
        self.val1 = value
        return value


    def str(self):
        s = op2str[self.op] + '  ' + str(self.val1) + ' ' + str(self.val2)
        return s
    
def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def make_circuit(db):
    cct = {} # hash mapping wire to logic (string) that drives it
    for l in db:
        m = re.match(r'(.*) -> ([a-z]+)',l)
        if m:
            wire = m.group(2)
            cct[wire] = Logic(m.group(1))
            print(f"{wire} is driven by {cct[wire].str()}")
        else:
            sys.exit(1)
    return cct

def do_part1(db):
    tot = 0
    cct = make_circuit(db)
    tot = cct['a'].eval(cct)

    return tot



def do_part2(db):
    tot = 0
 

    return tot
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

#p2 = do_part2(db)
#print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



