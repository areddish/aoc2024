from aoc_helper import *

DEBUG = False
class VM:
    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.IP = 0
        self.output = []
        # Op Code to FN
        self.fn = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

    def adv(self, combo, literal):
        if DEBUG:
            print("adv", combo)
        self.A = int(self.A / (2**combo))

    def bxl(self, combo, literal):
        if DEBUG:
            print("bxl", literal)
        self.B = self.B ^ literal

    def bst(self, combo, literal):
        if DEBUG:
            print("bst", combo)
        self.B = combo % 8
    
    def jnz(self, combo, literal):
        if DEBUG:
            print("jnz", literal)
        if self.A != 0:
            self.IP = literal
    
    def bxc(self, combo, literal):
        if DEBUG:
            print("bxc", combo)
        self.B = self.C ^ self.B
    
    def out(self, combo, literal):
        if DEBUG:
            print("out", combo)
        self.output.append(combo % 8)
        #print(",".join([str(x) for x in self.output]))
    
    def bdv(self, combo, literal):
        if DEBUG:
            print("bdv", combo)
        self.B = int(self.A / (2**combo))

    def cdv(self, combo, literal):
        if DEBUG:
            print("cdv", combo)
        self.C = int(self.A / (2**combo))

    def run_with_init(self,A,B,C):
        self.A = A
        self.B = B
        self.C = C
        self.output = []
        self.IP = 0
        self.run()

    def run(self):
        while self.IP < len(self.program) - 1:
            fn = self.fn[self.program[self.IP]]
            self.IP += 1
            literal = self.program[self.IP]
            combo = self.program[self.IP]
            if combo == 4:
                combo = self.A
            elif combo == 5:
                combo = self.B
            elif combo == 6:
                combo = self.C
            self.IP += 1
            # Modify IP before call to fn so that jumps
            # or IP modifying operations work.
            fn(combo, literal)
            # print(self.IP)

ans = 0
ans2 = 0

# ## Test cases
# t1 = VM(0,0,9,[2,6])
# t1.run()
# assert t1.B == 1, "If register C contains 9, the program 2,6 would set register B to 1."

# t1 = VM(10,0,9,[5,0,5,1,5,4 ])
# t1.run()
# assert t1.output == [0,1,2], "If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2."

# t1 = VM(2024,29,0,[0,1,5,4,3,0 ])
# t1.run()
# assert t1.A == 0 and [int(x) for x in t1.output] == [4,2,5,6,7,7,7,7,3,1,0], "If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A."
# t1 = VM(0,29,0,[1,7 ])
# t1.run()
# assert t1.B == 26, "If register B contains 29, the program 1,7 would set register B to 26."
# t1 = VM(0,2024,43690,[4,0  ])
# t1.run()
# assert t1.B == 44354, "IIf register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354."

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day17.txt") as file:
    lines = file.read().strip().splitlines()
    A = int(lines[0].split(": ")[1])
    B = int(lines[1].split(": ")[1])
    C = int(lines[2].split(": ")[1])
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]
    vm = VM(A,B,C,program)
    vm.run()
    answer(",".join([str(n) for n in vm.output]))

    # By printing out the opcodes and then converting them to python the actual program looks like
    # this, combining some lines into one:
    #   while A != 0
    #      B = (A % 8) ^ 1
    #      C = int((A / 2**B)) %8 
    #      B = (B ^ 5) ^ C
    #      A = int(A/8)
    #   OUT.append(B%8)
    #
    # It's observed the A register is /8 each iteration and given the 3 bit restriction, we can
    # conclude the output is encoded as octal to the register. Each iteration is just a transformation
    # on the digit. Thus we have LEN(PROGRAM) digits with each digit being 0-7. So try them all DFS style
    # until we find the answer. If mulitple answers, take the minimum since it wants lowest value.

    NO_ANSWER = 1e19 # this number is larger than any possible solution
    def find_A_for_program(vm, current_index, A_so_far, pow = 15):
        answers = [NO_ANSWER]
        # Exit conditions
        if current_index > len(vm.program) or pow < 0:
            return NO_ANSWER

        # There's an opposite relationship. The higher order bits of A will produce
        # the later digits of program.
        REVERSED_GOAL = list(reversed(vm.program))       
        for j in range(8):
            A = j*8**pow + A_so_far
            if A == 0:
                continue
            vm.run_with_init(A,0,0)
            if vm.output == vm.program:
                # Could probably just early out here and stop the program.
                return A

            # If the translation matches the desired digit, we have a candidate
            # value for this coefficent/octal based digit. Continue exploring here.
            if vm.output[pow] == REVERSED_GOAL[current_index]:
                answers.append(find_A_for_program(vm, current_index+1, A, pow-1))
            
        return min(answers)

    answer(find_A_for_program(VM(0,0,0,program), 0, 0, 15))