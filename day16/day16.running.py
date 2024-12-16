import heapq
from aoc_helper import *
import itertools
from collections import deque, Counter, defaultdict

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)

move_to_dir_map = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT,
    "\n": (0,0) 
}

DIRS = [RIGHT, DOWN, LEFT, UP]

def cw(dir):
    if dir == UP:
        dir = RIGHT
    elif dir == RIGHT:
        dir = DOWN
    elif dir == DOWN:
        dir = LEFT
    else:
        assert dir == LEFT, dir
        dir = UP
    return dir

def ccw(dir):
    if dir == UP:
        dir = LEFT
    elif dir == RIGHT:
        dir = UP
    elif dir == DOWN:
        dir = RIGHT
    else:
        assert dir == LEFT, dir
        dir = DOWN
    return dir 

def dijkstra_algorithm(start, end, board):
    w = len(board[0])
    h = len(board)

    dir = RIGHT
    visited = set()
    nodes = [(0, dir, *start)]
    path = []
    while nodes:
        dist, dir, x, y = heapq.heappop(nodes)
        if (x,y,dir) in visited:
            continue
        visited.add((x,y,dir))
        #end condidtion
        if x == end[0] and y == end[1]:
            print(path)
            return dist, path

        for offset in [(1,*dir), (1000, *cw(dir)), (1000, *ccw(dir))]:
            cost, dx,dy = offset
            nx = x
            ny = y
            if cost == 1:
                nx = x + dx
                ny = y + dy

            if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#" and (nx,ny, (dx,dy)) not in visited:
                # distance/compute equation
                heapq.heappush(nodes, (dist + cost, (dx,dy), nx,ny))


def dijkstra_algorithm2(start, end, board):
    w = len(board[0])
    h = len(board)

    dir = RIGHT
    visited = set()
    score = defaultdict(lambda: 1e6)
    prev = {}
    nodes = [(0, dir, *start)]
    path = []

    while nodes:
        dist, dir, x, y = heapq.heappop(nodes)
        # if (x,y,dir) in visited:
        #     continue
        # visited.add((x,y,dir))
        #end condidtion
        if x == end[0] and y == end[1]:
            path = [end]
            Tx,Ty=end
            while Tx != start[0] and Ty != start[1]:
                px,py = prev[(Tx,Ty)]
                path.append((px,py))
                Tx = px
                Ty = py
            print(path)
            return dist, path

        for offset in [(1,*dir), (1000, *cw(dir)), (1000, *ccw(dir))]:
            cost, dx,dy = offset
            nx = x
            ny = y
            if cost == 1:
                nx = x + dx
                ny = y + dy

            alt = cost + dist
            if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#":# and (nx,ny, (dx,dy)) not in visited:
                # distance/compute equation
                if alt < score[(nx,ny,dx,dy)]:
                    prev[(nx,ny)] = (x,y)
                    score[(nx,ny,dx,dy)] = alt
                    heapq.heappush(nodes, (dist + cost, (dx,dy), nx,ny))
    print("no find")
    return 0, []
                
import sys
import copy
sys.setrecursionlimit(1000000)
def find_all(start, end, board, score):
    w = len(board[0])
    h = len(board)

    x,y = start
    Q = [(x,y,*RIGHT, 0, [(x,y)], set())]
    all_paths = []
    while Q:
        x,y,dx,dy,current_path_cost, path, visited = Q.pop()
        print(len(Q))
        if x == end[0] and y == end[1]:
            #print("Found Path!", current_path_cost, path)
            all_paths.append((current_path_cost, path))

        if current_path_cost > score:
            continue

        if (x,y,dx,dy) in visited:
            continue

        v1 = visited.copy()
        v2 = visited.copy()
        v3 = visited.copy()
        v1.add((x,y,dx,dy))
        v2.add((x,y,dx,dy))
        v3.add((x,y,dx,dy))

        cw_dir = cw((dx,dy))
        ccw_dir = ccw((dx,dy))
        # if (x,y,*cw_dir) not in visited:
        #     Q.append((x,y,*cw_dir, current_path_cost + 1000))
        # if (x,y,*ccw_dir) not in visited:
        #     Q.append((x,y,*ccw_dir, current_path_cost + 1000))

        nx = x + dx
        ny = y + dy    
        if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#" and (nx,ny, (dx,dx)) not in visited:
            p = path.copy()
            p.append((nx,ny))
            Q.append((nx,ny,dx,dy, current_path_cost + 1, p, v1))

        dx,dy = cw_dir
        nx = x + dx
        ny = y + dy    
        if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#" and (nx,ny, (dx,dx)) not in visited:
            p = path.copy()
            p.append((nx,ny))
            Q.append((nx,ny,dx,dy, current_path_cost + 1001, p, v2))

        dx,dy = ccw_dir
        nx = x + dx
        ny = y + dy    
        if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#" and (nx,ny, (dx,dx)) not in visited:
            p = path.copy()
            p.append((nx,ny))
            Q.append((nx,ny,dx,dy, current_path_cost + 1001, p, v3))
    return all_paths

#with open("test.txt") as file:
#with open("test2.txt") as file:
#with open("test3.txt") as file:
with open("day16.txt") as file:
    ans = 0
    ans2 = 0
    grid = []
    start = None
    end = None
    dir = RIGHT
    lines = file.read().strip().split("\n")
    for j,line in enumerate(lines):
        row = []
        for i,ch in enumerate(line):
            row.append(ch)
            if ch == "S":
                start = (i,j)
            if ch == "E":
                end = (i,j)
        grid.append(row)

    print(start,end)

    ans, path = dijkstra_algorithm(start, end, grid)
    answer(ans)
    def pp(grid, path):
        W = len(grid[0])
        H = len(grid)
        for y in range(H):
            for x in range(W):
                if (x,y) in path:
                    ch = "*"
                else:
                    ch = grid[y][x]
                print(ch, end="")
            print()

    pp(grid, path)
    tiles = set()
    all_paths = find_all(start, end, grid, ans)
    for cost, path in all_paths:
        print("Path: ", cost)
        for p in path:
            tiles.add(p)
        #pp(grid, path)
    answer(len(tiles))

