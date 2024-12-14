from aoc_helper import *
import numpy as np
import functools
import sys
sys.setrecursionlimit(10**6)

@functools.cache
def play(x,y,a,b,p,cur_move,spent, a_presses, b_presses):    
    px,py = p
    #print(x,y)
    if x == px and y == py:
        return spent
    
    if x > px or y > py:
        return 0
    ax,ay = a
    bx,by = b
    a_press = 0
    b_press = 0
    # press a
    if a_press < 100:
        a_press = play(x+ax,y+ay,a,b,p, cur_move+1, spent+3,a_presses + 1, b_presses)
    # press b
    if b_press < 100:
        b_press = play(x+bx,y+by,a,b,p, cur_move+1, spent+1,a_presses, b_presses+1)

    if a_press != 0 and b_press != 0:
        return min (a_press, b_press)
    elif a_press != 0:
        return a_press
    else:
        return b_press

#with open("test.txt") as file:
with open("day13.txt") as file:
    lines = file.read().strip().split("\n\n")
    ans = 0
    ans2 = 0

    claws = []
    for line in lines:
        parts = line.split("\n")
        claws.append({
            "A": tuple(nums(parts[0])),
            "B": tuple(nums(parts[1])),
            "Prize": tuple(nums(parts[2])),
        })

    for offset in [0, 10000000000000]:
        ans = 0
        for j, c in enumerate(claws):
            #ans += play(0,0,c["A"],c["B"],c["Prize"],0,0,0,0)
            ax,ay = c["A"]
            bx,by = c["B"]
            px,py = c["Prize"]
            px = px + offset
            py = py + offset
            a = np.array([[ax,bx],[ay,by]])
            b = np.array([px,py])
            solution = np.linalg.solve(a,b)
            sx2,sy2 = [int(float(x)+0.5) for x in np.around(solution)]
            if sx2 <= 0 or sy2 <= 0:
                continue

            if abs((sx2*ax + sy2*bx) - px) < 1e-16 and abs((sx2*ay + sy2*by) - py) < 1e-16:
                ans += sx2 * 3 + sy2
        answer(ans)
