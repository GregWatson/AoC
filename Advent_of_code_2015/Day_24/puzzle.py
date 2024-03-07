#import argparse
import sys
import re
import functools
import array
import copy
import itertools
import math

input_file_name = 'input.txt'
print_on = False
W = [1,3,5,11,13,17,19,23,29,31,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
Group_Weight3 = round(sum(W)/3)
Group_Weight4 = round(sum(W)/4)

def get_valid_lists(L,num, Group_Weight):
    combs = list(itertools.combinations(L,num))
    valids = [ l for l in combs if sum(l) == Group_Weight ]
    return valids

def do_part1():
    print(f"{len(W)} gifts. Group weight is {Group_Weight3}   (total is {sum(W)})")
    c = 0
    min_qe = 99000000000
    for num in [6]:
        g1 = get_valid_lists(W,num,Group_Weight3)
        for g1x, g1l in enumerate(g1):
            qe = math.prod(g1l)
            if qe >= min_qe: continue
            restL = [ i for i in W if not i in g1l ]
            for num2 in [6,8,10]:
                g2 = get_valid_lists(restL,num2,Group_Weight3)
                if len(g2): min_qe = qe
    return min_qe

def do_part2():
    print(f"{len(W)} gifts. Group weight is {Group_Weight4}   (total is {sum(W)})")
    c = 0
    min_qe = 999999999
    for num in [5]:
        g1 = get_valid_lists(W,num,Group_Weight4)
        for g1x, g1l in enumerate(g1):
            qe = math.prod(g1l)
            if qe >= min_qe: continue
            restL = [ i for i in W if not i in g1l ]
            for num2 in [5,7,9,11]:
                g2 = get_valid_lists(restL,num2,Group_Weight4)
                for g2x,g2l in enumerate(g2):
                    print(f"{g1x}/{len(g1)}  {g2x}/{len(g2)} \r",end='')
                    rest2L = [ i for i in restL if not i in g2l ]
                    for num3 in [5,7,9,11]:
                        g3 = get_valid_lists(rest2L, num3, Group_Weight4)
                        if len(g3): min_qe = qe
    print("")
    return min_qe
   
    

#---------------------------------------------------------------------------------------
#p1 = do_part1()
#print(f"Part 1 is {p1}")

p2 = do_part2()
print(f"Total for part 2 is {p2}.")



