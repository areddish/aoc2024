from aoc_helper import *
import heapq
from collections import deque
import functools

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)

DIRECTION_TO_COMMAND = {
    UP: "^",
    DOWN: "v",
    RIGHT: ">",
    LEFT: "<",
}

COMMANDS_TO_DIRECTION = {    
    "^": UP,
    "v": DOWN,
    ">": RIGHT,
    "<": LEFT,
    "A": None
}

CONTROLLER_KEY_TO_LOCATION = {
    "x": (0,0),
    "^": (1,0),
    "A": (2,0),    

    "<": (0,1),
    "v": (1,1),        
    ">": (2,1),    
}

keypad_start = (2, 3)
KEYPAD = 1
keypad_grid = [ list("789"), list("456"), list("123"), list("x0A") ]
controller_start = (2, 0)
CONTROLLER = 2
controller_grid = [ ["x", "^", "A"], ["<","v",">"]]

@functools.cache
def device_path(dev_number, loc, desired):
    device = keypad_grid if dev_number == 1 else controller_grid
    W = len(device[0])
    H = len(device)

    Q = [(0, loc, "")]
    visited = set()
    all_paths = []
    min_len = None
    while Q:
        dist, cur, path = heapq.heappop(Q)
        x, y = cur

        if min_len and dist > min_len:
            continue

        if (x,y, path) in visited:
            continue
        visited.add((x,y, path))
        
        if device[y][x] == "x":            
            assert False, "panic!"

        if device[y][x] == desired:
            all_paths.append((path + "A", (x,y)))
            if not min_len:
                min_len = len(path + "A")
            
        for dx,dy in [DOWN, LEFT, UP, RIGHT]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < W and 0 <= ny < H and device[ny][nx] != "x":
                heapq.heappush(Q, (dist + 1, (nx,ny), path+DIRECTION_TO_COMMAND[(dx,dy)]))

    shortest_paths = []
    for p, c in all_paths:
        if len(p) == min_len:
            shortest_paths.append((p, c))
    return shortest_paths

# Pre=compute all paths
# (robot_location, target, cost)
all = {}
for y in range(len(controller_grid)):
    for x in range(len(controller_grid[0])):
        if controller_grid[y][x] == "x":
            continue
        robot_loc = (x,y)
        for ch in "<>^vA":
            options = device_path(CONTROLLER, robot_loc, ch)
            all[(x,y,ch)] = options

# Readding the forums indicated some of these solutions may be less
# optimal but seems to work same with or with out them
# all[(2,0,"<")].pop(0)
# all[(0,1,"A")].pop()
# all[(2,0,"v")].pop(0)

def forward_sim(codes, device, start):
    result = ""
    x,y = start
    for ch in codes:
        assert ch != " ", "Panic!"
        if ch == "A":
            # capture result 
            result += keypad_grid[y][x] if device == 1 else controller_grid[y][x]
        else:
            dx,dy = COMMANDS_TO_DIRECTION[ch]
            x += dx
            y += dy
    return result

def check_solution(code, num_robots):
    for _ in range(num_robots):
        code = forward_sim(code, 2, (2,0))
    # punch into keypad
    return forward_sim(code, 1, (2,3))

@functools.cache
def bfs_min_path_controller(ch, x , y, depth, max_depth):
    # if depth % 5 == 0:
    #     print(x,y,depth)
    if depth >= max_depth:
        assert len(all[(x,y,ch)]) == 1 or len(all[(x,y,ch)][0][0]) == len(all[(x,y,ch)][1][0]) 
        p, l = all[(x,y,ch)][0]
       # print(f"returning {depth=} {p=} {l=}")
        return len(p)

    best = None
    for p in all[(x,y,ch)]:        
        loc = controller_start
        result = 0
        for ch2 in p[0]:
            r = bfs_min_path_controller(ch2, *loc, depth+1, max_depth)
            loc = CONTROLLER_KEY_TO_LOCATION[ch2]
            result += r
        if not best or result < best:
            best = result
    #print(ch, x, y, depth, best)
    return best

def transform(code, device, cur):
    Q = deque([(code, "", cur)])
    ans = []
    min_path_size = 1e9
    while Q:
        next_part, cur_path, cur = Q.popleft()

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

ans = 0
#with open("test.txt") as file:
with open("day21.txt") as file:
    lines = file.read().strip().splitlines()
    location = None
    for NUM_ROBOTS in [2, 25]:
        ans = 0
        for code in lines:        
            val = int("".join(code[:-1]))
            #print(code, val)
            options = []
            for ways in transform(code, KEYPAD, (2,3)):
                #print(ways)                
                p_length = 0
                robot_input = 0
                loc = controller_start
                for ch in ways:
                    shortest = bfs_min_path_controller(ch,*loc,0,NUM_ROBOTS-1)
                    loc = CONTROLLER_KEY_TO_LOCATION[ch]
                    robot_input += shortest
                options.append(robot_input)
                #print(robot_input, check_solution(robot_input, NUM_ROBOTS))              
            ans += min(options) * val
        answer(ans)