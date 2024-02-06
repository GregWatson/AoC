#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False
next_plus_1 = {}
next_plus_2 = {}
for i in range(97,123):
    c = chr(i)
    next_plus_1[c] = chr(i+1)
    next_plus_1['h'] = 'j'
    next_plus_1['n'] = 'p'
    next_plus_1['k'] = 'm'
    next_plus_1['z'] = 'a'
for i in range(97,123):
    c = chr(i)
    next_plus_2[c] = next_plus_1[next_plus_1[c]]


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def check_ok(w):
    # Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    # Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
    # Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
    overlap_count = 0
    last_c = '0'
    for c in w:
        if c in 'iol': return False
        if c == last_c:
            overlap_count += 1
            last_c = '0'
        else:
            last_c = c
    if overlap_count < 2: return False
    l = list(w)
    for i,c in enumerate(l[:-2]):
        if c != 'y' and c != 'z':
            if l[i+1] == next_plus_1[c] and l[i+2] == next_plus_2[c]: return True
    else:
        return False

def next_word(w):
    l = list(w)
    for i in range(len(l)-1,0,-1):
        l[i] = next_plus_1[l[i]]
        if l[i] != 'a':
            return ''.join(l)
    print(f"NO NEXT STRING!")
    sys.exit(1)



def do_part1(db):
    w = db
    while not(check_ok(w)):
        w = next_word(w)
    return w



def do_part2(db):

    return tot

    

#---------------------------------------------------------------------------------------
# Load input
#db = load_db()
#print(f"Loaded {len(db)} lines from input")

db = 'vzbxkghb'
p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part1('vzbxxzaa')
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")

