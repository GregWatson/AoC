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
    str2hash = "abcdef609043"
    i = 0
    while not done:
        if i % 10000 == 0 : print(f"{i}\r",end='')
        n = "iwrupvqb" + str(i)
        result = hashlib.md5(n.encode())
        r = result.hexdigest()
        if r[0:6] == '000000': 
            print(f"{r} - DONE")
            break
        else:
            i = i + 1

    # printing the equivalent hexadecimal value.
    print("\nThe hexadecimal equivalent of hash is : ", end ="")
    print(f"hex of md5 is {r}. Type is {type(r)}.")

    return i



def do_part2(db):


    return tot
    

#---------------------------------------------------------------------------------------
# Load input
# db = load_db()

db = 1


p1 = do_part1(db)
print(f"Part 1 is {p1}")

#p2 = do_part2(db)
#print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



