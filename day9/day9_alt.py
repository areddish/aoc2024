from aoc_helper import *

def crc(files):
    files.sort(key=lambda file:file[1])
    result = 0
    location = None
    for file in files:
        location = file[1]
        for i in range(file[2]):
            result += file[0] * location
            location += 1
    return result

def get_lists(input_str):
    file_id = 0
    free_id = -1
    file_list = []
    free_list = []
    current_block_loc = 0
    for i,ch in enumerate(input_str):
        val = int(ch)
        if i % 2 == 0:
            # store the id, start_block, len
            file_list.append([file_id,current_block_loc, val])            
            file_id += 1 
        else:
            free_list.append([free_id,current_block_loc,val])
            free_id -= 1
        current_block_loc += val
    return file_list, free_list

with open("day9.txt") as file:
    s = file.read().strip()
    #s = "2333133121414131402"
    #s = "12345"
    file_list, free_list = get_lists(s)
    
    # part 1, single move
    # part 2, defrag?
    for part in [1,2]:
        file_list, free_list = get_lists(s)
        updated_file_list = []
        while file_list:
            # Check each file from the end of the list one by one
            move_candidate = file_list.pop()
            #assert all([free_list[a-1][1] < free_list[a][1] for a in range(1,len(free_list))])
            for free_candidate in free_list:
                # do not move it after
                if move_candidate[1] < free_candidate[1]:
                    break
                # can we move it here?
                move_size = 1 if part == 1 else move_candidate[2]
                if move_size <= free_candidate[2]:
                    if move_candidate[2] > move_size:
                        file_list.append([move_candidate[0], move_candidate[1], move_candidate[2]-1])
                        move_candidate[2] = move_size
                    # update location to consume free space                
                    move_candidate[1] = free_candidate[1]
                    # update location and lengh of free block
                    free_candidate[2] -= move_size
                    free_candidate[1] += move_size
                    break
            updated_file_list.append(move_candidate)
        answer(crc(updated_file_list))
