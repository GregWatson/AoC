import sys
import re
import functools
import array
import copy

def load_db():
    with open('input.txt') as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def count_letters(l):
    acount = {}
    for w in l:
        for c in w:
            if c in acount: acount[c] += 1
            else:  acount[c] = 1
    letters = [ (k, acount[k]) for k in acount.keys()]
    letters.sort(key=lambda x: x[1], reverse=True)
    nums = [ acount[k] for k in acount.keys()]
    nums.sort(reverse=True)
    uniq_nums = list(set(nums))
    uniq_nums.sort(reverse=True)
    #print(f"{letters}    {nums}    {uniq_nums}")
    seq = ''
    for n in uniq_nums:
        chars = [k for k in acount.keys() if acount[k]==n]
        chars.sort()
        #print(f"{n} -> {chars}")
        seq += ''.join(chars)
    return seq[0:5]

def rotate_by(words, sectorID):
    s = ' '.join(words)
    news = ''
    for c in s:
        if c.isalpha():
            c = chr( ( (ord(c)-ord('a')+sectorID)%26 + ord('a')) )
        news += c
    if news.startswith('north'): print(f"{sectorID} {news}")
    return news


def do_part1(db):
    tot = 0
    for l in db:
        words = l.split('-')
        lastword = words.pop()
        m = re.match(r'(\d+)\[([a-z]+)\]',lastword)
        if m:
            sectorID, checksum = int(m.group(1)), m.group(2)
            seq = count_letters(words)
            print(f"{seq}")
            if seq == checksum: tot += sectorID
        else: 
            print("NO MATCH")
            sys.exit(1)

    return tot

def do_part2(db):
    tot = 0
    for l in db:
        words = l.split('-')
        lastword = words.pop()
        m = re.match(r'(\d+)\[([a-z]+)\]',lastword)
        if m:
            sectorID, checksum = int(m.group(1)), m.group(2)
            seq = count_letters(words)
            if seq != checksum: continue
        s = rotate_by(words, sectorID)
    sys.exit(1)

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"saw {len(db)} lines")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Part 2 is {p2}.")

