#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools
import math
import time
import string

BLENDER=False

# --- Blender ---
if BLENDER:
    import bpy
    sys.path.append(r'C:\cygwin64\home\gwatson\AOC')
    from blenderLib import *
# ---------------

input_file_name = 'input.txt'
print_on = False
BIGNUM=10000000
MAX=141; MINSAVED=100; NUMCHEATS=20


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l for l in lines ]

def getParticles(db):
    particles = []
    for line in db:
        m = re.match(r'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>', line)
        if not m:
            print(f"Error, bad particle line {line}")
            return None
        particles.append( [ int(m.group(i)) for i in range(1,10) ] )
    return particles

def manhattan(p):
    return abs(p[0]) + abs(p[1]) + abs(p[2])

def getClosest(particles):
    closest = -1
    closestDist = BIGNUM
    for i,p in enumerate(particles):
        dist = manhattan(p)
        if dist < closestDist:
            closestDist = dist
            closest = i
    return closest, closestDist

def moveParticle(p):
    p[3] += p[6]
    p[4] += p[7]
    p[5] += p[8]
    p[0] += p[3]
    p[1] += p[4]
    p[2] += p[5]

def deleteCollisions(particles):
    positions = {}
    for i,p in enumerate(particles):
        pos = (p[0], p[1], p[2])
        if pos in positions:
            positions[pos].append(i)
        else:
            positions[pos] = [i]
    toDelete = set()
    for pos, inds in positions.items():
        if len(inds) > 1:
            toDelete.update(inds)
    for index in sorted(toDelete, reverse=True):
        del particles[index]

def doPart1(db):
    particles = getParticles(db)
    lastClosest = -1
    count = 0
    while True:
        count += 1
        if count % 1000 == 0:
            closestIndex, closestIndexDist = getClosest(particles)
            print(f"Closest is {closestIndex} at {closestIndexDist}")
            if closestIndex == lastClosest:
                return closestIndex
            lastClosest = closestIndex
        for p in particles: moveParticle(p)
    
def doPart2(db):
    particles = getParticles(db)
    count = 0
    lastLen = len(particles)
    while True:
        count += 1
        if count % 1000 == 0:
            newLen = len(particles)
            if newLen == lastLen:
                print(f"Stable at {newLen} particles")
                return newLen
            lastLen = newLen
        for p in particles: moveParticle(p)
        deleteCollisions(particles)

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
