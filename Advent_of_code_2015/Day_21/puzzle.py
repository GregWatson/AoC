#import argparse
import sys
import re
import functools
import array
import copy
# import math

input_file_name = 'input.txt'
print_on = False

Weapons = { 'Dagger':     {'Cost':8, 'Damage':4, 'Armor':0 },
            'Shortsword': {'Cost':10, 'Damage':5, 'Armor':0 },
            'Warhammer':  {'Cost':25, 'Damage':6, 'Armor':0 },
            'Longsword':  {'Cost':40, 'Damage':7, 'Armor':0 },
            'Greataxe':   {'Cost':74, 'Damage':8, 'Armor':0 }
          }

Armor = { 'Leather':     {'Cost':13, 'Damage':0, 'Armor':1 },
          'Chainmail':   {'Cost':31, 'Damage':0, 'Armor':2 },
          'Splintmail':  {'Cost':53, 'Damage':0, 'Armor':3 },
          'Bandedmail':  {'Cost':75, 'Damage':0, 'Armor':4 },
          'Platemail':   {'Cost':102,'Damage':0, 'Armor':5 },
          'None':   {'Cost':0,'Damage':0, 'Armor':0 }
        }

Rings = { 'Damage_P1':     {'Cost':25, 'Damage':1, 'Armor':0 },
          'Damage_P2':     {'Cost':50, 'Damage':2, 'Armor':0 },
          'Damage_P3':     {'Cost':100, 'Damage':3, 'Armor':0 },
          'Defence_P1':    {'Cost':20, 'Damage':0, 'Armor':1 },
          'Defence_P2':    {'Cost':40, 'Damage':0, 'Armor':2 },
          'Defence_P3':    {'Cost':80, 'Damage':0, 'Armor':3 },
          'None_1':        {'Cost':0,  'Damage':0, 'Armor':0 },
          'None_2':        {'Cost':0,  'Damage':0, 'Armor':0 }
        }

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def get_cost(cfg):
    c = 0
    for k in cfg.keys(): c += cfg[k]['Cost']
    return c

def do_battle(cfg, boss):
    my_hp = 100
    my_damage = 0
    for k in cfg.keys(): my_damage += cfg[k]['Damage']
    my_damage -= boss['Armor']
    if my_damage < 1: my_damage = 1
    my_armor = 0
    for k in cfg.keys(): my_armor += cfg[k]['Armor']
    boss_damage = boss['Damage'] - my_armor
    if boss_damage < 1: boss_damage = 1
    boss_hp = boss['hp']
    while True:
        boss_hp -= my_damage
        if boss_hp < 1: return True
        my_hp -= boss_damage
        if my_hp < 1: return False

        

def do_part1(boss):
    battle_count = 0
    my_config = {}
    lowest_cost = 1000
    for wep in Weapons.keys():
        my_config['weapon'] = Weapons[wep]
        for arm in Armor.keys():
            my_config['armor'] = Armor[arm]
            for r1 in Rings.keys():
                my_config['r1'] = Rings[r1]
                for r2 in Rings.keys():
                    if r2 == r1: continue
                    my_config['r2'] = Rings[r2]

                    battle_count += 1
                    i_win = do_battle(my_config, boss)
                    if i_win:
                        cost  = get_cost(my_config)
                        if cost < lowest_cost: lowest_cost = cost
        
    return lowest_cost

def do_part2(boss):
    battle_count = 0
    my_config = {}
    high_cost = 0
    for wep in Weapons.keys():
        my_config['weapon'] = Weapons[wep]
        for arm in Armor.keys():
            my_config['armor'] = Armor[arm]
            for r1 in Rings.keys():
                my_config['r1'] = Rings[r1]
                for r2 in Rings.keys():
                    if r2 == r1: continue
                    my_config['r2'] = Rings[r2]

                    battle_count += 1
                    i_lose = not do_battle(my_config, boss)
                    if i_lose:
                        cost  = get_cost(my_config)
                        if cost > high_cost: high_cost = cost
        
    return high_cost


#---------------------------------------------------------------------------------------
# Load input
#db = load_db()
#print(f"Loaded {len(db)} lines from input")
boss = { 'hp': 100, 'Damage': 8, 'Armor': 2 }

#p1 = do_part1(boss)
#print(f"Part 1 is {p1}")

p2 = do_part2(boss)
print(f"Total for part 2 is {p2}.")



