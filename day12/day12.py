from aoc_helper import *

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)

DIRS = [LEFT, RIGHT, UP, DOWN]

# Group the regions
def group(x,y, G, W, H):
    ch = G[y][x]
    if ch == ".":
        return []
    
    shape = [(x,y)]
    next_ = [(x,y)]
    seen = set(shape)
    while next_:
        x,y = next_.pop()      
        for dx,dy in DIRS:
            tx = x + dx
            ty = y + dy
            if 0 <= tx < W and 0 <= ty < H and G[ty][tx] == ch and (tx,ty) not in seen:
                shape.append((tx,ty))
                next_.append((tx,ty))
                seen.add((tx,ty))
    return shape

def perimeter(nodes):
    p = 0
    for n in nodes:
        for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            tx = n[0] + dx
            ty = n[1] + dy
            if (tx, ty) not in nodes:
                p += 1
    return p

def bbox(hull):
    x = list(hull)
    min_x = x[0][0]
    max_x = x[0][0]
    min_y = x[0][1]
    max_y = x[0][1]

    for n in x[1:]:
        max_x = max(max_x, n[0])
        min_x = min(min_x, n[0])
        max_y = max(max_y, n[1])
        min_y = min(min_y, n[1])
    return (min_x, min_y, max_x, max_y)

# This marks the checked set and sets and flags in the arr to the current
# state of this edge/side
def mark(checked, x,y, move_dir, face_dir, nodes, arr, offset):
    dx,dy = move_dir
    dfx, dfy = face_dir
    tx = x + dx
    ty = y + dy
    fx = tx + dfx
    fy = ty + dfy
    i = 1
    while (tx,ty) in nodes and (fx,fy) not in nodes:
        arr[offset + i*(dx + dy)] = True
        checked.add((tx, ty, (-dfx, -dfy)))
        i += 1
        tx = x + dx*i
        ty = y + dy*i
        fx = tx + dfx
        fy = ty + dfy

# This scans the point cloud in four directions and counts the
# number of edges it sees.
def scan_for_sides(point_cloud):
    checked = set()
    edges = 0

    min_x, min_y, max_x, max_y = bbox(point_cloud)

    # scan horizontally
    left_inside_region = [False] * ((max_y - min_y) + 1)
    right_inside_region = [False] * ((max_y - min_y) + 1)
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x,y,RIGHT) in checked:
                continue
            checked.add((x,y,RIGHT))            
            if (x,y) in point_cloud:
                if not left_inside_region[y - min_y]:
                    edges += 1
                    mark(checked, x,y, UP, LEFT, point_cloud, left_inside_region, y-min_y)
                    mark(checked, x,y, DOWN, LEFT, point_cloud, left_inside_region, y-min_y)
                left_inside_region[y - min_y] = True
            else:
                left_inside_region[y - min_y] = False

    for x in range(max_x, min_x - 1, -1):
        for y in range(min_y, max_y + 1):
            if (x,y,LEFT) in checked:
                continue
            checked.add((x,y,LEFT))
            if (x,y) in point_cloud:
                if not right_inside_region[y - min_y]:
                    edges += 1
                    mark(checked, x,y, UP, RIGHT, point_cloud, right_inside_region, y - min_y)
                    mark(checked, x,y, DOWN, RIGHT, point_cloud, right_inside_region, y - min_y)
                right_inside_region[y - min_y] = True
            else:
                right_inside_region[y - min_y] = False

    # scan vertically
    top_inside_region = [False] * ((max_x - min_x) + 1)
    bottom_inside_region = [False] * ((max_x - min_x) + 1)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x,y,DOWN) in checked:
                continue
            checked.add((x,y,DOWN))
            if (x,y) in point_cloud:
                if not top_inside_region[x- min_x]:
                    edges += 1
                    mark(checked, x,y, LEFT, UP, point_cloud, top_inside_region, x- min_x)
                    mark(checked, x,y, RIGHT, UP, point_cloud, top_inside_region, x- min_x)              
                top_inside_region[x- min_x] = True
            else:
                top_inside_region[x- min_x] = False

    for y in range(max_y, min_y - 1, -1):                
        for x in range(min_x, max_x + 1):
            if (x,y,UP) in checked:
                continue
            checked.add((x,y,UP))
            if (x,y) in point_cloud:
                if not bottom_inside_region[x- min_x]:
                    edges += 1
                    mark(checked, x,y, LEFT, DOWN, point_cloud, bottom_inside_region, x- min_x)
                    mark(checked, x,y, RIGHT, DOWN, point_cloud, bottom_inside_region, x- min_x)                  
                bottom_inside_region[x- min_x] = True
            else:
                bottom_inside_region[x- min_x] = False
    return edges

#with open("test.txt") as file:
#with open("test2.txt") as file:
#with open("test3.txt") as file:
#with open("test4.txt") as file:
#with open("test5.txt") as file:
with open("day12.txt") as file:
    lines = file.read().strip().splitlines()

    G = []
    ans = 0
    ans2 = 0
    for i,l in enumerate(lines):
        row = []
        for j,r in enumerate(l):
            row.append(r)
        G.append(row)
    W = len(G[0])
    H = len(G)

    shapes = []
    for y in range(H):
        for x in range(W):
            shape = group(x,y,G,W,H)
            if shape:
                shapes.append(shape)
            for i,j in shape:
                G[j][i] = "."
            
    #print("\n".join("".join([ch for ch in row]) for row in G))

    for shape in shapes:
        area = len(shape) # we have the point cloud, so the area is # of points
        perim = perimeter(shape)
        side_count = scan_for_sides(shape)
        ans += area * perim
        ans2 += area * side_count
        #print(f"{G[shape[0][1]][shape[0][0]]} {area=} {perim=} {side_count=}")
    answer(ans)
    answer(ans2)
