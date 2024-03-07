#import argparse
import sys
import re
import functools
import array
import copy


def do_part1():
    num = 20151125
    next_row = 2
    row = 1
    col = 1
    while ((row != 2978) or (col!=3083)) :
        if row == 1:
            row = next_row
            next_row += 1
            col = 1
        else:
            row -= 1
            col += 1
        num = (num * 252533) % 33554393
        if (row + col) < 5: print(f"{row},{col},{num}")
    return num

def do_part2():
    tot=0
  
    return tot




#---------------------------------------------------------------------------------------
# Load input

p1 = do_part1()
print(f"Part 1 is {p1}")

#p2 = do_part2(db)
#print(f"Total for part 2 is 207.")



