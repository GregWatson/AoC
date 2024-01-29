#import argparse
import sys
import re
import functools
import array
import copy


# get total size of a RL
def RL_size(rl):
    sz = 0
    for r in rl:
        if (r[0]==0) : pass
        else: sz = sz + r[1] - r[0] + 1
    return sz

def remove_range(RL, lo,hi):
    print(f"          remove range ({lo},{hi}) for current range {RL[0]}")
    r = RL[0]
    rlo = r[0]
    rhi = r[1]
    if rlo == 0: return
    if lo !=1 and hi !=4000:
        print(f"Bad range delete {lo}-{hi}")
        sys.exit(1)
    if lo <= rlo and hi >= rhi: 
        RL[0] = (0,0)  # delete entire range
        return
    if lo == 1: # delete 1-hi
        if rlo > hi: return
        if rhi <= hi : 
            RL[0] = (0,0)  # delete entire range
            return
        RL[0] = (hi+1,rhi)
        return

    if hi==4000: # delete lo-4000
        if rhi < lo: return
        if rlo >= lo: 
            RL[0] = (0,0)  # delete entire range
            return
        RL[0] = (rlo, lo-1)
    return

class Part:
    def __init__(self,x,m,a,s):
        self.x=x
        self.m=m
        self.a=a
        self.s=s

    def print(self):
        print(f"X:{self.x} M:{self.m} A:{self.a} S:{self.s}")

    def get_val(self, letter):
        return self.x if letter  == 'x' else self.m if letter == 'm' else self.a if letter == 'a' else self.s
    
    def rating_sum(self):
        return self.x + self.m + self.a +self.s
    

class XMAS:
    def __init__(self):
        self.x = [ (1,4000) ] # list of valid ranges (aka RangeList or RL)
        self.m = [ (1,4000) ] # list of valid ranges
        self.a = [ (1,4000) ] # list of valid ranges
        self.s = [ (1,4000) ] # list of valid ranges

    def sizeof(self):
        return RL_size(self.x) * RL_size(self.m) * RL_size(self.a) * RL_size(self.s)

    def get_RL(self, letter):
        if letter == 'x': return self.x
        if letter == 'm': return self.m
        if letter == 'a': return self.a
        if letter == 's': return self.s
        sys.exit(1)

    def str(self):
        return f"X:{self.x[0]} M:{self.m[0]} A:{self.a[0]} S:{self.s[0]} "
    
def load_rules():
    rules = {}
    with open("rules.txt") as f:
        lines = f.readlines()
    rules_txt = [ l.strip() for l in lines ]
    for r in rules_txt:
        m = re.match(r'([a-z0-9]+)\{([^}]+)\}', r)
        if m:
            rule_ID = m.group(1)
            if len(rule_ID) <2 or len(rule_ID) > 3:
                print(f"SAW rule ID {rule_ID}")
            seqL = m.group(2).split(',')
            print(f"{rule_ID} -> {seqL}")
            rules[rule_ID] = seqL
        else:
            print(f"No rule match on {r}")
    return rules

def load_parts():
    parts = []
    with open("parts.txt") as f:
        lines = f.readlines()
    parts_txt = [ l.strip() for l in lines ]
    for pl in parts_txt:
        m = re.match(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', pl)
        if m:
            p = Part(int(m.group(1)),int(m.group(2)), int(m.group(3)), int(m.group(4)) )
            # p.print()
            parts.append(p)
    return parts



def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def process_rule(rule,p):
    # returns A, R, rule_id or 'c'. 'c' means comparison failed - try next rule
    colon_pos = rule.find(':')
    target_rule = rule[colon_pos+1:]
    letter = rule[0] # one of xmas
    value = p.get_val(letter)
    relop = rule[1]
    comparand = int(rule[2:colon_pos])
    # print(f"       Rule {rule} is IF {letter}(value {value}) {relop} {comparand} THEN {target_rule}")
    if relop == '<':
        if value < comparand:
            return target_rule
        return 'c'
    if value > comparand:
        return target_rule
    return 'c'



def process_part(p, rules):
    rule_id = 'in'
    print(f"Process part ",end='')
    p.print()
    while rule_id:
        print(f"   rule_id {rule_id}")
        rule_seq = rules[rule_id]
        for rule in rule_seq:
            if len(rule) < 4: # unconditional rule
                if rule == 'A': return True
                if rule == 'R': return False
                rule_id = rule
                break
            else: # conditional rule
                next = process_rule(rule, p)
                if next == 'c': continue
                if next == 'A' : return True
                if next == 'R' : return False
                rule_id = next
                break


def p2_rule(xmas, rule, rules):
    print(f"      p2_rule called on: XMAS={xmas.str()} rule:{rule}")
    # return count of accepts when rule passes, as well as new xmas that is modified for when rule fails.
    xmas_fail = copy.deepcopy(xmas)
    colon_pos = rule.find(':')
    target_rule = rule[colon_pos+1:] # e.g. A, R or rule_ID such as pq
    letter = rule[0] # one of 'xmas'
    relop = rule[1]
    comparand = int(rule[2:colon_pos])
    # print(f"       Rule {rule} is IF {letter}(value {value}) {relop} {comparand} THEN {target_rule}")
    RL = xmas.get_RL(letter)
    fRL = xmas_fail.get_RL(letter)
    if relop == '<':
        remove_range(RL, comparand, 4000) # true
        remove_range(fRL,1,comparand-1)
    else: # relop is >
        remove_range(RL,1,comparand) # true
        remove_range(fRL,comparand+1, 4000)
    print(f"      p2_rule. After RL deletion, xmas is {xmas.str()}   xmas_fail is {xmas_fail.str()}")

    if target_rule =='A':
        print(f"Compute accept on {xmas.str()} which has size {xmas.sizeof()}")
        return (xmas.sizeof() , xmas_fail )
    if target_rule =='R':
        return (0 , xmas_fail )
    return (p2_proc_rule(xmas, target_rule, rules), xmas_fail)


def p2_proc_rule(xmas, rule_id, rules):
    c = 0
    while rule_id:
        print(f"   p2_proc_rule: c={c}  XMAS={xmas.str()} rule_id:{rule_id}")
        rule_seq = rules[rule_id]
        for rule in rule_seq:
            print(f"     p2_proc_rule: rule is {rule},  current count is {c}")
            if len(rule) < 4: # unconditional rule
                if rule == 'A': return c + xmas.sizeof()
                if rule == 'R': return c
                rule_id = rule
            else: # conditional rule. Must process both paths
                count, new_xmas = p2_rule(xmas, rule, rules)
                c = c + count
                xmas = new_xmas
    return c

def do_part2(rules):
    xmas = XMAS()
    rule_id = 'in'
    c = p2_proc_rule(xmas, rule_id, rules)
    return c


#---------------------------------------------------------------------------------------
# Load input
rules = load_rules()
parts = load_parts()
print(f"Saw {len(rules)} rules and {len(parts)} parts ")

for r in rules:
    print(f"{r} => {rules[r]}")
# c = 0
# for p in parts:
#     res = process_part(p, rules)
#     if res:
#         c = c + p.rating_sum()
#
# print(f"Total is {c}")

c2 = do_part2(rules)

print(f"Part 2 Total space is {c2}")
