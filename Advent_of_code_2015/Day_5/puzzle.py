#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def do_part1(db):
    #It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    #It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    #It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    tot = 0
    for l in db:
        conditions_met = 0
        m = re.match(r'.*(.)\1.*',l)
        if m:
            conditions_met += 1
            #print(f"Line {l} has {m.group(1)} twice")
        m = re.match(r'.*(ab|cd|pq|xy).*',l)
        if not m:
            conditions_met += 1
            #print(f"Line {l} doesn't have proscribed chars")
        m = re.match(r'.*(a|e|i|o|u).*(a|e|i|o|u).*(a|e|i|o|u).*',l)
        if m:
            conditions_met += 1
            #print(f"Line {l} has 3 vowels")
        
        if conditions_met == 3: tot += 1

    return tot



def do_part2(db):
    tot = 0
    
    # It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    # It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.

    for l in db:
        conditions_met = 0
        m = re.match(r'.*(..).*\1.*',l)
        if m:
            conditions_met += 1
            # print(f"Line {l} has {m.group(1)} twice")

        s = list(l)
        for i,c in enumerate(s[:-2]):
            if s[i] == s[i+2] and s[i] != s[i+1]:
                conditions_met += 1
                print(f"  line was {l}")
                break

        if conditions_met == 2: 
            tot += 1
            print(f"{tot}  {l} matches.  Letter pair is {m.group(1)}")

    return tot
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



