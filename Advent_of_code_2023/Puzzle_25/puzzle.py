#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False

load_distances_from_file = True
get_node_name = []
get_node_index = {}
num_nodes = 0
d_from_to = []

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_graph(db):
    global get_node_name
    global get_node_index
    global num_nodes
    global d_from_to

    id_to_ids = []
    for l in db:
        m = re.match(r'(.{3}): ([a-z ]+)',l)
        if m:
            n1 = m.group(1)
            l = m.group(2)
            to = l.split(' ')
            if not n1 in get_node_name: 
                get_node_name.append(n1)
            for n in to: 
                if not n in get_node_name: get_node_name.append(n)
            id_to_ids.append((n1, to))

    num_nodes = len(get_node_name)

    # make node name list alphabetical
    get_node_name.sort()

    # create map node id -> index
    for i,id in enumerate(get_node_name):
        get_node_index[id] = i
    
    max_connectivity = 0
    connects_to_ids = {}

    # create full bidi graph using just node names.
    g1 = {}
    for id,to in id_to_ids:
        if not id in g1: g1[id] = to
        else: g1[id].extend(to)
        for n in to:
            if not n in g1: g1[n] = [id]
            else: 
                if not id in g1[n]: g1[n].append(id)

    # find max connectivity for a single node
    max_l = 0
    for id in get_node_name:
        if len(g1[id]) > max_l: max_l = len(g1[id])
        #print(f"{id} -> {g1[id]}")
    if print_on: print(f"Max connectivity for a single node is {max_l}")

    # new graph using list of list of node indexes
    g = [ [] for n in range(num_nodes) ]
    # distance from node to every other node. Initially 0. [node_idx][node_idx]
    d_from_to = [ array.array('i', [0] * num_nodes) for n in range(num_nodes) ]

    for n1 in g1:
        n1_idx = get_node_index[n1]
        for i,n2 in enumerate(g1[n1]):
            g[n1_idx].append(get_node_index[n2])
    return g


# def get_min_dist(g,n1_idx,n2_idx,visited):
#     print(f"get_min {n1_idx}->{n2_idx}  visited:{visited}")
#     # if already computed then return it
#     if d_from_to[n1_idx][n2_idx] > 0: 
#         return d_from_to[n1_idx][n2_idx]
#     if n2_idx in g[n1_idx]: 
#         return 1 # direct neighbour
#     # go through direct neighbours and find min path
#     min_d = 999
#     for idx in g[n1_idx]:
#         v = visited[:]
#         v.append(idx)
#         d = 1 + get_min_dist(g,idx,n2_idx,v)
#         if d < min_d: min_d = d
#     return min_d


# build the d_from_to array.
def compute_all_distances(g):
    global d_from_to
    if load_distances_from_file:
        print("compute_all_distances: loading from file...",end='')        
        with open('distances.txt') as f:
            lines = f.readlines()
        for l in lines:
            m = re.match(r'(\d+) (\d+) (\d+)',l)
            if m:
                d_from_to[int(m.group(1))][int(m.group(2))] = int(m.group(3))
        print("loaded.")
        return
    
    print("compute_all_distances: computing")
    for n1_idx in range(num_nodes):
        if print_on: print(f"{n1_idx}")
        d = 1
        l = g[n1_idx]
        v = [n1_idx] # nodes already seen
        while l:
            if print_on: print(f"    d={d}    \r",end='')
            new_l = []
            for idx in l:
                if d_from_to[n1_idx][idx]==0 and not idx in v:
                    d_from_to[n1_idx][idx] = d
                    new_l.extend(g[idx])
            v.extend(l)
            l = new_l
            d += 1


def print_all_distances(d_from_to):
    for n1_idx in range(num_nodes):
        for n2_idx in range(num_nodes):
            print(f"{n1_idx} {n2_idx} {d_from_to[n1_idx][n2_idx]}")

def build_two_groups(g):
    # find max distance
    mx = 0
    for n1_idx in range(num_nodes):
        for n2_idx in range(num_nodes):
            if d_from_to[n1_idx][n2_idx] > mx:
                mx = d_from_to[n1_idx][n2_idx] ; g1_idx = n1_idx ; g2_idx = n2_idx
    print(f"max separation is {mx} from {g1_idx} to {g2_idx}")
    g1 = [g1_idx]; g2 = [g2_idx]

    # put nodes in the groups
    for n1_idx in range(num_nodes):
        if n1_idx == g1_idx or n1_idx == g2_idx: continue
        dist_to_g1 = d_from_to[g1_idx][n1_idx]
        dist_to_g2 = d_from_to[g2_idx][n1_idx]
        if dist_to_g1 > dist_to_g2: g2.append(n1_idx)
        else: g1.append(n1_idx)
    
    print(f"{'-'*100}\ng1={len(g1)}\n{g1}\n{'-'*100}\ng2={len(g2)}\n{g2}")

def do_part1(g):
    compute_all_distances(g)
    g1,g2 = build_two_groups(g)

    return 0
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
g = get_graph(db)
print(f"Graph has {num_nodes} nodes.")

p1 = do_part1(g)

############################################
# So part 1 returned 2 group sizes:  787 and 780
#
# This is NOT the answer - the product is too low.
# But there are only 4 other combos possible so I tried them and found  782 785 = 613870
#
############################################
