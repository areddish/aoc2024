from aoc_helper import *
from collections import defaultdict

#with open("test.txt") as file:
with open("day19.txt") as file:
    l1, l2 = file.read().strip().split("\n\n")

    all_patterns = set([word for word in l1.split(", ")])
    desired = [line.strip() for line in l2.split("\n")]

    DP = defaultdict(lambda: 0)
    def can_make_towel(all_patterns, towel):
        global DP
        if towel in DP:
            return DP[towel]
        
        # We got here due to following a combination and exhausted
        # the choices. Input doesn't contain empty words.
        if not towel:
            return 1       
        
        ways = 0
        for pattern in all_patterns:
            if towel.startswith(pattern):
                ways += can_make_towel(all_patterns, towel[len(pattern):])
        DP[towel] = ways
        return DP[towel]
    
    can_make_count = 0
    all_ways_count = 0
    for towel in desired:
        possible_ways = can_make_towel(all_patterns, towel)        
        if possible_ways > 0:
            can_make_count += 1
            all_ways_count += possible_ways

    answer(can_make_count)
    answer(all_ways_count)