from aoc_helper import *
import random

def swap(r1, r2, dep_graph):
    temp = dep_graph[r1]
    dep_graph[r1] = dep_graph[r2]
    dep_graph[r2] = temp    

# used for printing out the rules, started to do visual inspection but didn't
# def expand_rule(r, dep_graph):
#     result = ""
#     r1, op, r2 = dep_graph[r]
#     if r1.startswith("x") or r1.startswith("y"):
#         result += r1
#     else:
#         result += expand_rule(r1, dep_graph)
#     result += " "
#     result += op
#     result += " " 
#     if r2.startswith("x") or r2.startswith("y"):
#         result += r2 + " "
#     else:
#         result += expand_rule(r2, dep_graph)
#     return result

# get's all dependent rule names   
def get_all_inputs(r, dep_graph):
    result = set()
    r1, op, r2 = dep_graph[r]
    if not r1.startswith("x") and not r1.startswith("y"):
        result.add(r1)
        result = result.union(get_all_inputs(r1, dep_graph))          
    if not r2.startswith("x") and not r2.startswith("y"):
        result.add(r2)        
        result = result.union(get_all_inputs(r2, dep_graph))
    return result

def wires2int(z):
    num = 0
    for i,n in enumerate(z):
        num += 2**i * n
    return num

def int2wires(n, num_bits=46):
    barray = [int(bit) for bit in reversed(list(bin(n))[2:])]
    i = len(barray)
    while i < num_bits:
        barray.append(0)
        i += 1
    return barray

ans = 0
ans2 = 0
#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day24.txt") as file:
    connections, commands = file.read().strip().split("\n\n")

    starting_wire_outputs = {}
    for c in connections.split("\n"):
        r, v = c.split(": ")
        v = int(v)
        starting_wire_outputs[r] = v

    # Input was in order, but just to be safe sort and
    # find out what x & y are
    x = []
    y = []
    sorted_keys = sorted(starting_wire_outputs.keys())
    for k in sorted_keys:
        if k.startswith("x"):
            x.append(starting_wire_outputs[k])
        if k.startswith("y"):            
            y.append(starting_wire_outputs[k])

    # For part 2, we need to know what the goal is that we are adding to get.
    goal = [int(bit) for bit in reversed(list(bin(wires2int(x) + wires2int(y)))[2:])]
    #print(wires2int(x), wires2int(y), wires2int(x) + wires2int(y))

    dep_graph = {}
    for cmd in commands.split("\n"):
        parts = cmd.split(" ")
        r1 = parts[0]
        r2 = parts[2]
        op = parts[1]
        dep = parts[4]
        assert dep not in dep_graph
        dep_graph[dep] = [r1, op, r2]

    def add(a, b, dep_graph, num_bits = 45):
        regs = {}
        i = 0
        for x,y in zip(int2wires(a,num_bits), int2wires(b,num_bits)):
            regs[f"x{i:02d}"] = x
            regs[f"y{i:02d}"] = y
            i += 1
        #assert regs == starting_registers
        return run(regs, dep_graph)
    
    def run(initial_registers, dep_graph):
        registers = initial_registers.copy()
        settled = False
        iters = 0
        while not settled and iters < 50:
            settled = True
            for dst, eq in dep_graph.items():
                r1, op, r2 = eq
                r1 = registers.get(r1, None)
                r2 = registers.get(r2, None)
                if r1 == None or r2 == None:
                    settled = False
                else:
                    val = None
                    if op == "AND":
                        val = r1 & r2
                    elif op == "XOR":
                        val = r1 ^ r2
                    elif op == "OR":
                        val = r1 | r2
                    else:
                        assert False, f"Don't know how to deal with {op}"
                    registers[dst] = val
            iters += 1
        z = []
        sorted_keys = sorted(registers.keys())
        for k in sorted_keys:
            if k.startswith("z"):
                z.append(registers[k])
        return z
    
    assert run(starting_wire_outputs, dep_graph) == add(wires2int(x), wires2int(y), dep_graph)
    z = run(starting_wire_outputs, dep_graph)
    print(z, wires2int(x)+ wires2int(y))
    answer(wires2int(z))

    # For part 2 we go through and add 2**i + 0 and see which don't produce the correct
    # output. This indicates which bits are off. This problem input is structured such
    # that only 4 bits are off so we find those.
    incorrect_wires  = []
    for i in range(len(x)):
        g = int2wires(2**i)
        z = add(2**i, 0, dep_graph)
        gn = wires2int(g)
        zn = wires2int(z)
        if gn != zn:
            # didn't match, find the bits that don't match and store them
            g0_pair = 0
            while zn > 1:
                zn /= 2
                g0_pair += 1
            #swap(f"z{i:02d}", f"z{j:02d}", dep_graph)
            incorrect_wires.append((f"z{i:02d}", f"z{g0_pair:02d}"))

    assert len(incorrect_wires) == 4, "Found too many pairs"

    test_suite = [(wires2int(x),wires2int(y),goal)]
    random.seed(12242024)
    for _ in range(25):
        a = random.randint(2**2, 2**45)
        b = random.randint(2**2, 2**45)
        test_suite.append((a, b,int2wires(a+b)))

    # Now for each par in incorrect_wires we enumerate all possible connections
    # of inputs and record the ones that swapping fixes that bit only.
    groups = [[], [], [], []]
    #ans2 = set()
    i = 0
    for output1, output2 in incorrect_wires:
        # the bit to check is encoded in the z output
        power = int(output1[1:])
        output1_candidates = [r for r in set([output1]).union(get_all_inputs(output1, dep_graph))]
        output2_candidates = [r for r in set([output2]).union(get_all_inputs(output2, dep_graph))]
        for r1 in output1_candidates:
            for r2 in output2_candidates:
                # Check if this one is broken
                if not add(2**power, 0, dep_graph) == int2wires(2**power):
                    # If so, swap and record if it's fixed. This isn't the final solution
                    # it's a possible solution.
                    swap(r1, r2, dep_graph)
                    # FUTURE: could probably determine answer here by testing against test_suite
                    # and all([add(a,b,dep_graph)==a_plus_b for a,b,a_plus_b in test_suite]):
                    if add(2**power, 0, dep_graph) == int2wires(2**power):
                        groups[i].append((r1,r2))
                        print("Found:",r1,r2)                        
                    # undo it so we don't modify the later bits                        
                    swap(r2,r1, dep_graph)
        i+=1
    assert len(groups) == 4, "Wrong number of pairs"

    # We know there are four pairs, can brute force this now.
    for g0_pair in groups[0]:
        for g1_pair in groups[1]:
            for g2_pair in groups[2]:
                for g3_pair in groups[3]:
                    swap(*g0_pair, dep_graph)
                    swap(*g1_pair, dep_graph)
                    swap(*g2_pair, dep_graph)
                    swap(*g3_pair, dep_graph)                    
                    if all([add(a,b,dep_graph)==a_plus_b for a,b,a_plus_b in test_suite]):
                        answer(",".join(sorted(g0_pair + g1_pair + g2_pair + g3_pair)))
                        exit()
                    swap(*g0_pair, dep_graph)
                    swap(*g1_pair, dep_graph)
                    swap(*g2_pair, dep_graph)
                    swap(*g3_pair, dep_graph)  
