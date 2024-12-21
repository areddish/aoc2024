from aoc_helper import *
import heapq
from collections import defaultdict, deque

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)


def code_on_keypad(code, cur):
    path = ""
    for ch in code:
        sub_path, cur = device_path(keypad, cur, ch)
        path += sub_path
    return path, cur

def command_on_dir(command, cur):
    path = ""
    for ch in command:
        sub_path, cur = device_path(controller, cur, ch)
        path += sub_path
    return path, cur


# def dijkstra_algorithm(start, end, grid):
#     h = len(grid)
#     w = len(grid[0])

#     dist = defaultdict(lambda: (w*h)**2)
#     visited = set()
#     nodes = [(0, *start)]
#     dist[start] = 0
#     path = defaultdict(lambda: None)
#     #path[start] = None
#     while nodes:
#         d, x, y = heapq.heappop(nodes)
#         if (x,y) in visited:
#             continue
#         visited.add((x,y))
#         if x == end[0] and y == end[1]:
#             if d < dist[(x,y)]:
#                 dist[(x,y)] = d
#         for offset in [LEFT, RIGHT, UP, DOWN]:
#             dx,dy = offset
#             nx = x + dx
#             ny = y + dy
#             if 0 <= ny <= h and 0 <= nx <= w and grid[ny][nx] != "#":
#                 heapq.heappush(nodes, (d + 1, nx,ny))
#                 if d + 1 < dist[(nx,ny)]:
#                     dist[(nx,ny)] = d + 1
#                     path[(nx,ny)] = (x,y)
#     return dist, path


d_to_c = {
    UP: "^",
    DOWN: "v",
    RIGHT: ">",
    LEFT: "<",
}

commands = {    
    "^": UP,
    "v": DOWN,
    ">": RIGHT,
    "<": LEFT,
    "A": None
}

keypad_start = (2, 3)
keypad = 1
keypad_gird = [ list("789"), list("456"), list("123"), list("x0A") ]
controller_start = (2, 0)
controller = 2
controller_grid = [ ["x", "^", "A"], ["<","v",">"]]

import functools

@functools.cache
def device_path(dev_number, loc, desired):
    device = keypad_gird if dev_number == 1 else controller_grid
    W = len(device[0])
    H = len(device)

    Q = [(0, loc, DOWN, "")]
    visited = set()
    all_paths = []
    min_len = None
    while Q:
        dist, cur, dir, path = heapq.heappop(Q)
        x, y = cur

        if min_len and dist > min_len:
            continue

        if (x,y, path) in visited:
            continue
        visited.add((x,y, path))

        
        if device[y][x] == "x":
            assert False, "f"
            continue

        if device[y][x] == desired:
            all_paths.append((path + "A", (x,y)))
            if not min_len:
                min_len = len(path + "A")
            
            #return path+"A", (x,y)
        
        for dx,dy in [DOWN, LEFT, UP, RIGHT]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < W and 0 <= ny < H and device[ny][nx] != "x":
                heapq.heappush(Q, (dist + 1, (nx,ny), (dx,dy), path+d_to_c[(dx,dy)]))

    shortest_paths = []
    for p, c in all_paths:
        if len(p) == min_len:
            shortest_paths.append((p, c))
    return shortest_paths

def transform(code, device, cur):
    Q = deque([(code, "", cur)])
    ans = []
    min_path_size = 1e9
    while Q:
        next_part, cur_path, cur = Q.popleft(0)

        if len(cur_path) > min_path_size:
            continue
        if not next_part:
            ans.append(cur_path)
            min_path_size = min(min_path_size, len(cur_path))
            continue

        ch = next_part[0]
        rest = next_part[1:]

        for paths in device_path(device, cur, ch):
            Q.append((rest, cur_path + paths[0], paths[1]))
                
    return ans


#with open("test.txt") as file:
with open("day21.txt") as file:
    lines = file.read().strip().splitlines()
    location = None

    codes = []
    
    for y,line in enumerate(lines):
        code = list(line)
        val = int("".join(line[:-1]))

        # path, cur = code_on_keypad(code, keypad_start)
        # print(len(path))
        # path, cur = command_on_dir(path, controller_start)
        # print(len(path))
        # path, cur = command_on_dir(path, controller_start)
        # print(len(path))
        
        print("processing",code)
        # for
        l2 = transform(code, keypad, keypad_start)
        print("l2 = ",len(l2))
        l3 = []
        for p in l2:
            l3 = l3 + transform(p, controller, controller_start)
        print("l3 = ", len(l3))
        l4 = []
        for p in l3:
            l4 = l4 + transform(p, controller, controller_start)       
            if len(l4) % 2000:
                print("len", len(l4))     
        m_path = min([len(p) for p in l4])
        print(code, m_path)

        codes.append((code, val, m_path))
       

    ans = 0
    for code, val, len_path in codes:
        print(f"{code=} {val=} {len_path=} {len_path*val}")
        ans += len_path * val
    answer(ans)
    #answer(find_cheats(start, path, to_end_distance, 20, 100))

#     029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
