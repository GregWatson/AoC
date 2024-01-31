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

def parse(db):
    src_chars = 0
    final_chars= 0 
    for l in db:
        outs = ''
        if len(l) < 3:
            print(f"Line too short <{l}>")
            sys.exit(1)
        src_chars += len(l)
        l1 = l[1:-1]
        print(f"LINE: {l1}  len is {len(l1)}")
        ll = len(l1)
        i = 0
        while i < ll:
            c = l1[i]
            if not c == chr(92):
                #print(f" Not \\")
                i += 1
                outs += c
            else:
                i = i+1
                c = l1[i]
                print(f"i is {i}  c is {c}")
                if c == chr(92):
                    i = i+1
                    outs += chr(92)
                elif c == r'"':
                    i = i+1
                    outs += c
                elif c == "x":
                    i = i+1
                    hex_chars = l1[i:i+2]
                    i = i + 2
                    c = chr(int(hex_chars,16))
                    print(f"hex chars is {hex_chars}")
                    outs += c
                else:
                    print(f"Unknown. i={i} c={c}  line is {l1}")
                    sys.exit(1)

        lo = len(outs)
        final_chars += lo
        print(f"len is {lo}")
    return src_chars - final_chars



def do_part1(db):
    tot = parse(db)
    return tot



def do_part2(db):
    src_chars = 0
    final_chars= 0 
    for l in db:
        outs = ''
        if len(l) < 3:
            print(f"Line too short <{l}>")
            sys.exit(1)
        src_chars += len(l)
        l1 = l[1:-1]  # remove quotes
        print(f"LINE: {l1}  len is {len(l1)}")
        ll = len(l1)
        outl = 6 # the bookend quotes
        i = 0
        while i < ll:
            c = l1[i]
            if not c == chr(92):
                #print(f" Not \\")
                i += 1
                outl += 1
            else:
                outl += 2
                i = i+1
                c = l1[i]
                print(f"i is {i}  c is {c} outl is {outl}")
                if c == chr(92):
                    i = i+1
                    outl += 2
                elif c == r'"':
                    i = i+1
                    outl += 2
                elif c == "x":
                    i = i+1
                    i = i + 2
                    outl += 3
                else:
                    print(f"Unknown. i={i} c={c}  line is {l1}")
                    sys.exit(1)

        print(f"len is {outl}")
        final_chars += outl

    return final_chars - src_chars
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



