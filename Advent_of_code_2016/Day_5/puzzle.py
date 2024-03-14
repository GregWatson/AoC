#import argparse
import sys
import re
import functools
import array
import copy
import hashlib

input_file_name = 'input.txt'
print_on = False

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def do_part1(db):
    done = False
    i = 0
    s = ''
    while not done:
        if i % 10000 == 0 : print(f"{i}\r",end='')
        n = "ugkcyxxp" + str(i)
        result = hashlib.md5(n.encode())
        r = result.hexdigest()
        if r[0:5] == '00000': 
            print(f"{r[0:6]}")
            s += r[5]
        i = i + 1
        done = len(s)==8

    # printing the equivalent hexadecimal value.
    return s



def do_part2(db):
    done = False
    i = 0
    s = [ ' ' for i in range(8) ]
    while not done:
        n = "ugkcyxxp" + str(i)
        result = hashlib.md5(n.encode())
        r = result.hexdigest()
        if r[0:5] == '00000': 
            pos = r[5]
            val = r[6]
            if pos in '01234567':
                ipos = int(pos)
                if s[ipos] == ' ': 
                    s[ipos] = val
                    print(f"{s}")
        i = i + 1
        done = not ' ' in s

    # printing the equivalent hexadecimal value.
    return s

#---------------------------------------------------------------------------------------
# Load input
# db = load_db()

db = 1

#p1 = do_part1(db)
#print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



