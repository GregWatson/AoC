#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False
num_towns = 0
dists = {}
towns = []

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_new_s(s):
    news = ''
    last_c = 'x'
    rep = 0
    for i,c in enumerate(list(s)):
        if c != last_c:
            if rep:
                news += str(rep) + last_c
                rep = 0
        rep += 1
        last_c = c
    news += str(rep) + last_c
    return news

def do_part1(s):
    for r in range(40):
        s = get_new_s(s)
        print(f"{r} {s} {len(s)}")


    return 0



def do_part2(s):
    for r in range(50):
        s = get_new_s(s)
        print(f"{r} {s} {len(s)}")


    return 0

    

#---------------------------------------------------------------------------------------
# Load input
#db = load_db()
#print(f"Loaded {len(db)} lines from input")


#p1 = do_part1('1113222113')
#print(f"Part 1 is {p1}")

p2 = do_part2('1113222113')
#print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



