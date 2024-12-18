from aoc_helper import *
import heapq

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)

def dijkstra_algorithm(start, end, corrupted):
    w,h = end
    visited = set()
    nodes = [(0, *start)]
    while nodes:
        dist, x, y = heapq.heappop(nodes)
        if (x,y) in visited:
            continue
        visited.add((x,y))
        if x == end[0] and y == end[1]:
            return dist
        
        for offset in [LEFT, RIGHT, UP, DOWN]:
            dx,dy = offset
            nx = x + dx
            ny = y + dy
            if 0 <= ny <= h and 0 <= nx <= w and (nx,ny) not in corrupted:
                heapq.heappush(nodes, (dist + 1, nx,ny))
    return None

#with open("test.txt") as file:
with open("day18.txt") as file:
    lines = file.read().strip().splitlines()
    location = None

    bytes = []
    for j,line in enumerate(lines):
        x,y = [int(x) for x in line.split(",")]
        bytes.append((x,y))

    corrupted = set()
    # for y in range(6):
    #     for x in range(6):
    #         print("#" if (x,y) in corrupted else ".", end="")
    #     print()

    start = (0,0)
    end = (70,70)
    mem_used = 0
    can_reach = True
    while mem_used < len(bytes) and can_reach:
        index = mem_used % len(bytes)
        x,y = bytes[index]        
        corrupted.add((x,y))
        bytes[index] = (x, y+1)
        mem_used += 1

        steps = dijkstra_algorithm(start, end, corrupted)
        can_reach = steps != None
        if mem_used == 1024:
            answer(steps)
        if not can_reach:
            answer(f"{x},{y}")