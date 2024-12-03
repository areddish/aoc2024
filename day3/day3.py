from aoc_helper import *

MUL = 10
COMMA = 11
LPAREN = 12
RPAREN = 13
NUM = 14
DO = 15
DONT = 16

class Token:
    def __init__(self, kind, index, val=None):
        self.kind = kind
        self.index = index
        self.val = val

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
                return Token(COMMA, self.cursor - 1)
            elif ch == "(":
                self.cursor += 1
                return Token(LPAREN, self.cursor - 1)
            elif ch == ")":
                self.cursor += 1
                return Token(RPAREN, self.cursor - 1)
            
            num = ""
            while ch.isdigit() and self.cursor < self.n:
                num += ch
                self.cursor += 1
                if self.cursor < self.n:
                    ch = self.str[self.cursor]
            if num:
                assert 1 <= len(num) <= 3
                return Token(NUM, self.cursor - len(num), int(num))
        
            fn_val = [MUL, DONT, DO]
            for i, fn_name in enumerate(["mul", "don't", "do"]):
                if self.str[self.cursor:].startswith(f"{fn_name}("):
                    self.cursor += len(fn_name)
                    return Token(fn_val[i], self.cursor - len(fn_name))
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
    n_desired = len(desired)
    while i < len(tokens):
        kind = tokens[i].kind
        if kind == DO and i < len(tokens) - 2 and tokens[i+1].kind == LPAREN and tokens[i+2].kind == RPAREN:
            enabled = True
        elif kind == DONT and i < len(tokens) - 2 and tokens[i+1].kind == LPAREN and tokens[i+2].kind == RPAREN:
            enabled = False
        elif kind == MUL and i < len(tokens) - n_desired:
            kinds = [t.kind for t in tokens[i:i+n_desired]]
            if kinds == desired:
                ans += tokens[i+2].val * tokens[i+4].val
                if enabled:
                    ans2 += tokens[i+2].val * tokens[i+4].val
        i += 1
    answer(ans)
    answer(ans2)