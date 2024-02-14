#import argparse
import sys
import re
import functools
import array
import copy
import json

input_file_name = 'input.txt'
print_on = False


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def parse_db(db):
    rspec = {} 
    for l in db:
        m = re.match(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+).*',l)
        if m:
            name, speed, fly_time, rest_time = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            print(f"{name, speed, fly_time, rest_time}")
            rspec[name] = {'speed':speed, 'fly_time':fly_time, 'rest_time':rest_time}
    return rspec

def get_dist(dict,time):
    period = dict['fly_time'] + dict['rest_time']
    dist_per_period = dict['speed'] * dict['fly_time']
    num_periods = int(time/period)
    residue = time % period
    if residue > dict['fly_time']: residue = dict['fly_time']
    dist = num_periods * dict['speed'] * dict['fly_time'] + residue * dict['speed']
    return dist

def do_part1(db):
    tot = 0
    rspec = parse_db(db)
    for n in rspec:
        d = get_dist(rspec[n], 2503)
        if d > tot: tot = d

    return tot

def do_part2(db):
    tot = 0
    rspec = parse_db(db)
    points = {}
    for r in rspec: points[r] = 0

    for step in range(2503):
        dists = {}
        mx = 0
        for r in rspec:
            dists[r] = get_dist(rspec[r], step+1)
            if dists[r] > mx: mx = dists[r]

        for r in rspec:
            if dists[r] == mx: points[r] += 1

    mx = 0
    for r in points:
        if points[r] > mx:
            mx = points[r]
    return mx

    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")

