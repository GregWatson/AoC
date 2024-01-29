#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False
ev = []
count = [0,0] 
run_count = 0
flops = [ ['sf', 'bq', 'jx', 'zz', 'pf', 'xk', 'mg', 'dp', 'mh', 'tj'], # list of flop_ids
          [ 'pt', 'qn', 'kg', 'hr', 'ls', 'vq', 'bh', 'gb', 'vv']
        ]

def add_event( e ): # from_id, pulse, to_id
    global ev
    global count
    global run_count
    if e[2] != 'rx' : 
        ev.append( e )
    else:
        #print("Skipped rx")
        if e[1] == 0:
            print("Saw low pulse. Count is {run_count}")
            sys.exit(1)
    count[e[1]] += 1

    if e[1] == 0:
        if e[0] in [ 'qr', 'bf', 'gm', 'cx']:
            print (f"zero on {e[0]} count is {run_count}")
            

class Gate:
    global flops
    def __init__(self,id,type,output_ids):
        self.id = id
        self.type = type
        self.output_ids = output_ids
        if type == '%': # flop
            self.state = 0 # off
            # flops.append(self.id)
        elif type == '&':
            self.state = {} # hash of input gate ID to this gate. maps gate ID to last pulse type.
        else: self.state = None

    def print(self):
        print(f"{self.type} {self.id} -> {self.output_ids} state:{self.state}")

    def process_pulse(self,from_id, p):
        if print_on: print(f"{self.id} gets pulse {p} from {from_id}   current state is {self.state}")
        if self.type == '%':
            if p == 0:
                self.state = 1 - self.state
                for id in self.output_ids:
                    add_event( (self.id, self.state, id) )
            return
        elif self.type == '&':
            self.state[from_id] = p
            all_inputs = [self.state[id] for id in self.state]
            output = 0 if sum(all_inputs) == len(all_inputs) else 1
            for id in self.output_ids:
                add_event( (self.id, output, id) )
            return
        elif self.type == 'broadcaster':
            for id in self.output_ids:
                add_event( (self.id, p, id) )
        else: 
            print(f"unknown type")
            sys.exit(1)

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_output_ids(s):
    # get list of gates.
    return s.split(', ')

def get_circuit(db):
    circuit = {}
    for l in db:
        m = re.match(r'broadcaster -> (.*)', l)
        if m:
            gate = Gate('broadcaster','broadcaster', m.group(1).split(', ') ) 
            circuit['broadcaster'] = gate
        else:
            m = re.match(r'(&|%)([a-z]+) -> (.*)', l)
            if m:
                gate = Gate(m.group(2), m.group(1), m.group(3).split(', ') ) 
                circuit[m.group(2)] = gate

    # terminate element?
    circuit['rx'] = Gate('rx','rx',[])

    # now map inputs to & gates
    for id in circuit:
        g = circuit[id]
        for dst_id in g.output_ids:
            dst = circuit[dst_id]
            if dst.type == '&':
                dst.state[id]=0  # all NAND inputs start as zero

    return circuit

def run_circuit(circuit):
    global ev
    # send low pulse to bcaster
    add_event( ('', 0, 'broadcaster') ) # from_id, pulse, to_id
    while ev:
        event = ev.pop(0)
        if print_on: print(f"{event}  {ev}")
        circuit[event[2]].process_pulse(event[0], event[1])

    return

def show_flops(cicuit):
    global flops
    for fl in flops:
        for f_id in fl:
            print(f" {f_id}",end='')
        print (" : ", end='')
    print("")
    for fl in flops:
        for f_id in fl:
            print(f"  {circuit[f_id].state}",end='')
        print (" : ", end='')
    print("")


#---------------------------------------------------------------------------------------
# Load input
db = load_db()
circuit = get_circuit(db)
for id in circuit:
    g = circuit[id]
    # print(f"{g.type}{g.id}->{g.output_ids}  st:{g.state}")

for i in range(1000):
    if i % 10000 == 0 : 
        print (f"{i+1}")
    run_count = i+1
    run_circuit(circuit)
    #show_flops(circuit)


    #for id in circuit:
    #    g = circuit[id]
    #    g.print()

lo, hi = count
print(f"hi {hi}  lo {lo}  (sum {hi+lo})  total {hi * lo}")

# This function computes GCD 
def compute_gcd(x, y):

   while(y):
       x, y = y, x % y
   return x

# This function computes LCM
def compute_lcm(x, y):
   lcm = (x*y)//compute_gcd(x,y)
   return lcm

a = compute_lcm(3760, 3767)
b = compute_lcm(4001, 4091)
c = compute_lcm(a,b)
print(f"lcm is {c}")
