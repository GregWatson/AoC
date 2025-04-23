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
    return [ l.strip() for l in lines ]

def get_PsandCs(db):
    parentOf = {}
    childrenOf = {}
    weightOf = {}
    for l in db:
        m = re.match(r'([a-z]+) \((\d+)\)\s*-?>?\s*(.*)',l)
        if m:
            name = m.group(1)
            weight=int(m.group(2))
            rest = m.group(3)
            #print(f"{name}")
            weightOf[name] = weight
            if not name in childrenOf: childrenOf[name] = []
            if not name in parentOf: parentOf[name] = []
            if len(rest):
                children = rest.split(', ')
                # print(f"{name}'s children are {children}")
                for child in children:
                    parentOf[child] = name
                childrenOf[name] = children
    return parentOf, childrenOf, weightOf

def getFullWeightOf(node, childrenOf, weightOf):
    weight = weightOf[node]
    children = childrenOf[node]
    for child in children:
        weight += getFullWeightOf(child, childrenOf, weightOf)
    return weight

def balance(root, childrenOf, weightOf, fullWeightOf, target=0):
    print(f"Balance {root}")
    children = childrenOf[root]
    if not len(children):
        print(f"Must adjust end node. Weight is {weightOf[root]} but target is {target}")
        sys.exit(1)
    childWeights = [fullWeightOf[c] for c in children]
    print(f"{root} => {children}, {childWeights}")
    if childWeights.count(childWeights[0]) == len(childWeights):
        print(f"All child weights are the same ({childWeights[0]}) - must adjust THIS node (weight {weightOf[root]} to hit target {target})")
        sys.exit(1)
    for i,w in enumerate(childWeights):
        if childWeights.count(w) > 1: targetWeight = w
        elif childWeights.count(w) == 1: 
            offweight = w
            offchild = children[i]
    print(f"unbalanced child is {offchild} with weight {offweight} while target is {targetWeight}")
    balance(offchild, childrenOf, weightOf, fullWeightOf, target=targetWeight)


def doPart1(db):
    count = 0
    parentOf, childrenOf, weightOf = get_PsandCs(db)
    for n in weightOf:
        if not len(parentOf[n]): 
            return n

def doPart2(db, root):
    count = 0
    parentOf, childrenOf, weightOf = get_PsandCs(db)
    fullWeightOf = {}
    for n in weightOf: fullWeightOf[n] = getFullWeightOf(n, childrenOf, weightOf)
    balance(root, childrenOf, weightOf, fullWeightOf)

    return count
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db, p1)
print(f"\n\n\n\nPart 2 is {p2}")
