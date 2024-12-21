from aoc_helper import *
import heapq
from collections import defaultdict

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)


def dijkstra_algorithm(start, end, grid):
    h = len(grid)
    w = len(grid[0])

    dist = defaultdict(lambda: (w*h)**2)
    visited = set()
    nodes = [(0, *start)]
    dist[start] = 0
    path = defaultdict(lambda: None)
    #path[start] = None
    while nodes:
        d, x, y = heapq.heappop(nodes)
        if (x,y) in visited:
            continue
        visited.add((x,y))
        if x == end[0] and y == end[1]:
            if d < dist[(x,y)]:
                dist[(x,y)] = d
        for offset in [LEFT, RIGHT, UP, DOWN]:
            dx,dy = offset
            nx = x + dx
            ny = y + dy
            if 0 <= ny <= h and 0 <= nx <= w and grid[ny][nx] != "#":
                heapq.heappush(nodes, (d + 1, nx,ny))
                if d + 1 < dist[(nx,ny)]:
                    dist[(nx,ny)] = d + 1
                    path[(nx,ny)] = (x,y)
    return dist, path

def find_cheats(start, path, to_end_distance, cheat_distance_allowed=2, save_distance_goal=100):
    ans = set()
    for x,y in path:
        dist_from_end = to_end_distance[(x,y)]
        if dist_from_end > to_end_distance[start]:
            continue
        for dy in range(-cheat_distance_allowed,cheat_distance_allowed+1,1):
            for dx in range(-cheat_distance_allowed,cheat_distance_allowed+1,1):
                nx = x + dx
                ny = y + dy
                distance_between_cheat_points = abs(dx) + abs(dy)
                distance_saved = dist_from_end - to_end_distance[(nx,ny)] - distance_between_cheat_points
                if distance_between_cheat_points <= cheat_distance_allowed and distance_saved >= save_distance_goal:
                    #print(f"start = {(x,y)} end = {(nx,ny)}")
                    ans.add((x,y,nx,ny))

    return len(ans)

#with open("test.txt") as file:
with open("day20.txt") as file:
    lines = file.read().strip().splitlines()
    location = None

    grid = []
    start = None
    end = None
    for y,line in enumerate(lines):
        row = []
        for x,ch in enumerate(line):
            row.append(ch)
            if ch == "S":
                start = (x,y)
            if ch == "E":
                end = (x,y)
        grid.append(row)

    W = len(grid[0])
    H = len(grid)

    to_end_distance, path = dijkstra_algorithm(end, start, grid)
    print(to_end_distance[start])

    answer(find_cheats(start, path, to_end_distance, 2, 100))
    answer(find_cheats(start, path, to_end_distance, 20, 100))