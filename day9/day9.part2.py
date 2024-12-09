from aoc_helper import *

# def print_fd(fd):
#     index = 0
#     for item in fd:
#         id, len, type, moved = item
#         for i in range(len):
#             print("." if type == "FREE" else id, end="")
#     print()


def crc_part2(fd):
    #print_fd(fd)
    result = 0
    index = 0
    for item in fd:
        id, len, type, moved = item
        if type == "FREE":
            index += len
        else:
            for i in range(len):
                result += index * id
                index += 1
    return result

with open("day9.txt") as file:
    s = file.read().strip()
    #s = "2333133121414131402"
    #s = "12345"
    fd = []    
    id = 0
    free_sizes = []
    for i,ch in enumerate(s):
        val = int(ch)
        if i % 2 == 0:
            # id, length, type, has_been_moved
            fd.append([id,val,"FILE",False])
            id += 1   
        else:
            # id, length, type, has_been_moved
            fd.append([-1,val,"FREE",False])
            free_sizes.append(val)

    # part 2
    free_sizes.sort(reverse=True)
    current_free_block_index = 1
    while True:
        # search from right for first to place
        candidate_use_block_index = len(fd)-1
        while fd[candidate_use_block_index][2] != "FILE" or fd[candidate_use_block_index][3]:
            candidate_use_block_index -= 1
        if candidate_use_block_index <= 0:
            break
        #print("Trying to place Block: ", fd[candidate_use_block])

        # now we have a block, look for a free spot
        current_free_block_index = 0
        while current_free_block_index < len(fd) and (fd[current_free_block_index][2] != "FREE" or (fd[current_free_block_index][2] == "FREE" and fd[current_free_block_index][1] < fd[candidate_use_block_index][1])):
            current_free_block_index +=  1
        if current_free_block_index >= len(fd):
            # cand move this one
            fd[candidate_use_block_index][2] = "IMMOVABLE"
            fd[candidate_use_block_index][3] = True
            continue

        #print("Found free block",fd[current_free_block])
        if fd[candidate_use_block_index][3]:
            # already moved before
            break

        if current_free_block_index > candidate_use_block_index:
            # only move things left
            fd[candidate_use_block_index][2] = "IMMOVABLE"
            continue

        # if we find one, slot it in
        if candidate_use_block_index > 0:
            # create the block, handling the 2 cases
            # 1) we full consume the free space
            if fd[candidate_use_block_index][1] == fd[current_free_block_index][1]:
                fd[current_free_block_index][0] = fd[candidate_use_block_index][0]
                fd[current_free_block_index][2] = "FILE"
                fd[current_free_block_index][3] = True
            else:
                # 2) split and insert
                fd.insert(current_free_block_index, [fd[candidate_use_block_index][0], fd[candidate_use_block_index][1], "FILE", True])
                current_free_block_index += 1
                candidate_use_block_index += 1
                fd[current_free_block_index][1] -= fd[candidate_use_block_index][1]

            # free the space we moved
            fd[candidate_use_block_index][0] = -1
            fd[candidate_use_block_index][2] = "FREE"

    answer(crc_part2(fd))

