import heapq
from aoc_helper import *
import itertools
from collections import deque, Counter, defaultdict

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)

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

    ans = None
    while nodes:
        dist, dir, x, y = heapq.heappop(nodes)
        if (x,y,dir) in visited:
            continue
        visited.add((x,y,dir))
        #end condidtion
        if x == end[0] and y == end[1]:
            #print("Found 1")
            return dist, path
            if not ans:
                ans = dist, path

        for offset in [(1,*dir), (1001, *cw(dir)), (1001, *ccw(dir)), (2001, *cw(cw(dir)))]:
            cost, dx,dy = offset
            nx = x + dx
            ny = y + dy

            if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#":# and (nx,ny, (dx,dy)) not in visited:
                # distance/compute equation
                heapq.heappush(nodes, (dist + cost, (dx,dy), nx,ny))
#        if dist < 92432:
#            heapq.heappush(nodes, (dist, dir, x, y))
    return ans

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

DP = {}
def dp_find_all(start, dir, end, cost, score, path):
    global grid
    global DP
    w = len(grid[0])
    h = len(grid)
    
    if (start, dir) in DP:
        return DP[(start, dir)]
    
    if start == end:
        DP[(start, dir)] = (cost, path)
        return (cost, path)
    
    if cost > score:
        DP[(start, dir)] = (cost, [])
        return (cost, [])

    x,y = start
    dx,dy = dir
    cw_dir = cw((dx,dy))
    ccw_dir = ccw((dx,dy))

    nx = x + dx
    ny = y + dy    
    if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#":
        p = path.copy()
        p.append((nx,ny))
        dp_find_all((nx,ny), (dx,dy), end, cost + 1, score, p)

    dx,dy = cw_dir
    nx = x + dx
    ny = y + dy    
    if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#":
        p = path.copy()
        p.append((nx,ny))
        dp_find_all((nx,ny), (dx,dy), end, cost + 1001, score, p)

    dx,dy = ccw_dir
    nx = x + dx
    ny = y + dy    
    if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#":
        p = path.copy()
        p.append((nx,ny))
        dp_find_all((nx,ny), (dx,dy), end, cost + 1001, score, p)
    
    return [(10000, [])]

def find_all(start, end, board, score):
    w = len(board[0])
    h = len(board)

    x,y = start
    Q = [(x,y,*RIGHT, 0, [(x,y)])]
    visited = set()
    all_paths = []
    while Q:
        x,y,dx,dy,current_path_cost, path = Q.pop()
        print(len(Q))
        if x == end[0] and y == end[1]:
            #print("Found Path!", current_path_cost, path)
            all_paths.append((current_path_cost, path))

        if current_path_cost > score:
            continue

        if (x,y,dx,dy) in visited:
            continue
        visited.add((x,y,dx,dy, ((x,y) for x,y in path)))

        cw_dir = cw((dx,dy))
        ccw_dir = ccw((dx,dy))
        # if (x,y,*cw_dir) not in visited:
        #     Q.append((x,y,*cw_dir, current_path_cost + 1000))
        # if (x,y,*ccw_dir) not in visited:
        #     Q.append((x,y,*ccw_dir, current_path_cost + 1000))

        nx = x + dx
        ny = y + dy    
        if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#" and (nx,ny, (dx,dx), ((x,y) for x,y in path + [(nx,ny)])) not in visited:
            p = path.copy()
            p.append((nx,ny))
            Q.append((nx,ny,dx,dy, current_path_cost + 1, p))

        dx,dy = cw_dir
        nx = x + dx
        ny = y + dy    
        if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#" and (nx,ny, (dx,dx), ((x,y) for x,y in path + [(nx,ny)])) not in visited:
            p = path.copy()
            p.append((nx,ny))
            Q.append((nx,ny,dx,dy, current_path_cost + 1001, p))

        dx,dy = ccw_dir
        nx = x + dx
        ny = y + dy    
        if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != "#" and (nx,ny, (dx,dx), ((x,y) for x,y in path + [(nx,ny)])) not in visited:
            p = path.copy()
            p.append((nx,ny))
            Q.append((nx,ny,dx,dy, current_path_cost + 1001, p))
    return all_paths

def bfs(start, end, board):
    w = len(board[0])
    h = len(board)
    Q = deque([(*start, *RIGHT, 0, list())])
    visited = set()
    paths = []
    while Q:
        x,y,dx,dy,dist,path = Q.popleft()

        if (x,y,dx,dy) in visited:
            continue
      
        if x == end[0] and y == end[1]:
            paths.append(path)

        for move in [(1,dx,dy), (1001,*cw((dx,dy))), (1001, *ccw((dx,dy))), (2001, *cw(cw((dx,dy))))]:
            cost, xoff, yoff = move
            nx = x + xoff
            ny = y + yoff

            if 0 <= ny < h and 0 <= nx < w and board[ny][nx] != "#" and dist + cost <= 92432 and (nx,ny,xoff,yoff) not in visited:
                p2 = path.copy()
                p2.append((nx,ny))
                Q.append((nx,ny,xoff,yoff,dist+cost, p2))

    return paths

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
    bfs(start, end, grid)
    exit()

    for y in range(len(grid)):
        print(y, len(grid))
        for x in range(len(grid[0])):
            if grid[y][x] != "#":
                s1, p1 = dijkstra_algorithm((x,y), start, grid)
                s2, p2 = dijkstra_algorithm((x,y), end, grid)
                if s1+s2 == ans:
                    print("hmm..",s1,s2)
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

    bfs(start, end, grid)
    exit()
    pp(grid, path)
    tiles = set()
    #all_paths = find_all(start, end, grid, ans)
    all_paths = dp_find_all(start, RIGHT, end, 0, ans, list())
    for cost, path in all_paths:
        print("Path: ", cost)
        for p in path:
            tiles.add(p)
        #pp(grid, path)
    answer(len(tiles))

