from aoc_helper import *

def try_make_equation(ans, terms, allow_concat=False):
    vals = [(1, terms[0])]
    while vals:
        idx, current_val = vals.pop()
        if current_val == ans and idx == len(terms):
            return True
        if idx >= len(terms):
            continue
        term = terms[idx]
        idx += 1
        vals.append((idx, current_val + term))
        vals.append((idx, current_val * term))
        if allow_concat:
            vals.append((idx, int(str(current_val)+str(term))))
    return False

#with open("test.txt") as file:
with open("day7.txt") as file:
    lines = file.read().strip().splitlines()
    ans = 0
    ans2 = 0
    for l in lines:
        desired_value, eq = l.split(":")
        desired_value = int(desired_value)
        terms = [int(x) for x in eq.split()]
        if try_make_equation(desired_value, terms):
            ans += desired_value
            ans2 += desired_value
        elif try_make_equation(desired_value, terms, allow_concat=True):
            ans2 += desired_value
    answer(ans)
    answer(ans2)