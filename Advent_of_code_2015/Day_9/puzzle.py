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

def parse(db):
    global num_towns
    global towns
    dists = {}
    for l in db:
        m = re.match(r'(\w+) to (\w+) = (\d+)',l)
        if m:
            a = m.group(1)
            b = m.group(2)
            d = int(m.group(3))
            if a in dists:
                dists[a][b] = d
            else:
                dists[a] = {b:d}
                towns.append(a)
            if b in dists:
                dists[b][a] = d
            else:
                dists[b] = {a:d}
                towns.append(b)
            
        else:
            print("Bad format")
            sys.exit(1)

    for a in dists:
        for b in dists[a]:
            # print(f"{a}->{b} = {dists[a][b]}")
            pass
    num_towns = len(dists.keys())
    return dists

def get_sp(a,b,dist_so_far=0, path_so_far=[]):
    if print_on: print(f"get_sp {a} -> {b}.  Path so far is {path_so_far}")
    psf = path_so_far if len(path_so_far) > 0 else [a]
    dsf = dist_so_far
    if len(psf) == num_towns-1: # final hop
        dsf += dists[psf[-1]][b]
        if print_on: print(f"Path {psf},{b} is {dsf}")
        psf.append(b)
        return dsf, psf
    shortest = 9999
    chosen_nexthop = None
    for nexthop in towns:
        if nexthop in psf: continue
        if nexthop == b: continue
        psf_new = psf[:]
        psf_new.append(nexthop)
        if print_on: print(f"a {a} b {b}   next hop {nexthop}    psf is {psf_new} ")
        nhd, p = get_sp(a,b,dsf + dists[psf[-1]][nexthop], psf_new)
        if nhd < shortest:
            chosen_nexthop = nexthop
            shortest = nhd
            shortest_p = p
    if chosen_nexthop is None:
        print(f"Error - no path from {a} to {b} and path so far is {path_so_far}")
        sys.exit(1)
    return shortest, shortest_p

def get_lp(a,b,dist_so_far=0, path_so_far=[]):
    if print_on: print(f"get_lp {a} -> {b}.  Path so far is {path_so_far}")
    psf = path_so_far if len(path_so_far) > 0 else [a]
    dsf = dist_so_far
    if len(psf) == num_towns-1: # final hop
        dsf += dists[psf[-1]][b]
        if print_on: print(f"Path {psf},{b} is {dsf}")
        psf.append(b)
        return dsf, psf
    longest = 0
    chosen_nexthop = None
    for nexthop in towns:
        if nexthop in psf: continue
        if nexthop == b: continue
        psf_new = psf[:]
        psf_new.append(nexthop)
        if print_on: print(f"a {a} b {b}   next hop {nexthop}    psf is {psf_new} ")
        nhd, p = get_lp(a,b,dsf + dists[psf[-1]][nexthop], psf_new)
        if nhd > longest:
            chosen_nexthop = nexthop
            longest = nhd
            longest_p = p
    if chosen_nexthop is None:
        print(f"Error - no path from {a} to {b} and path so far is {path_so_far}")
        sys.exit(1)
    return longest, longest_p


def do_part1(db):
    global dists
    dists = parse(db)
    tot = 99999
    for i,a in enumerate(towns[:-1]):
        for j in range(i+1,len(towns)):
            d,p = get_sp(a, towns[j])
            if d < tot: 
                tot = d
                print(f"    So far shortest is {d} : {p}")
    print(f"shortest is {d}")
    return tot



def do_part2(db):
    global dists
    tot = 0
    for i,a in enumerate(towns[:-1]):
        for j in range(i+1,len(towns)):
            d,p = get_lp(a, towns[j])
            if d > tot: 
                tot = d
                print(f"    So far shortest is {d} : {p}")
    print(f"shortest is {d}")
    return tot

    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")


p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



