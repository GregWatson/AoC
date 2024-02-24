#import argparse
import sys
import re
import functools
import array
import copy
# import math

input_file_name = 'input.txt'
print_on = False





def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]



def do_part1(db):
    tot= 0
    num = 100000
    fac_sum = 0
    while fac_sum < 3400000:
        num += 1
        fac_sum = num + 1
        last = int(math.sqrt(num))+2
        for i in range(2,last):
            if num % i == 0: 
                fac_sum += i
                fac_sum += num / i
        if num % 1000 == 0:
            print(f"{num} {fac_sum}")
    return num

# Seive of Eratosthenes
def do_part2(db):
    tot=0
    houses = array.array('l', [0] * 10000000)
    for elf in range(1, 1000000):
        for i in range(50):
            hid = (i+1)*elf
            if hid < 10000000:
                houses[(i+1)*elf] += elf*11
    max  = 0
    for tot in range(10000000):
        if houses[tot] > max: 
            max = houses[tot]
            print(f"house {tot} has presents: {max}")
        if houses[tot] >= 34000000:
            return tot
    return -1


#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

#p1 = do_part1(db)
#print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 2 is {p2}.")



