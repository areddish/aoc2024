from aoc_helper import *
from collections import defaultdict

def check(update, rules):
    prev = update[0]
    for i, page in enumerate(update[1:]):
        if page not in rules[prev]:
            return False, i
        prev = page
    return True, 0

def fix(update, rules):
    good = False
    index = 0
    while not good:
        # move index right, could follow the dependency logic, but there isn't a lot of items per list
        update = update[:index] + [update[index+1], update[index]] + update[index+2:]
        good, index = check(update, rules)
    return update

#with open("test.txt") as file:
with open("day5.txt") as file:
    rules, updates = file.read().strip().split("\n\n")
    ans = 0
    ans2 = 0

    updates = [[int(x) for x in u.split(",")] for u in updates.split("\n")]
    page_rules = defaultdict(list)
    for rule in rules.split("\n"):
        x,y = [int(n) for n in rule.split("|")]
        page_rules[x].append(y)

    for update in updates:
        good, _ = check(update, page_rules)        
        #print(good, update[len(update)//2])
        if good:
            ans += update[len(update)//2]
        else:
            corrected_update = fix(update, page_rules)
            ans2 += corrected_update[len(corrected_update)//2]

    answer(ans)
    answer(ans2)
