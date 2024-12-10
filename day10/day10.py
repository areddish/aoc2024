from aoc_helper import *

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)
DIRECTIONS = [UP,RIGHT,DOWN,LEFT]

def walk(G, W, H, start, no_repeats = True):
    reached = 0
    seen = set()
    locations = [(start[0], start[1], 0)]
    while locations:
        next_ = []
        for sx,sy,height in locations:
            for dx,dy in DIRECTIONS:
                nx = sx + dx
                ny = sy + dy
                if no_repeats:
                    if (nx,ny,height) in seen:
                        continue
                    seen.add((nx,ny,height))
                if 0 <= nx < W and 0 <= ny < H and G[ny][nx] - height == 1:
                    if G[ny][nx] == 9:
                        reached += 1
                    else:                 
                        next_.append((nx,ny,height+1))
        locations = next_
    return reached

#with open("test.txt") as file:
#with open("test2.txt") as file:
#with open("test3.txt") as file:
#with open("test4.txt") as file:
#with open("test5.txt") as file:
with open("day10.txt") as file:
    lines = file.read().strip().splitlines()
    ans = 0
    ans2 = 0

    grid = []
    starts = []
    for j,line in enumerate(lines):
        row = []
        for i, ch in enumerate(line):
            val = -1 if ch == "." else int(ch)
            if val == 0:
                starts.append((i,j))
            row.append(val)
        grid.append(row)
    W = len(grid[0])
    H = len(grid)

    for s in starts:
        #print(f"{s=} {walk(grid, len(grid[0]), len(grid), s)}") 
        ans += walk(grid, W, H, s, no_repeats = True)
        ans2 += walk(grid, W, H, s, no_repeats = False)
    answer(ans)
    answer(ans2)