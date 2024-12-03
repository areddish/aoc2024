from aoc_helper import *

def check_safe(vals):
    desired_count = len(vals) - 1
    inc_count = 0
    dec_count = 0
    diff_count = 0
    prev = vals[0]
    for v in vals[1:]:
        diff = v - prev
        if diff > 0:
            inc_count += 1
        elif diff < 0:
            dec_count += 1
        diff = abs(diff)
        if (1 <= diff <= 3):
            diff_count += 1
        else:
            return False # if any diff size is outside of bound we can early terminate
        prev = v
    return (diff_count == desired_count) and (inc_count == desired_count or dec_count == desired_count)

#with open("test.txt") as file:
with open("day2.txt") as file:
    lines = file.read().strip().splitlines()
    data = nums(lines)
    ans = 0
    ans2 = 0
    for vals in data:
        if check_safe(vals):
            ans += 1

        for i in range(len(vals)):
            if check_safe(vals[:i]+vals[i+1:]):
                ans2 += 1
                break
    answer(ans)
    answer(ans2)