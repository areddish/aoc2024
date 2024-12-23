from aoc_helper import *
from collections import defaultdict
import networkx as nx

#with open("test.txt") as file:
with open("day23.txt") as file:
    lines = file.read().strip().splitlines()
    connections = defaultdict(list)
    g = nx.Graph()
    for line in lines:
        src, dst = line.split("-")
        g.add_node(src)
        g.add_node(dst)
        g.add_edge(src,dst)
        g.add_edge(dst,src)
        connections[src].append(dst)
        connections[dst].append(src)

    trips = set()
    for a in connections:
        for b in connections[a]:
            for c in connections[b]:
                if a == b or a == c:
                    continue
                if b == a or b == c:
                    continue
                if "t" not in a[0]+b[0]+c[0]:
                    continue
                a_connected = (a in connections[b] and a in connections[c])                
                b_connected = (b in connections[a] and b in connections[c])
                c_connected = (c in connections[a] and c in connections[b])
                if a_connected and b_connected and c_connected:
                    assert nx.is_connected(g.subgraph([a,b,c]))
                    trips.add(tuple(sorted((a,b,c))))

    answer(len(trips))

    # easymode: use networkx to find a clique - which is a fully connected subgraph
    answer(",".join(sorted(max(nx.find_cliques(g), key=len))))

    # def fully_connected(nodes, connections):
    #     for i, n in enumerate(nodes):
    #         for j, n2 in enumerate(nodes):
    #             if i == j:
    #                 continue
    #             if n not in connections[n2]:
    #                 return False
    #     return True

    
    # # for each triplet, try to expand
    # added = True
    # while added:
    #     new_set = set()
    #     for indext_t, t in enumerate(trips):
    #         added = False
    #         for node in connections:
    #             if node in t:
    #                 continue
    #             if fully_connected([*t, node], connections):
    #             #if nx.is_connected(g.subgraph([*t, node])):
    #                 print([*t, node])
    #                 new_set.add(tuple([*t, node]))
    #                 added = True
    #     trips = new_set
