from collections import defaultdict

import pyperclip
answer_part = 1
def answer(v):
    global answer_part
    pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2

l1 = []
l2 = []
l2_counter = defaultdict(int)
#with open("test.txt") as file:
with open("day1.txt") as file:
    lines = file.read().strip().splitlines()

for l in lines:
    x,y = [int(n) for n in l.split()]
    l1.append(x)
    l2.append(y)
    l2_counter[y] += 1

ans = 0
for left, right in zip(sorted(l1), sorted(l2)):
    ans += abs(left - right)
answer(ans)   

ans = 0
for l in l1:
    ans += l2_counter[l]*l
answer(ans)