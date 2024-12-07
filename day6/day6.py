#python ..\aoc_helper\src\aoc_helper\input.py
from aoc_helper import *
from collections import defaultdict

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)

def printg(G, obs):
    W = len(G[0])
    H = len(G)
    for y in range(H):
        for x in range(W):
            if (x,y) in obs:
                print("O", end="")
            else:
                print(G[y][x],end="")
        print()
    print()

def has_loop(G, sx, sy, ox, oy, cur_path):
    cur = start
    dir = UP
    path = set()
    while 0 <= cur[0] < W and 0 <= cur[1] < H:
        x,y = cur
        if G[y][x] == "#" or cur == (ox,oy):
            cur = (cur[0] - dir[0], cur[1] - dir[1])
            if dir == UP:
                dir = RIGHT
            elif dir == RIGHT:
                dir = DOWN
            elif dir == DOWN:
                dir = LEFT
            else:
                assert dir == LEFT, dir
                dir = UP
            # rotate
        else:
            if (x,y,dir) in cur_path or (x,y,dir) in path:
                return True
            path.add((x,y,dir))
        cur = (cur[0] + dir[0], cur[1] + dir[1])
    
    return False

#with open("test.txt") as file:
with open("day6.txt") as file:
    lines = file.read().strip().splitlines()
    ans = 0
    ans2 = 0

    start = (None, None)
    piles = set()
    G = []
    dir = UP
    for j,line in enumerate(lines):
        G.append(line)
        for i, ch in enumerate(line):
            if ch == "^":
                start = (i,j)
            if ch == "#":
                piles.add((i,j))
    W = len(G[0])
    H = len(G)

    cur = start
    ans = 1
    path = set()
    obs = set()

    while 0 <= cur[0] < W and 0 <= cur[1] < H:
        x,y = cur
        if G[y][x] == "#":
            cur = (cur[0] - dir[0], cur[1] - dir[1])
            if dir == UP:
                dir = RIGHT
            elif dir == RIGHT:
                dir = DOWN
            elif dir == DOWN:
                dir = LEFT
            else:
                assert dir == LEFT, dir
                dir = UP
            # rotate
        else:
            #printg(G, x, y)
            path.add((x,y,dir))
            ans += 1
        # Move
        sx,sy = cur
        cur = (cur[0] + dir[0], cur[1] + dir[1])
        if has_loop(G, *start, *cur, set()):
            obs.add((cur[0], cur[1]))

    answer(len(set([(x[0],x[1]) for x in path])))
    answer(len(obs))# - set(start) - piles))