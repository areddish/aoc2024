from aoc_helper import *
from collections import defaultdict

def mix(value, secret):
    return value ^ secret

def prune(secret):
    return secret % 16777216

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day22.txt") as file:
    lines = file.read().strip().splitlines()
    ans = 0
    sequences_to_try = set()
    N = len(lines)

    # we are going to track all sequences per input secret # and then the profit we have there.
    inputs = []
    for _ in range(N):
        inputs.append(defaultdict(int))

    for line_number, l in enumerate(lines):
        s = int(l)
        ones = [s % 10]   
        for i in range(2000):
            s = mix(s * 64, s)
            s = prune(s)
            s = mix(s // 32, s)
            s = prune(s)
            s = mix(s * 2048, s)
            s = prune(s)
            ones.append(s % 10)
            
        deltas = [ones[i] - ones[i-1] for i in range(1,len(ones))]
        for i in range(len(deltas)-3):
            seq = (deltas[i], deltas[i+1], deltas[i+2], deltas[i+3])
            if seq not in inputs[line_number]:
                inputs[line_number][seq] = ones[i+4]
            # intuition was that we'd have to find things over 7. This was a fortunate guess to
            # eliminate a bunch of searching. After solving the problem, I moved this up to 9
            # for my input. A more comprehensive solution should use all. For my input all
            # sequences to try was 40,951. Using >= 9 whittles that down to 10,000. Although the 
            # runtime isn't too bad either way (difference of seconds)
            if ones[i+4] >= 9:
                sequences_to_try.add(seq)
        ans += s
answer(ans)

# We have an exhaustive list of sequences, try all of thoe across the matrix of
# input profits and maximize.
max_profit = 0
for i,seq in enumerate(sequences_to_try):
    profit = 0
    for j in range(N):
        profit += inputs[j].get(seq, 0)
    max_profit = max(profit, max_profit)
answer(max_profit)