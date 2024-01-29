#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False
x_max = 0
y_max = 0
z_max = 0
map_sym_to_int = { '#':-1, '.':0, '<':1, '>':2, '^':3, 'v':4}
map_int_to_sym = { -1:'#', 0:'.', 1:'<', 2:'>', 3:'^', 4:'v'}
LAST=(139,139)

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_map(db):
    m = [ array.array('i', [-1]*x_max) for y in range(len(db))]
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            m[y][x]=map_sym_to_int[db[y][x]]
    return m

def print_map(m):
    for y,row in enumerate(m):
        for x in range(len(row)):
            print(map_int_to_sym[m[y][x]],end='')
        print("")
    print("")

def remove_slopes(m):
    for y,row in enumerate(m):
        for x in range(len(row)):
            if m[y][x] > 0: m[y][x]=0
    return m


# Get max len from xs,ys to y=140, given already travelled ds
def get_max_len(m,xs,ys,ds,prevx,prevy,visitedL):
    x =xs; y=ys; d=ds
    px=prevx; py=prevy
    while True:
        # see options
        if y == 140: 
            if print_on: print(f"   +++ ({xs},{ys}) has total dist {d} to exit.  Visited={visitedL}")
            return d
        opts=[]
        #print(f"   currently at {x},{y}. prev={px},{py}")
        for o in [(x+1,y,'<'),(x-1,y,'>'),(x,y+1,'^'),(x,y-1,'v')]:
            #print(f"      checking option {o[0]},{o[1]}:")
            if o[0]==px and o[1]==py: 
                #print(f"         - option is same as prev")
                continue # cant go back
            for v in visitedL:
                if o[0] == v[0] and o[1] == v[1]: continue
            i = m[o[1]][o[0]]
            # print(f"      map at {o[0]},{o[1]} is {i}")
            if i == -1: continue # forest, cant go there
            if i == map_sym_to_int[o[2]]: continue # cant go against slope
            if o[1] == 140: 
                # print(f"   +++ ({xs},{ys}) has total dist {d+1} to exit.  Visited={visitedL}")
                return d+1 # exited
            opts.append(o)
        if not len(opts): return -1  # no path
        d=d+1
        # print(f"     So valid opts are {opts}")

        if len(opts)==1: # just one option
            px=x;py=y
            o=opts[0]
            x=o[0]; y=o[1]
            for v in visitedL:
                if o[0] == v[0] and o[1] == v[1]: return -1
        else: # branch
            visitedL.append((x,y))
            ml = 0 # max dist seen
            if print_on: print(f"AT {x},{y}. d is {d} Paths: {opts}")
            for o in opts:
                v = copy.deepcopy(visitedL)
                dist = get_max_len(m, o[0],o[1],d,x,y,v)
                if dist > ml:
                    ml = dist
            if ml > 0: 
                return ml
            else: 
                return -1

def is_node(x,y,m):
    if m[y][x] == -1: return False
    if x==1 and y==1: return True
    if x==139 and y==139: return True
    num_exits = 0
    for o in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if m[o[1]][o[0]] != -1: num_exits += 1
    return num_exits > 2

def get_node_list(m):
    # a node has 3 or more exits
    nl=[(1,1),(139,139)]
    for y in range(1,y_max-1):
        for x in range(1,x_max-1):
            if is_node(x,y,m):
                nl.append((x,y))

    print(f"{len(nl)} Nodes are {nl}")
    return nl

# track x,y to next node, return distance and (x,y) of end node
def track_edge_to_node(m,sx,sy,spx,spy,nl):
    x,y,px,py = sx,sy,spx,spy
    d = 1
    while not (x,y) in nl:
        if print_on: print(f"Track start({sx},{sy}) :  currently at {x},{y}.  Prev {px},{py}")
        num_exits = 0
        nx,ny=0,0
        for o in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:   
            if o[0]==px and o[1]==py: continue # never go back
            # print(f"   map({nx},{ny}) is {m[ny][nx]}")
            if m[o[1]][o[0]] != -1: 
                num_exits += 1
                nx,ny = o
        if num_exits == 0: # dead end
            return 0,(-1,-1)
        if num_exits > 1: # must be at node
            if not (x,y) in nl:
                print(f"track_edge_to_node: Expected {x},{y} to be node but not in list")
                sys.exit(1)
            return d,(x,y)
        d += 1
        px,py = x,y
        x,y = nx,ny
    return d,(x,y)
            


# get edges for this node
def get_edges_for_node(n,m,nl):
    x,y = n
    edges_to_nodes = {} # maps node to distance
    for o in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if o[1]==0 or o[1]==140: continue
        if m[o[1]][o[0]] != -1:
            print(f"Get edges for node {x},{y}: start at {o[0]},{o[1]}")
            d,dst = track_edge_to_node(m,o[0],o[1],x,y,nl)
            if d > 0:
                print(f"Edge ({n[0]},{n[1]}) -> ({dst[0]},{dst[1]}) d={d}")
                if dst in edges_to_nodes:
                    if edges_to_nodes[dst] < d:
                        edges_to_nodes[dst] = d # take longest path
                else:
                    edges_to_nodes[dst] = d
    return edges_to_nodes  




# get all edges between nodes and their length
def get_all_edges(m,nl):
    edges = {}
    for n in nl:
        e = get_edges_for_node(n,m,nl)
        edges[n] = e
    # check symmetrical
    for n in edges:
        edges_to_nodes = edges[n]
        for dst_node in edges_to_nodes:
            dist_to_node = edges_to_nodes[dst_node]
            dist_from_node = edges[dst_node][n]
            if dist_to_node != dist_from_node:
                print(f"Dists dont match: {n[0]},{n[1]} -> {dst_node[0]},{dst_node[1]} is {dist_to_node}", end='')
                print(f" but {dst_node[0]},{dst_node[1]} -> {n[0]},{n[1]} is {dist_from_node}")
    return edges

# get hash of list of adjacent nodes 
def get_adj_nodes(el):
    an = {}
    for n in el:
        an[n] = []
        edges = el[n]
        for dst in edges: an[n].append(dst)

    for n in an: print(f"{n} -> {an[n]}")
    return an

def do_part1(map):
    x=1
    y=1
    d=1
    return get_max_len(map,x,y,d,1,0, [])
    
 
# get length of path
def get_len(el, p):
    fn = p[0]
    d = 2
    for tn in p[1:]:
        d += el[fn][tn]
        fn = tn
    return d


def do_part2(map):
    nl = get_node_list(map)
    el = get_all_edges(map, nl)
    adj_nodes = get_adj_nodes(el)

    active_paths = [ [(1,1)] ]
    done_paths = []

    i = 0
    while len(active_paths):
        i += 1
        if i % 10000 ==0: print(f"{len(done_paths)}     \r",end='')
        path = active_paths.pop()
        last_el = path[-1]
        next_hops = adj_nodes[last_el]
        for nh in next_hops:
            if nh == LAST: # exit
                p = path[:]
                p.append(nh)
                done_paths.append(p)
            elif nh in path: continue
            else: # keep going
                p = path[:]
                p.append(nh)
                active_paths.append(p)
    print("")

    ml = 0
    for p in done_paths: 
        # print(f"DONE: {p}")
        l = get_len(el, p)
        if l > ml: ml = l
    return ml







#---------------------------------------------------------------------------------------
# Load input
db = load_db()
x_max = len(db[0])
y_max = len(db)

map = get_map(db)
print_map(map)
p1 = do_part1(map)
print(f"max len is {p1}")

map = remove_slopes(map)
print_map(map)
p2 = do_part2(map)

print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")
