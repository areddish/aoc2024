import re

def nums(lines):
    nums = []
    for line in lines:
        nums.append([int(x) for x in re.findall(r"(\d+)", line)])
    return nums