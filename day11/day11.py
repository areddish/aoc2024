from aoc_helper import *
from collections import Counter

# Part 2 can't compute, so instead of trying to build the actual result
# we just track the counts of the stone faces, then update the counts
# per the rules, afterwards the procssed stones should be removed.
def fast_blink(stone_value, stone_occurences, stone_counter):
    if stone_value == 0:
        stone_counter[1] += stone_occurences
    else:
        s = str(stone_value)
        n = len(s)
        if n % 2 == 0:
            mid = n // 2
            right = int(s[mid:])
            left = int(s[:mid])    
            stone_counter[left] += stone_occurences
            stone_counter[right] += stone_occurences
        else:
            stone_counter[stone_value * 2024] += stone_occurences
    stone_counter[stone_value] -= stone_occurences

with open("day11.txt") as file:
    lines = file.read().strip()
    # lines = "0 1 10 99 999"
    # lines = "125 17"
    stones = [int(x) for x in lines.split()]
    ans = 0
    ans2 = 0
    counter = Counter(stones)
    for i in range(75):
        for stone_value,stone_occurence in list(counter.items()):
            fast_blink(stone_value, stone_occurence, counter)
        if i == 24:
            for stone_value,stone_occurence in counter.items():
                ans += stone_occurence
    for stone_value,stone_occurence in counter.items():
        ans2 += stone_occurence
    answer(ans)
    answer(ans2)

# # Original solution used for part 1
# # Just does pure transform
# def blink(stone):
#     if stone == 0:
#         return [1]
#     else:
#         s = str(stone)
#         if len(s) % 2 == 0:        
#             right = int(s[(len(s)//2):])
#             left = int(s[:len(s)//2])    
#             return [left, right]
#         else:
#             return [stone*2024]

# with open("day11.txt") as file:
#     lines = file.read().strip()
#     stones = [int(x) for x in lines.split()]
#     for _ in range(25):
#         new_ = []
#         for stone in stones:
#             new_ += blink(stone)
#         stones = new_
#     answer(len(stones))