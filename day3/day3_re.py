from aoc_helper import *
import re

with open("day3.txt") as file:
    str = file.read().strip()
    matches = re.findall(f"mul\((\d+),(\d+)\)", str)
    ans = sum([int(x[0])*int(x[1]) for x in matches])
    answer(ans)

    matches = re.findall(f"(mul)\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)", str)
    enabled = True
    ans2 = 0
    for match in matches:
        if match[4] == "don't":
            enabled = False
        elif match[3] == "do":
            enabled = True
        elif enabled:
            ans2 += int(match[2])*int(match[1])
    answer(ans2)