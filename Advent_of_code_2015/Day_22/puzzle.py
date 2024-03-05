#import argparse
import sys
import re
import functools
import array
import copy
# import math

input_file_name = 'input.txt'
print_on = False
min_mana_spent = 100000
min_mana_cost  = 1000
strs = []

HP = 0
MANA = 1
ARMOR = 2
ARMOR_TURNS_LEFT = 3
SHIELD_TURNS_LEFT = 4
POISON_TURNS_LEFT = 5
RECHARGE_TURNS_LEFT = 6
MM_TURNS_LEFT = 7
DRAIN_TURNS_LEFT = 8
MANA_SPENT = 9
BOSS_HP = 10
STR_ID = 11
STATUS_LEN = STR_ID+1

Items = { 'MagicMissile': {'Cost':53, 'Damage':4, 'Health':0, 'Armor':0, 'Mana':0,  'Turns':0, 'TurnsLeft': MM_TURNS_LEFT},
          'Drain':        {'Cost':73, 'Damage':2, 'Health':2, 'Armor':0, 'Mana':0,  'Turns':0, 'TurnsLeft': DRAIN_TURNS_LEFT},
          'Shield':       {'Cost':113,'Damage':0, 'Health':0, 'Armor':7, 'Mana':0,  'Turns':6, 'TurnsLeft': SHIELD_TURNS_LEFT},
          'Poison':       {'Cost':173,'Damage':3, 'Health':0, 'Armor':0, 'Mana':0,  'Turns':6, 'TurnsLeft': POISON_TURNS_LEFT},
          'Recharge':     {'Cost':229,'Damage':0, 'Health':0, 'Armor':0, 'Mana':101,'Turns':5, 'TurnsLeft': RECHARGE_TURNS_LEFT}
          }

def copy_s(s):
    news = array.array('i', s)
    strs.append(strs[s[STR_ID]])
    news[STR_ID] = len(strs)-1
    return news

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

# return a list of possible new status based on legal player options
def get_player_options(s):
    global min_mana_cost
    global min_mana_spent
    if s[MANA] < min_mana_cost: return []
    new_l = []
    for k in Items:
        if Items[k]['Cost'] > s[MANA]: continue
        if s[Items[k]['TurnsLeft']] > 0: continue # still active
        news = copy_s(s)
        # if (k == 'Poison'): strs[news[STR_ID]] += f"<Poison has {news[Items[k]['TurnsLeft']]} turns left>\n" 
        news[Items[k]['TurnsLeft']] = Items[k]['Turns']
        news[MANA] -= Items[k]['Cost']
        news[MANA_SPENT] += Items[k]['Cost']
        strs[news[STR_ID]] += f"Player casts {k}: Uses {Items[k]['Cost']} - Tot Mana spent={news[MANA_SPENT]}. "
        if Items[k]['Turns'] == 0: # immediate
            if Items[k]['Health']:
                news[HP] += Items[k]['Health']
                strs[news[STR_ID]] += f"{k}: Added {Items[k]['Health']} - health is {news[HP]}\n"
            if Items[k]['Damage']:
                news[BOSS_HP] -= Items[k]['Damage']
                strs[news[STR_ID]] += f"{k}: Hit Boss for {Items[k]['Damage']} damage. Boss has {news[BOSS_HP]} hp.\n"
            if news[BOSS_HP] < 1:
                if news[MANA_SPENT] < min_mana_spent: 
                    min_mana_spent = news[MANA_SPENT]
                    strs[news[STR_ID]] += f"Boss killed! Mana used was {news[MANA_SPENT]}\n"
                    print(f"{strs[news[STR_ID]]}")
                continue
        else:
            strs[news[STR_ID]] += f"Active for {news[Items[k]['TurnsLeft']]} turns.\n"
        new_l.append(news)
    return new_l

def apply_updates(sl):
    global min_mana_spent
    new_l = []
    for s in sl:
        if s[MANA_SPENT] > min_mana_spent: continue # no point going further
        s[ARMOR] = 0
        for k in Items:
            if s[Items[k]['TurnsLeft']] > 0: # Effect happens
                strs[s[STR_ID]] += f"{k} has {s[Items[k]['TurnsLeft']]} Turns left. "
                s[Items[k]['TurnsLeft']] -= 1
                if Items[k]['Damage']:
                    s[BOSS_HP] -= Items[k]['Damage']
                    strs[s[STR_ID]] += f"Does {Items[k]['Damage']} damage to boss."
                if Items[k]['Health']:
                    s[HP] += Items[k]['Health']
                    strs[s[STR_ID]] += f"Adds  Does {Items[k]['Health']} health (now {s[HP]})."
                if Items[k]['Armor'] : 
                    s[ARMOR] = Items[k]['Armor']
                    strs[s[STR_ID]] += f"Armor is now {s[ARMOR]}. "
                if Items[k]['Mana']:
                    s[MANA] += Items[k]['Mana']
                    strs[s[STR_ID]] += f"Mana is now {s[MANA]}."
        strs[s[STR_ID]] += "\n"
        if s[BOSS_HP] < 1: # killed boss
            strs[s[STR_ID]] += f"Boss killed! Mana used was {s[MANA_SPENT]}\n"
            if s[MANA_SPENT] < min_mana_spent: 
                min_mana_spent = s[MANA_SPENT]
                print(f"{strs[s[STR_ID]]}")
            continue
        new_l.append(s)
    return new_l

def do_boss_hits(boss, sl):
    new_l = []
    for s in sl:
        damage = boss['Damage'] - s[ARMOR]
        if damage < 1: damage  = 1
        s[HP] -= damage
        if s[HP] > 0: 
            strs[s[STR_ID]] += f"Boss damage is {boss['Damage']}. Armor is {s[ARMOR]}. So Boss hits for {damage}. Player now has {s[HP]} HP.\n"
            s[ARMOR] = 0
            new_l.append(s)
    return new_l

def get_status_string(s):
    s = f"Player has {s[HP]} HP, {s[ARMOR]} Armor, {s[MANA]} mana. Boss has {s[BOSS_HP]} HP.\n"
    return s

def do_part1(boss):
    global min_mana_spent
    global strs
    status = array.array('i', [50, 500, 0, 0, 0, 0, 0, 0, 0, 0, 51,0])
    #status = array.array('i', [10, 250, 0, 0, 0, 0, 0, 0, 0, 0, 14,0])
    strs = [ get_status_string(status) ]
    all_status = [ status ]
    while len(all_status) > 0:
        new_all_status = []
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        for s in all_status:
            # print(f"{s[STR_ID]} : {strs[s[STR_ID]]}")
            # Player turn
            strs[s[STR_ID]] += f"-- Player Turn --\n{get_status_string(status)}"
            pup = apply_updates([s])
            if len(pup):
                pl = get_player_options(pup[0]) 
                for ss in pl: strs[ss[STR_ID]] += "-- Boss Turn --\n"
                ubl = apply_updates(pl)
                bl = do_boss_hits(boss, ubl)
                new_all_status.extend(bl)
        all_status = new_all_status
        print(f"After round there are {len(all_status)} paths active. Min mana is {min_mana_spent}")
    return min_mana_spent

def do_part2(boss):
    global min_mana_spent
    global strs
    min_mana_spent = 10000
    status = array.array('i', [50, 500, 0, 0, 0, 0, 0, 0, 0, 0, 51,0])
    #status = array.array('i', [10, 250, 0, 0, 0, 0, 0, 0, 0, 0, 14,0])
    strs = [ get_status_string(status) ]
    all_status = [ status ]
    while len(all_status) > 0:
        new_all_status = []
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        for s in all_status:
            # print(f"{s[STR_ID]} : {strs[s[STR_ID]]}")
            # Player turn
            s[HP] -= 1
            if s[HP] < 1: continue
            strs[s[STR_ID]] += f"\n-- Player Turn (Player loses 1 HP) --\n{get_status_string(s)}"
            pup = apply_updates([s])
            if len(pup):
                pl = get_player_options(pup[0]) 
                for ss in pl: strs[ss[STR_ID]] += f"\n-- Boss Turn --\n{get_status_string(ss)}"
                ubl = apply_updates(pl)
                bl = do_boss_hits(boss, ubl)
                new_all_status.extend(bl)
        all_status = new_all_status
        print(f"After round there are {len(all_status)} paths active. Min mana is {min_mana_spent}")
    return min_mana_spent

#---------------------------------------------------------------------------------------
# Load input
#db = load_db()
#print(f"Loaded {len(db)} lines from input")
boss = { 'hp': 51, 'Damage': 9 }
#boss = { 'hp': 14, 'Damage': 8 }
for k in Items: 
    if Items[k]['Cost'] < min_mana_cost: min_mana_cost = Items[k]['Cost']

#p1 = do_part1(boss)
#print(f"Part 1 is {p1}")

p2 = do_part2(boss)
print(f"Total for part 2 is {p2}.")



