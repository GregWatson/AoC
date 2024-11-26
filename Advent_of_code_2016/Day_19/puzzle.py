#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools

input_file_name = 'input.txt'
print_on = False


def doPart1(numELves):
    a = array.array('l',[1 for i in range(numELves)])
    pos = 0
    next = 1
    while True:
        # print(f"a is {a}   pos={pos}  next={next}")
        if next == pos: return pos+1
        if a[next] == 0: 
            next = (next+1)%numELves
        else:
            a[next]=0 
            # print(f"{pos} took from {next}")
            pos = (next+1)%numELves
            while a[pos]==0 : pos= (pos+1)%numELves
            next = (pos+1)%numELves


def doPart2(numELves):
    a = array.array('l',[i for i in range(numELves)])
    pos = 0
    N = len(a)
    while N>1:
        opp = (pos + (N>>1))%N
        oppElf= a.pop(opp)
        if N%1000==0: print(f'circle={N}  elf={a[pos]+1} (pos={pos+1})  steals from elf {oppElf+1} at pos {opp}')
        N = N-1
        if opp > pos: pos=(pos+1)
        pos = pos%N
    return a[0]+1
        



#---------------------------------------------------------------------------------------
# Load input

p1 = doPart1(3004953)
print(f"Part 1 is {p1}")

p2 = doPart2(3004953)
print(f"Part 2 is {p2}.")



