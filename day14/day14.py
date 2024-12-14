from aoc_helper import *

def part1(robots,W,H):
    midpoint_x = W // 2
    midpoint_y = H // 2
    q = [0,0,0,0] 
    for r in robots:
        x,y,vx,vy = r
        if x < midpoint_x:
            if y<midpoint_y:
                q[0] += 1
            elif y > midpoint_y:
                q[3] += 1
        elif x > midpoint_x:
            if y<midpoint_y:
                q[1] += 1
            elif y >midpoint_y:
                q[2] += 1
    answer(q[0]*q[1]*q[2]*q[3])

# Image was found by noticing pattern where they started bunching up, then advancing by mulitpling by 
# 101 each frame until the image appeared. Just matched it since the positions are unique and match the
# original robot count.
# def prettyprint(robots):
#     for y in range(H):
#         for x in range(W):
#             if (x,y) in robots:
#                 print("*", end="")
#             else:
#                 print(".", end="")
#         print()
target = {}
with open("xmas.txt") as file:
    for j, l in enumerate(file.read().strip().splitlines()):
        for i,ch in enumerate(l):
            if ch == "*":
                target[(i,j)] = 1
print(len(target))

#with open("test.txt") as file:
with open("day14.txt") as file:
    lines = file.read().strip().split("\n")
    robots = []
    for line in lines:
        parts = line.split()
        x,y = [int(x) for x in parts[0].split("=")[1].split(",")]
        vx,vy = [int(x) for x in parts[1].split("=")[1].split(",")]
        robots.append((x,y,vx,vy))

    W = 101
    H = 103    
    #W = 11 
    #H = 7

    i = 0
    while True:
        for j in range(len(robots)):
            x,y,vx,vy = robots[j]
            robots[j] = ((x+vx)%W,(y+vy)%H,vx,vy)
        i += 1

        if i == 100:
            part1(robots,W,H)

        matches = 0
        for r in robots:
            x,y,vx,vy = r
            if (x,y) in target:
                matches += 1
            else:
                break
        if matches == len(robots):
            answer(i)
            break