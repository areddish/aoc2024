from aoc_helper import *

def safe(val,lim):
    return 0 <= val < lim

def find_words(board, x, y, words = ["XMAS", "SAMX"]):
    limit = len(words[0]) - 1
    found = 0
    # don't need to look in other directions as they'll create duplicates since we're checking both words
    for dx,dy in [(1,0),(0,1),(1,1),(1,-1)]: 
        if safe(x+dx*limit, W) and safe(y+dy*limit, H):
            if "".join([board[y+dy*i][x+dx*i] for i in range(limit+1)]) in words:
                found += 1
    return found

def check_mas_kernel(board,x,y):
    word1 = ""
    word2 = ""
    for offset in range(3):
        word1 += board[y+offset][x+offset]
        word2 += board[y+offset][x+2-offset]
    return (word1 == "SAM" or word1 == "MAS") and (word2 == "SAM" or word2 == "MAS")

#with open("test.txt") as file:
with open("day4.txt") as file:
    board = file.read().strip().splitlines()
    ans = 0
    ans2 = 0

    W = len(board[0])
    H = len(board)
    
    for y in range(H):
        for x in range(W):
            ans += find_words(board,x,y)
            if safe(x+2, W) and safe(y+2, H) and check_mas_kernel(board,x,y):
                ans2 += 1

    answer(ans)
    answer(ans2)
