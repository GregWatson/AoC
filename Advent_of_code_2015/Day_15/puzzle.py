#import argparse
import sys
import re
import functools
import array
import copy
import json
import itertools

input_file_name = 'input.txt'
print_on = False
ings = ['Sugar','Sprinkles', 'Candy', 'Chocolate']



def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def load_info(db):
    props = {}
    cals = {}
    for l in db:
        m = re.match(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)',l)
        if m:
            ingredient = m.group(1)
            cap, dur, fla, tex, cal = int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6))
            print(f"{ingredient} {cap, dur, fla, tex, cal}")
            props[ingredient]=[cap, dur, fla, tex]
            cals[ingredient] = cal
    return props,cals

def get_score(props, tsps):
    cap,spr,fla,tex = 0,0,0,0
    for i,ing in enumerate(ings):
        cap += tsps[i] * props[ing][0]
        spr += tsps[i] * props[ing][1]
        fla += tsps[i] * props[ing][2]
        tex += tsps[i] * props[ing][3]
    if cap < 0: cap = 0
    if spr < 0: spr = 0
    if fla < 0: fla = 0
    if tex < 0: tex = 0
    tot = cap * spr * fla * tex
    # print(f"{tsps} {cap,spr,fla,tex} {tot}")
    return tot


def do_part1(db):
    tot = 0
    props, cals= load_info(db)
    for sugar in range(101):
        print(f"{sugar}  \r",end='')
        after_sugar = 100-sugar
        for sprinkles in range(after_sugar+1):
            after_sprinkles = after_sugar - sprinkles
            for candy in range(after_sprinkles+1):
                after_candy = after_sprinkles - candy
                for chocolate in range(after_candy+1):
                    s = get_score(props, [sugar,sprinkles,candy,chocolate])
                    if s > tot: tot = s
    print("")
    return tot


def do_part2(db):
    tot = 0
    props,cals = load_info(db)
    for sugar in range(101):
        print(f"{sugar}  \r",end='')
        after_sugar = 100-sugar
        for sprinkles in range(after_sugar+1):
            after_sprinkles = after_sugar - sprinkles
            for candy in range(after_sprinkles+1):
                after_candy = after_sprinkles - candy
                for chocolate in range(after_candy+1):
                    s = get_score(props, [sugar,sprinkles,candy,chocolate])
                    if s > tot: 
                        cal = sugar*cals['Sugar'] + sprinkles*cals['Sprinkles'] + candy*cals['Candy']+ chocolate*cals['Chocolate']
                        if cal == 500:
                            tot = s
    print("") 


    return tot

    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")

