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
NUMX=38
NUMY=24
MINSIZE=85
MAXSIZE=94
BIGNUM = 99999999

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getStops(db):
    mstops = {}
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            if c in '01234567':
                mstops[c] = (x,y)
    stops = []
    for i in range(len(mstops)): 
        stops.append(mstops[str(i)])
        print(f"Stop {i} found at {stops[-1]}")
    return stops

def blockOff(maze):
    # Block off all dead ends that are not junctions
    # a dead end is a point that has only one path
    # a path is a '.' or a number
    newMaze = [ l[:] for l in maze ]
    changed = True
    while changed:
        changed = False
        # block off all dead ends
        for y in range(1,len(newMaze)-1):
            for x in range(1,len(newMaze[y])-1):
                if newMaze[y][x] == '.':
                    c = 0
                    for d in [(0,1),(1,0),(0,-1),(-1,0)]:
                        if newMaze[y+d[1]][x+d[0]] != '#': 
                            c += 1
                        if c > 1:
                            break
                    if c == 1:
                        newMaze[y][x] = '#'
                        changed = True
    return newMaze

def isJunction(maze, x, y):
    # check if the point is a junction
    # a junction is a point that has 3 or more paths
    # a path is a '.' or a number
    c = 0
    for d in [(0,1),(1,0),(0,-1),(-1,0)]:
        if maze[y+d[1]][x+d[0]] != '#': 
            c += 1
        if c > 2:
            return True
    return False

def getJunctions(maze):
    # get a list of all junctions in the maze
    # a junction is a point that has 3 or more paths
    # a path is a '.' or a number
    junctions = []
    for y in range(1,len(maze)-1):
        for x in range(1,len(maze[y])-1):
            if maze[y][x] != '#' and (isJunction(maze, x, y) or maze[y][x] in '01234567'):
                junctions.append((x,y))
                if maze[y][x] in '01234567': print(f"Stop {maze[y][x]} found at ({x},{y})")
    return junctions

def getSetOfNearestJunctions(maze, junctions, x,y):
    # get list of nearest junctions
    nearest = []
    curPoints = [(x,y)]
    been = [(x,y)]
    cost = 0
    while curPoints:
        cost += 1
        newPoints = []
        for x,y in curPoints:
            for d in [(0,1),(1,0),(0,-1),(-1,0)]:
                if maze[y+d[1]][x+d[0]] != '#':
                    if (x+d[0],y+d[1]) not in been:
                        been.append((x+d[0],y+d[1]))
                        if (x+d[0],y+d[1]) in junctions:
                            nearest.append( ((x+d[0],y+d[1]),cost) )
                        else:
                            newPoints.append((x+d[0],y+d[1]))
        curPoints = newPoints
    # sort by cost
    nearest.sort(key=lambda x: x[1])
    # print(f"Nearest junctions from ({x},{y}) are {nearest}")
    return nearest

def getNearestJunctions(maze, junctions):
    nearestJs = {}
    for j in junctions:
        nearest = getSetOfNearestJunctions(maze, junctions, j[0],j[1])
        nearestJs[j] = nearest
    return nearestJs



def printMaze(maze, junctions=[]):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            print(maze[y][x], end='')
        print()
    print()

def getShortestPath(nearestJs, A, B):
    # get shortest path from A to B (in terms of distance)
    # A and B are tuples (x,y)
    # nearestJs is dict junction => list of neighbour Junctions and cost
    # Return the distance
    activeJs = nearestJs[A][:]
    visited = {}
    visited[A] = 0
    shortest = BIGNUM
    while len(activeJs):
        newActive = []
        for xy, cost in activeJs:
            if cost >= shortest:
                continue
            if xy == B:
                if cost < shortest:
                    shortest = cost
                continue
            if xy in visited:
                if cost >= visited[xy]:
                    continue
            visited[xy] = cost
            for jxy, hopCost in nearestJs[xy]:
                newCost = cost + hopCost
                for i, j in enumerate(newActive):
                    if j[0] == jxy:
                        if newCost < j[1]:
                            newActive[i] = (jxy, newCost)
                else:
                    newActive.append((jxy, newCost))
        activeJs = newActive
    if shortest == BIGNUM:
        print(f"Shortest path from {A} to {B} not found")
        sys.exit(1)
    return shortest        
        


def getShortestPaths(nearestJs, stops):
    # get shortest paths between all stops
    # stops is a list of tuples (x,y)
    # nearestJs is dict junction => list of neighbour Junctions and cost
    # Return a dict of (A,B) => distance
    graph = {}
    for i in range(len(stops)):
        for j in range(i+1, len(stops)):
            start = stops[i]
            end = stops[j]
            distance = getShortestPath(nearestJs, start, end)
            graph[(start, end)] = distance
            graph[(end, start)] = distance
            print(f"Shortest distance from {start} to {end} is {distance}")
    return graph

def doPart1(db):
    c = 0
    stops = getStops(db)
    maze = [ list(l) for l in db ]
    maze = blockOff(maze)
    J = getJunctions(maze)
    printMaze(maze, J)
    nearestJs = getNearestJunctions(maze, J)
    shortestPaths = getShortestPaths(nearestJs, stops)
    perms = itertools.permutations([i+1 for i in range(len(stops)-1)])
    shortest = BIGNUM
    shortestSeq = []
    costPath=''
    for p in perms:
        # print(f"Trying path 0 -> {p}")
        dist = 0
        cur = stops[0]
        cp ='0'
        for i in p:
            nextStop = stops[i]
            nextHop = shortestPaths[(cur, nextStop)]
            dist += nextHop
            cur = nextStop
            cp = cp + f" + {nextHop}"
        if dist < shortest:
            shortest = dist
            shortestSeq = p
            costPath = cp
            print(f"Shortest path is {shortest}")
            print(f"Shortest path sequence is {shortestSeq} with cost {costPath}")
    c = shortest
    return c

def doPart2(db):
    stops = getStops(db)
    maze = [ list(l) for l in db ]
    maze = blockOff(maze)
    J = getJunctions(maze)
    printMaze(maze, J)
    nearestJs = getNearestJunctions(maze, J)
    shortestPaths = getShortestPaths(nearestJs, stops)
    perms = itertools.permutations([i+1 for i in range(len(stops)-1)])
    shortest = BIGNUM
    shortestSeq = []
    costPath=''
    for p in perms:
        pp = list(p)
        pp.append(0)
        # print(f"Trying path 0 -> {pp}")
        dist = 0
        cur = stops[0]
        cp ='0'
        for i in pp:
            nextStop = stops[i]
            nextHop = shortestPaths[(cur, nextStop)]
            dist += nextHop
            cur = nextStop
            cp = cp + f" + {nextHop}"
        if dist < shortest:
            shortest = dist
            shortestSeq = pp
            costPath = cp
            print(f"Shortest path is {shortest}")
            print(f"Shortest path sequence is {shortestSeq} with cost {costPath}")
    c = shortest

    return c

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}.")


