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

class Point:
    def __init__(self,x,y,z):
        self.x=int(x)
        self.y=int(y)
        self.z=int(z)

    def str(self): # x,y,z
        return(f"({self.x},{self.y},{self.z})")
    
    def copy(self):
        return Point(self.x, self.y, self.z)
    
    def same_as(self,p):
        return self.x == p.x and self.y == p.y and self.z == p.z
    
class Brick: # p1 is lowest z
    def __init__(self,p1,p2):
        if p1.z != p2.z:
            if p1.z <= p2.z:
                self.p1=p1
                self.p2=p2
            else:
                self.p1=p2
                self.p2=p1
            self.len = p2.z - p1.z + 1
        elif p1.x != p2.x:
            if p1.x <= p2.x:
                self.p1=p1
                self.p2=p2
            else:
                self.p1=p2
                self.p2=p1
            self.len = p2.x - p1.x + 1
        else:
            if p1.y <= p2.y:
                self.p1=p1
                self.p2=p2
            else:
                self.p1=p2
                self.p2=p1
            self.len = p2.y - p1.y + 1

    def str(self):
        return f"{self.p1.str()}-{self.p2.str()}" 

class Heap: # 3 d array. index as [z][x][y]
    def __init__(self,z,x,y):
        self.h = []
        for z in range(z):
            a = [ array.array('i', [-1 for y in range(y)]) for x in range(x)]
            self.h.append(a)

    # destroy brick number n from heap and return num cells destroyed
    def destroy(self, n, b, x_max, y_max): 
        z1 = b.p1.z # start z
        z2 = b.p2.z # start z
        c = 0
        for z in range(z1,z2+1):
            for x in range(x_max+1):
                for y in range(y_max+1):
                    if self.h[z][x][y] == n: 
                        self.h[z][x][y] = -1
                        c += 1
        return c

    # see if brick can drop
    def brick_can_drop(self, b_id, brick):
        if  brick.p1.z == 1: return False
        if brick.len == 1 or brick.p1.z != brick.p2.z:
            return self.h[brick.p1.z-1][brick.p1.x][brick.p1.y] == -1
        # brick is in x or y
        vec  = (1,0)
        x = brick.p1.x
        y = brick.p1.y
        z = brick.p1.z
        if brick.p1.y != brick.p2.y:
            vec = (0,1)
        for l in range(brick.len):
            if self.h[z-1][x][y] >= 0: return False
            x += vec[0]
            y += vec[1]
        return True

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_snapshot_list(db):
    snapshot_list = []
    max_b = 0
    for l in db:
        m = re.match(r'(\d+),(\d+),(\d+)\~(\d+),(\d+),(\d+)', l)
        if m:
            p1=Point(m.group(1),m.group(2),m.group(3))
            p2=Point(m.group(4),m.group(5),m.group(6))
            b = Brick(p1,p2)
            if b.len > max_b: max_b = b.len
            snapshot_list.append(b)
    print(f"Longest brick is {max_b}")
    return snapshot_list, max_b

def get_max_xyz(brick_list):
    x,y,z = 0,0,0
    x1 = max([b.p1.x for b in brick_list])
    x2 = max([b.p2.x for b in brick_list])
    y1 = max([b.p1.y for b in brick_list])
    y2 = max([b.p2.y for b in brick_list])
    z1 = max([b.p1.z for b in brick_list])
    z2 = max([b.p2.z for b in brick_list])
    return( max([x1, x2]), max([y1, y2]), max([z1,z2]) )

def print_list_of_bricks(brick_list):
    for b in snapshot_list:
        print(f"({b.p1.x},{b.p1.y},{b.p1.z}) - ({b.p2.x},{b.p2.y},{b.p2.z})")

# place brick in heap at specified location
def heap_add_brick(heap,id, b):
    p1 = b.p1
    p2 = b.p2
    if p1.z != p2.z:
        z = p1.z
        while z <= p2.z:
            heap.h[z][p1.x][p1.y]=id
            z += 1
    elif p1.x != p2.x:
        x = p1.x
        while x <= p2.x:
            heap.h[p1.z][x][p1.y]=id
            x += 1
    else:
        y = p1.y
        while y <= p2.y:
            heap.h[p1.z][p1.x][y]=id
            y += 1

# return the distance that a point can drop
def drop_amount(heap, p):
    z = p.z - 1
    # print(f"drop_amount: point {p.str()}.  Heap at {p.x},{p.y},{z} is {heap.h[z][p.x][p.y]}")
    while (z > 0) and heap.h[z][p.x][p.y] == -1 : 
        #print(f"  --- heap at {p.x},{p.y},{z} is {heap.h[z][p.x][p.y]}")
        z -= 1
    
    return p.z - z - 1

# return number of other bricks that support this brick
def num_supporting_bricks(b, heap):
    if b.p1.z == 1: return 0  # on the floor
    if b.len == 1 or b.p1.z != b.p2.z: # single cell or vertical stack
        if heap.h[b.p1.z-1][b.p1.x][b.p1.y] != -1: 
            return 1
        else:
            print(f"WEIRD - nothing supporting this brick {b.str()}!") 
            return 0

    # check each cell in x or y direction, depending on brick layout
    p = b.p1.copy()
    if b.p1.x != b.p2.x :
        vec=(1,0)
    else: vec=(0,1)
    supporting_bricks = []
    while True:
        # print(f"    num_supporting_bricks:  brick is {b.str()}. Vec is {vec}. Current point is {p.str()}")
        # check cell below p
        brick_below_id = heap.h[p.z-1][p.x][p.y]
        if brick_below_id != -1:
            if not brick_below_id in supporting_bricks:
                supporting_bricks.append(brick_below_id)
        if p.same_as(b.p2): 
            return len(supporting_bricks)
        p.y += vec[1]
        p.x += vec[0]

# return 0 or 1 if brick can be disintegrated (bricks above will stay).
# Go through each cell of the brick.
# If cell has brick B above then check that B is supported by another brick.
def can_disintegrate(n,b,brick_list, heap):
    p = b.p1.copy()
    # create direction vector for brick
    if b.p1.z != b.p2.z : 
        vec= (0,0,0) # x,y,z
        p = b.p2.copy()  # only need check top cell for z brick
    elif b.p1.x != b.p2.x :
        vec=(1,0,0)
    else: vec=(0,1,0)
    while True:
        # print(f"can_disintegrate:  brick is {b.str()}. Vec is {vec}. Current point is {p.str()}")
        # check cell above p
        brick_above_id = heap.h[p.z+1][p.x][p.y] # has brick above
        if brick_above_id != -1:
            ba = brick_list[brick_above_id]
            ns = num_supporting_bricks(ba, heap)
            if ns == 1: return False
        if p.same_as(b.p2): 
            return True
        p.z += vec[2]
        p.y += vec[1]
        p.x += vec[0]            



def do_part1(brick_list, x_max, y_max, z_max):
    # let bricks settle (fall) into 'heap'
    heap = Heap(z_max+1, x_max+1, y_max+1)
    for n,b in enumerate(brick_list):
        print(f"Drop brick id {n} : {b.str()}")
        # any brick already at z==1 stays there.
        if b.p1.z == 1: 
            heap_add_brick(heap, n, b)
        else:
            # see if it can drop
            p = b.p1.copy()
            # (1) single cube, or just a vertical stack
            if b.p1.x == b.p2.x and b.p1.y == b.p2.y:
                distance = drop_amount(heap, p)
                #print(f"Dropping Z brick  {n} : {b.str()} by distance {distance} to ",end='')
                if distance:
                    b.p1.z = b.p1.z - distance
                    b.p2.z = b.p2.z - distance
                #print(f"{b.str()}")
                heap_add_brick(heap,n,b)
            elif b.p1.x != b.p2.x:  # (2) lies along x
                min_dist = 1000
                for x in range(b.p1.x, b.p2.x+1):
                    p.x = x
                    distance = drop_amount(heap, p)
                    if distance < min_dist: min_dist = distance
                if min_dist < 1000:
                    #print(f"Dropping X brick {n} : {b.str()} by distance {min_dist} to ",end='')
                    b.p1.z = b.p1.z - min_dist
                    b.p2.z = b.p2.z - min_dist
                #print(f"{b.str()}")
                heap_add_brick(heap,n,b)
            else: # (3) lies along y
                min_dist = 1000
                for y in range(b.p1.y, b.p2.y+1):
                    p.y = y
                    distance = drop_amount(heap, p)
                    if distance < min_dist: min_dist = distance
                if min_dist < 1000:
                    #print(f"Dropping Y brick {n} : {b.str()} by distance {min_dist} to ",end='')
                    b.p1.z = b.p1.z - min_dist
                    b.p2.z = b.p2.z - min_dist
                #print(f"{b.str()}")
                heap_add_brick(heap,n,b)

    draw_heap(heap,start=1,end=4)

    # count bricks that can be disintegrated
    c = 0
    for  n,b in enumerate(brick_list):
        if can_disintegrate(n,b,brick_list, heap):
            # print(f"Can disintegrate brick {n}  {b.str()}")
            c += 1

    return c, heap


# draw heap level z
def show_xy(z, xy):
    print(f"Level {z}:   Y")
    for y in range(y_max+1):
        for x in range(x_max+1):
            v= xy[x][y]
            if v <0: print(f"... ",end='')
            else: print("%3d "%v,end='')
        print("" if y < y_max else " -> X")
    print("")
    
def draw_heap(heap, start=0, end=z_max):
    for z, xy in enumerate(heap.h):
        if z >= start and z <=end:
            show_xy(z,xy)

def do_part2(brick_list, heap, x_max, y_max, z_max, max_b):
    c = 0
    for n,b in enumerate(brick_list):
        # if n > 0: continue
        if print_on: print(f"Destroying brick {n} {b.str()} -------------")
        h = copy.deepcopy(heap)
        # destroy brick n from heap
        nc = h.destroy(n, b, x_max, y_max)
        if print_on: print(f"   Destroyed the brick itself ({n}) - had {nc} cells.")
        # Now check all heap locations above this brick to see if there are
        # bricks that can drop, in which case destroy them and repeat.
        z = b.p2.z+1 # level to look at
        done = False
        bc = 0
        last_z = z
        while not done:
            if print_on: print(f"      Checking level {z}")
            cant_destroy = []
            for x in range(x_max+1):
                for y in range(y_max+1):
                    b_id = h.h[z][x][y]
                    if b_id > -1 and b_id not in cant_destroy:
                        if h.brick_can_drop(b_id, brick_list[b_id]):
                            if print_on: print(f"         CAN destroy {b_id} at {x},{y}")
                            nc = h.destroy(b_id, brick_list[b_id], x_max, y_max)
                            bc += 1
                            last_z = z
                        else:
                            cant_destroy.append(b_id)
                            if print_on: print(f"         Cannot destroy {b_id} at {x},{y}")
            z += 1
            if z > last_z+max_b: done = True

        print(f"   Destroying brick {n} results in {bc} other bricks destroyed")
        c += bc
    return c

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
snapshot_list, max_b = get_snapshot_list(db)
NUM_BRICKS=len(snapshot_list)
x_max, y_max, z_max = get_max_xyz(snapshot_list)

# Sort by lowest z
snapshot_list.sort(key=lambda brick: brick.p1.z)
print(f"Saw {NUM_BRICKS} bricks.  Max: x={x_max} y={y_max} z={z_max}")

c, heap = do_part1(snapshot_list, x_max, y_max, z_max)
print(f"Can disintegrate {c} bricks.")

c = do_part2(snapshot_list, heap, x_max, y_max, z_max, max_b)
print(f"Total for part 2 is {c} bricks.")
