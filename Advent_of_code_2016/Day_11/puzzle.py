#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools

input_file_name = 'input.txt'
print_on = False
PR=0
CO=1
CU=2
RU=3
PL=4
EL=5
DI=6
el_names = ['PR','CO','CU','RU','PL','EL','DI']
NUM_ELS = len(el_names)
TOP_FLOOR = 3
FINISHED = 0x1f # part 1
FINISHED = 0x7f # part 2
# FINISHED = 0x3

# move = ( chips_to_move, gens_to_move, from_floor, to_floor )

class Floors():
    def __init__(self):
        self.gens = array.array('I', [0] * 4)
        self.chips = array.array('I', [0] * 4)
        self.el = 0 # elevator
        self.moves = 0 # moves so far
    
    def copy(self):
        f = Floors()
        f.gens = array.array('I', [i for i in self.gens])
        f.chips = array.array('I', [i for i in self.chips])
        f.el = self.el
        f.moves = self.moves
        return f
    
    def hash(self):
        s = str(self.chips) + str(self.gens) + str(self.el)
        return s
    
    def place_gen(self,element,floor):
        if (self.gens[floor] & (1 << element)):
            print(f"Err tried to place gen {element} at floor {floor} but already present: gen is {self.gens}")
            sys.exit(1)
        self.gens[floor] |= (1 << element)

    def remove_gen(self,element,floor):
        if not (self.gens[floor] & (1 << element)):
            print(f"Err tried to remove gen {element} from floor {floor} but not present: gen is {self.gens}")
            sys.exit(1)
        self.gens[floor] ^= (1 << element)
        
    def floor_has_gen(self,element,floor):
        return (self.gens[floor] & (1 << element)) != 0

    def place_chip(self,element,floor):
        if (self.chips[floor] & (1 << element)):
            print(f"Err tried to place chip {element} at floor {floor} but already present: chip is {self.chips}")
            sys.exit(1)
        self.chips[floor] |= (1 << element)

    def remove_chip(self,element,floor):
        if not (self.chips[floor] & (1 << element)):
            print(f"Err tried to remove chip {element} from floor {floor} but not present: chip is {self.chips}")
            sys.exit(1)
        self.chips[floor] ^= (1 << element)
        
    def floor_has_chip(self,element,floor):
        return (self.chips[floor] & (1 << element)) != 0

    def show(self):
        s = ''
        for fl in [3,2,1,0]:
            s += "%1d" % fl
            if self.el == fl: s += ' E '
            else: s += '   '
            for el in range(NUM_ELS):
                if self.floor_has_chip(el,fl): s+= 'C:'+el_names[el] + ' '
                else: s += '     '
                if self.floor_has_gen(el,fl): s+= 'G:' + el_names[el] + ' '
                else: s += '     '
            s += "\n"
        return s

    def get_legal_single_object_moves(self):
        # can always move a single chip
        chips = self.chips[self.el]
        gens = 0
        # can only move a gen if its chip is not there. or there are no other gens
        for o in range(NUM_ELS):
            if self.floor_has_gen(o,self.el):
                if not self.floor_has_chip(o, self.el) or ((self.gens[self.el] ^ (1<<o)) == 0):
                    gens += 1 << o
        if (chips | gens) == 0 : return []
        dests = []
        if self.el < TOP_FLOOR: dests.append(self.el+1)
        if self.el > 0: dests.append(self.el-1)
        moves = []
        for dest_floor in dests:
            for o in range(NUM_ELS):
                bit = 1 << o
                # can only add chip to floor if no generators there or its own generator is there.
                if (chips & bit) and ((self.gens[dest_floor]==0) or (self.gens[dest_floor] & bit)):
                    moves.append((bit,0,self.el,dest_floor))
                # can only add gen to floor if all chips there have their own gens
                if (gens & bit) and (self.chips[dest_floor] & (self.gens[dest_floor] | bit) == self.chips[dest_floor]):
                    moves.append((0, bit, self.el, dest_floor))
        return moves
                
    def get_legal_double_object_moves(self):
        # Try chip + chip
        # can always move a chip.
        chipset = [ o for o in range(NUM_ELS) if self.floor_has_chip(o, self.el)]
        # if we have 2 or more chips then get all combinations of 2
        moves = []
        dests = [] # up to 2 destination floors.
        if self.el < TOP_FLOOR: dests.append(self.el+1)
        if self.el > 0: dests.append(self.el-1)
        for dest_floor in dests:
            if len(chipset) > 1: 
                for chippair in list(itertools.combinations(chipset, 2)):
                    # each chippair has 2 potential chips we can move
                    # Can go to floor if both chips have their gens there, or no gens at all.
                    if (self.gens[dest_floor] == 0) or (self.floor_has_gen(chippair[0],dest_floor) and self.floor_has_gen(chippair[1],dest_floor)):
                        moves.append(((1<<chippair[0]) + (1<<chippair[1]), 0, self.el, dest_floor))
                
        # try chip + gen pair
        for chip in chipset:
            if self.floor_has_gen(chip,self.el):  # this floor has the gen for the chip
                for dest_floor in dests:
                    # can move this chip+gen to the floor if the floor doesn't have any chips without their gens.
                    if (self.chips[dest_floor] & self.gens[dest_floor]) == self.chips[dest_floor]:
                        moves.append((1<<chip, 1<<chip, self.el, dest_floor))

        # try gen + gen
        genset = [ o for o in range(NUM_ELS) if self.floor_has_gen(o, self.el)]
        if len(genset) > 1:
            for genpair in list(itertools.combinations(genset, 2)):
                pairbits = (1<<genpair[0]) + (1<<genpair[1])
                # can move 2 gens out if 
                # 1. These are the only 2 gens here, or
                # 2. the two matching chips are not present.
                if (len(genset)==2) or ((self.chips[self.el] & pairbits) == 0):
                    for dest_floor in dests:
                        # can move 2 gens to a floor iff all chips have their gens.
                        if (self.chips[dest_floor] & (self.gens[dest_floor] | pairbits)) == self.chips[dest_floor]:
                            moves.append((0, pairbits, self.el, dest_floor ))

        return moves

    # return list of possible moves
    def get_legal_next_moves(self):
        if (self.gens[self.el] | self.chips[self.el]) == 0: # nothing to do
            return []
        
        single_object_moves = self.get_legal_single_object_moves()
        if len(single_object_moves) and print_on:
            print(f"{len(single_object_moves)} new single moves are:")
            for m in single_object_moves: print_move(m)
        double_object_moves = self.get_legal_double_object_moves()
        if len(double_object_moves) and print_on:
            print(f"{len(double_object_moves)} new double moves are:")
            for m in double_object_moves: print_move(m)
        single_object_moves.extend(double_object_moves)
        return single_object_moves

    def apply_move(self, move):
        if print_on:
            print("--- Apply ", end='')
            print_move(move)
            print(f"{self.show()}")

        chips = move[0]
        gens = move[1]
        from_floor = move[2]
        to_floor = move[3]
        if chips | gens == 0:
            print("Error: move has no chips or gens")
            sys.exit(1)
        for o in range(NUM_ELS):
            if chips & (1<<o): 
                self.remove_chip(o,from_floor)
                self.place_chip(o,to_floor)
            if gens & (1<<o): 
                self.remove_gen(o,from_floor)
                self.place_gen(o,to_floor)
        self.el = to_floor
        self.moves += 1

    def finished(self):
        return (self.gens[3] == FINISHED) and (self.chips[3] == FINISHED)
    
    def is_same_as(self, other):
        for fl in range(4):
            if self.gens[fl] != other.gens[fl]: return False
            if self.chips[fl] != other.chips[fl]: return False
        if self.el != other.el: return False
        return True

    def already_seen(self, seenlist):
        h = self.hash()
        if not h in seenlist: return False
        other = seenlist[h]
        if self.moves < other.moves: return False
        return True

    
    def check_status(self):
        # a chip cannot be on its own if there are other gens
        for fl in range(3):
            for o in range(NUM_ELS):
                if self.floor_has_chip(o,fl):
                    if not self.floor_has_gen(o,fl) and self.gens[fl]:
                        print(f"ERROR: Bad configuration for floor {fl}.")
                        print(f"{self.show()}")
                        sys.exit()


def print_move(m):
    s = "MOVE:"
    for o in range(NUM_ELS): 
        if m[0] & 1<<o : s += " C_" + el_names[o]
        if m[1] & 1<<o : s += " G_" + el_names[o]
    print(f"{s} from {m[2]} -> {m[3]}")

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def remove_move(moves, orig_move):
    newmoves = []
    for m in moves:
        if (m[0] == orig_move[0]) and (m[1] == orig_move[1]):
            if (m[2] == orig_move[3]) and (m[3] == orig_move[2]):
                # print("Removed inverse")
                continue
        newmoves.append(m)
    return newmoves

def add_seen(seen,f):
    h = f.hash()
    seen[h] = f.copy()
    # print(f"Added:\n{f.show()}")

def setup():
    f = Floors()
    f.place_gen(PR,0)
    f.place_chip(PR,0)
    for el in [CO, CU,RU,PL]:
        f.place_gen(el,1)
        f.place_chip(el,2)

    f1 = Floors()
    f1.chips[0] = 0x3
    f1.gens[1] = 0x1
    f1.gens[2] = 0x2
    f1.el = 0

    return f

def setup2():
    f = Floors()
    for el in [PR,EL,DI]:
        f.place_gen(el,0)
        f.place_chip(el,0)

    for el in [CO, CU,RU,PL]:
        f.place_gen(el,1)
        f.place_chip(el,2)


    return f
def do_part1(db):
    o = 0
    f = setup()
    print(f"{f.show()}")
    seen = {f.hash(): f.copy()}
    moves = f.get_legal_next_moves()
    paths = []
    fewest = 1000
    if len(moves): 
        paths.append((f, moves.pop()))
        for m in moves:
            paths.append((f.copy(), m))

    step = 0
    while len(paths):
        print(f"{step} ---- There are now {len(paths)} paths ----")
        step += 1
        new_paths = []
        fewest_this_loop = 1000
        for (f,m) in paths:
            f.apply_move(m)
            if f.moves < fewest_this_loop: fewest_this_loop = f.moves
            f.check_status() # check things still legal
            if f.finished():
                print(f"Finished in {f.moves}")
                if f.moves < fewest: fewest = f.moves
                continue
            if f.already_seen(seen): 
                # print("New floor has already been seen - discarding it")
                continue
            add_seen(seen, f)
            if print_on: print(f"After move, floors are:\n{f.show()}")
            newmoves = f.get_legal_next_moves()
            moves = remove_move(newmoves, m)  # dont just undo the move we made
            if len(moves): 
                if print_on: 
                    print(f"After move, there are {len(moves)} new moves:")
                    for mm in moves: print_move(mm)
                new_paths.append((f, moves.pop()))
                for mm in moves:
                    new_paths.append((f.copy(), mm))    
            else:
                if print_on: print("No possible new moves.")

        if fewest_this_loop > fewest:
            return fewest
        paths = new_paths
    return fewest

def do_part2(db):
    f = setup2()
    print(f"{f.show()}")
    seen = {f.hash(): f.copy()}
    moves = f.get_legal_next_moves()
    paths = []
    fewest = 1000
    if len(moves): 
        paths.append((f, moves.pop()))
        for m in moves:
            paths.append((f.copy(), m))

    step = 0
    while len(paths):
        print(f"{step} ---- There are now {len(paths)} paths ----")
        step += 1
        new_paths = []
        fewest_this_loop = 1000
        for (f,m) in paths:
            f.apply_move(m)
            if f.moves < fewest_this_loop: fewest_this_loop = f.moves
            f.check_status() # check things still legal
            if f.finished():
                print(f"Finished in {f.moves}")
                if f.moves < fewest: fewest = f.moves
                continue
            if f.already_seen(seen): 
                # print("New floor has already been seen - discarding it")
                continue
            add_seen(seen, f)
            if print_on: print(f"After move, floors are:\n{f.show()}")
            newmoves = f.get_legal_next_moves()
            moves = remove_move(newmoves, m)  # dont just undo the move we made
            if len(moves): 
                if print_on: 
                    print(f"After move, there are {len(moves)} new moves:")
                    for mm in moves: print_move(mm)
                new_paths.append((f, moves.pop()))
                for mm in moves:
                    new_paths.append((f.copy(), mm))    
            else:
                if print_on: print("No possible new moves.")

        if fewest_this_loop > fewest:
            return fewest
        paths = new_paths
    return fewest



#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")



