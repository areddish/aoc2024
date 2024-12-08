#python ..\aoc_helper\src\aoc_helper\input.py
from aoc_helper import *
from collections import defaultdict
import itertools

def find_antinodes2(p1, p2, W, H):
    x1,y1 = p1
    x2,y2 = p2
    dx = x2-x1
    dy = y2-y1

    test_pt = (x1, y1)
    test_pt2 =(x2, y2)

    result = set()
    all_results = set([test_pt, test_pt2])
    first_run = True
    while 0 <= test_pt[0] < W or 0 <= test_pt[1] < H or 0 <= test_pt2[0] < W or 0 <= test_pt2[1] < H:
        x1,y1 = test_pt
        x2,y2 = test_pt2
        test_pt = (x1-dx, y1-dy)
        test_pt2 = (x2+dx, y2+dy)
        if 0 <= test_pt[0] < W and 0 <= test_pt[1] < H:
            if first_run:
                result.add(test_pt)
            all_results.add(test_pt)
        if 0 <= test_pt2[0] < W and 0 <= test_pt2[1] < H:
            if first_run:
                result.add(test_pt2)
            all_results.add(test_pt2)
        first_run = False
    return result, all_results

#with open("test.txt") as file:
#with open("test2.txt") as file:
#with open('test3.txt') as file:
with open("day8.txt") as file:
    lines = file.read().strip().splitlines()
    H = 0
    W = 0
    nodes = defaultdict(list)
    for j,l in enumerate(lines):
        W = len(l)
        for i,ch in enumerate(l):
            if ch != ".":
                nodes[ch].append((i,j))
        H += 1
    locs = set()
    locs_part2 = set()
    for freq in nodes:
        antennas = nodes[freq]
        if len(antennas) <= 1:
            continue
        for antenna_pair in itertools.combinations(antennas, 2):
            antinodes, part2_antinodes = find_antinodes2(*antenna_pair, W, H)
            locs = locs.union(antinodes)
            locs_part2 = locs_part2.union(part2_antinodes)

    answer(len(locs))
    answer(len(locs_part2))