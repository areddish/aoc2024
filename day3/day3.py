from aoc_helper import *

MUL = 10
COMMA = 11
LPAREN = 12
RPAREN = 13
NUM = 14
DO = 15
DONT = 16

class Tokenizer:
    def __init__(self, str):
        self.cursor = 0
        self.str = str
        self.n = len(str)
        self.last_found = None

    def next_token(self):
        while self.cursor < self.n:
            ch = self.str[self.cursor]
            if ch == ",":
                self.cursor += 1
                return COMMA, self.cursor - 1, None
            elif ch == "(":
                self.cursor += 1
                return LPAREN, self.cursor - 1, None
            elif ch == ")":
                self.cursor += 1
                return RPAREN, self.cursor - 1, None
            
            num = ""
            while ch.isdigit() and self.cursor < self.n:
                num += ch
                self.cursor += 1
                if self.cursor < self.n:
                    ch = self.str[self.cursor]
            if num:
                assert 1 <= len(num) <= 3
                return NUM, self.cursor - len(num), int(num)
        
            fn_val = [MUL, DONT, DO]
            for i, fn_name in enumerate(["mul", "don't", "do"]):
                if self.str[self.cursor:].startswith(f"{fn_name}("):
                    self.cursor += len(fn_name)
                    return fn_val[i], self.cursor - len(fn_name), None
            self.cursor += 1

#with open("test.txt") as file:
with open("day3.txt") as file:
    lines = file.read().strip()

    tok = Tokenizer(lines)
    tokens = []
    t = tok.next_token()
    while t:
        tokens.append(t)
        t = tok.next_token()

    ans = 0
    ans2 = 0
    enabled = True
    i = 0
    desired = [MUL, LPAREN, NUM, COMMA, NUM, RPAREN]
    while i < len(tokens):
        kind, idx, num = tokens[i]
        if kind == DO and i < len(tokens) - 2 and tokens[i+1][0] == LPAREN and tokens[i+2][0] == RPAREN:
            enabled = True
        elif kind == DONT and i < len(tokens) - 2 and tokens[i+1][0] == LPAREN and tokens[i+2][0] == RPAREN:
            enabled = False
        elif kind == MUL and i < len(tokens) - 6:
            kinds = [t[0] for t in tokens[i:i+6]]
            if kinds == desired:
                ans += tokens[i+2][2] * tokens[i+4][2]
                if enabled:
                    ans2 += tokens[i+2][2] * tokens[i+4][2]
        i += 1
    answer(ans)
    answer(ans2)