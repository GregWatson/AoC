#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = False
SEQ = 'ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaCaSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTiBPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMgArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPBPBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFArCaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRnFArTiRnPMgArF'

#SEQ = 'O1PBPG3EEEJKEEJKEEPBJ1F31F3EEJKEEJKEEEEEEJ1F2F3J1G3EJ1PM'  + \
#      'MBF2PBF3J1EJ1M1F3JD3PMBPM1EJD3EPMMBPG2F3PM1F3J1EEF31EF3EJ1J1' + \
#      'G3F2EJ1G3EEJKP1F3PBEJ1G3EEJKEJ1MG3F3JKJKEEJ1G3EEJ1F3MBPM'+ \
#      '1EJD3EPM1F3PBPBEEJKEPBJKP1F3JKEJKEJKEPMBJ1F2F3EEP1F3PBEEPBJ1M' + \
#      '1F3EP1F3J1EEEJKE1EF32EJ1F3BEEEJKF3PBF3EJ1F31EEEF3J1F3M1PG3F'




def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def load_init_config(db):
    map = {}
    for l in db:
        m = re.match(r'(\w+) => (\w+)',l)
        if m:
            src,dst = m.group(1), m.group(2)
            if src in map:
                map[src].append(dst)
            else : 
                map[src] = [dst]
            if src in ['Al','D'] : print(f"{src} -> {map[src]}")
    return map

def load_rev_map(db):
    revmap = []
    for l in db:
        m = re.match(r'(\w+) => (\w+)',l)
        if m:
            src,dst = m.group(1), m.group(2)
            revmap.append((dst,src))
    return revmap

def get_configs(map,s):
    newkeys = {}
    kys = map.keys()
    tot = 0
    for k in kys:
        l = len(k)
        for i in range(len(s)-l+1):
            if s[i:i+l] == k:
                if k in ['Al','D'] : print(f"Found {k} at {i}")
                for ins in map[k]:
                    st = s[0:i] + ins + s[i+l:]
                    newkeys[st] = 1
    return len(newkeys.keys())

def do_part1(db):
    tot= 0
    map = load_init_config(db)
    tot = get_configs(map, SEQ)
    
    return tot

# get new candidate strings
def get_new_s(cur, revmap, terms):
    k = list(revmap.keys())
    c = 0
    k.sort(key=len, reverse=True)
    done = False
    while not done:
        done = True
        for key in terms:
            while key in cur:
                cur = cur.replace(key, revmap[key], 1)
                c += 1
                done = False
        print(f"{c} {cur}")
        for key in k:
            if key in terms: continue
            while key in cur:
                cur = cur.replace(key, revmap[key], 1)
                c += 1
                done = False
        print(f"{c} {cur}")
    return c

def do_part2(db):
    tot=0
    revmap = load_rev_map(db)
    mol=SEQ
    done = False
    while (mol != 'e') and not done:
        done = True
        for output, input in revmap:
            if output in mol:
                mol = mol.replace( output, input,1)
                tot += 1
                done = False
    print (f"{mol}")
    return tot




#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

#p1 = do_part1(db)
#print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 2 is 207.")



