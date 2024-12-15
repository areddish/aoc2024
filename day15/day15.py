from aoc_helper import *

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)

move_to_dir_map = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT,
    "\n": (0,0) 
}

class Warehouse():
    def __init__(self, grid, boxes):
        self.W = len(grid[0])
        self.H = len(grid)
        self.grid = grid
        self.boxes = boxes

    def is_wall(self, x, y):
        return self.grid[y][x] == "#"
    
    def find_box(self, x, y):
        for box in self.boxes:
            if box.occupies(x,y):
                return box
        return None
    
    def get_gps_sum(self):
        ans = 0
        for box in self.boxes:
            ans += 100 * box.y + box.x
        return ans
    
    def print(self, sx, sy):
        box_toggle = True
        for y in range(self.H):
            for x in range(self.W):
                box = self.find_box(x,y)
                if box:
                    if box.size == 2:
                        print("[" if box_toggle else "]", end="")
                    else:
                        print("O", end="")
                    box_toggle = not box_toggle                    
                elif x == sx and y == sy:
                    print("@", end="")
                else:
                    print(grid[y][x],end="")
            print()

class Box():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def try_move(self, dx, dy, warehouse):
        #print(f"Moving {(self.x,self.y)=} in {(dx,dy)=}")
        nx = self.x + dx
        ny = self.y + dy
        
        cascading_moves = set([self])
        for ddx in range(self.size):
            if warehouse.is_wall(nx+ddx,ny):
                return False, []
            collision = warehouse.find_box(nx+ddx, ny)
            if collision == self:
                continue
            if collision:
                can_move, boxes_to_move = collision.try_move(dx,dy,warehouse)
                if not can_move:
                    return False, []
                cascading_moves = cascading_moves.union(boxes_to_move)
        return True, cascading_moves
   
    def occupies(self, x, y):
        if self.y == y:
            for x_offset in range(self.size):
                if self.x + x_offset == x:
                    return True
        return False

    def __hash__(self):
        return (self.x, self.y).__hash__()

#with open("test.txt") as file:
#with open("test2.txt") as file:
#with open("test3.txt") as file:
with open("day15.txt") as file:
    lines = file.read().strip().split("\n\n")
    location = None
    for part in [1,2]:
        grid = []
        all_boxes = []
        for j,line in enumerate(lines[0].split("\n")):
            row = []
            for i,ch in enumerate(line):
                if ch == "@":
                    location = (i*part,j)
                if ch == "O":
                    all_boxes.append(Box(i*part, j, part))
                for _ in range(part):
                    row.append("." if ch != "#" else "#")
            grid.append(row)

        warehouse = Warehouse(grid, all_boxes)
        # print(len(moves))
        # warehouse.print(*location)
        for i, move in enumerate(lines[1]):
            # print(f"Move: {i} is {move=}")
            x, y = location
            dx, dy = move_to_dir_map[move]
            nx = x + dx
            ny = y + dy

            if warehouse.is_wall(nx,ny):
                continue
            else:
                box = warehouse.find_box(nx, ny)
                if box:
                    should_move, cascading_boxes_to_moves = box.try_move(dx, dy, warehouse)
                    if should_move:
                        for box in cascading_boxes_to_moves:
                            box.move(dx,dy)
                    else:
                        continue
            location = (nx,ny)
            # warehouse.print(*location)

        answer(warehouse.get_gps_sum())


## ORIGINAL Part 1
# def move_box(G, boxes, x, y, dir):
#     global bid
#     dx,dy = dir
#     nx = x + dx
#     ny = y + dy
#     if G[ny][nx] == "#":
#         return False
#     if (nx, ny) in boxes:
#         if move_box(G, boxes, nx, ny, dir):
#             boxes.remove((x,y))
#             boxes.append((nx,ny))
#             return True    
#     elif G[ny][nx] == ".":
#         boxes.remove((x,y))
#         boxes.append((nx,ny))
#         return True
#     return False

