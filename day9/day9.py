from aoc_helper import *

def crc(line):
    result = 0
    for i,n in enumerate(line):
        result += i * n
    return result

with open("day9.txt") as file:
    s = file.read().strip()
    #s = "2333133121414131402"
    #s = "12345"
    fd = []    
    id = 0
    next_free_block = -1
    next_use_block = 0
    for i,ch in enumerate(s):
        if i % 2 == 0:
            fd.append([id,int(ch)])
            id += 1   
            next_use_block = i         
        else:
            fd.append(int(ch))
            if next_free_block == -1:
                next_free_block = i

    new = []
    for i in range(fd[0][1]):
        new.append(fd[0][0])
    while True:
        id, count = fd[next_use_block]
        while count and fd[next_free_block]:
            count -= 1
            new.append(fd[next_use_block][0])
            fd[next_free_block] -= 1
            fd[next_use_block][1] -= 1

        if count > 0:
            # find new free block
            while fd[next_free_block+1][1]:
                new.append(fd[next_free_block+1][0])
                fd[next_free_block+1][1] -= 1
            next_free_block += 2
        else:
            # find next use block
            next_use_block -= 2

        if fd[next_use_block][1] == 0:
            break

    #print (new)
    answer(crc(new))