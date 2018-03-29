# Bipolar orientation or st-orientation
# Jose Pinilla

import networkx as nx
import matplotlib.pyplot as plt
from doubly import LL

def bipolar_orientation(G, s, t, ST_Num=False):
    ''' Get Bipolar orientation from graph

    Params:
        G - Undirected graph using networkx
    Returns:
        H - Directed graph with bipolar orientation using networkx

    '''
    # Graph characterization
    current = 0     # iteraion
    p = {}          # node parent
    pre = None      # node preorder
    low = {}        # vertex of smallest number
    preorder = []   # DFS node visit preordering
    ############ Depth First Search
    def dfs(G, v):
        nonlocal current, p, pre, low, preorder
        current += 1
        pre[v] = current
        low[v] = v
        preorder = preorder + [v]
        for w in G.neighbors(v):
            if pre[w] == 0:
                dfs(G, w)
                p[w] = v
                if pre[low[w]] < pre[low[v]]:
                    low[v] = low[w]
            elif (pre[w] < pre[low[v]]):
                low[v] = w

    ############ ST-Numbering
    pre = {v:0 for v in G}
    pre[s] = 1
    current = 1
    dfs(G,t)

    # Doubly linked list
    L = LL()
    nodes = {}
    nodes[s] = L.append(s)
    nodes[t] = L.append(t)

    sign = {}
    plus, minus = True, False
    sign[s] = minus
    for v in preorder[1:]:
        if sign[low[v]] == minus:
            nodes[v] = L.insert_before(nodes[p[v]], v)
            sign[p[v]] = plus
        else:
            nodes[v] = L.insert_after(nodes[p[v]], v)
            sign[p[v]] = minus

    # ST-Orientation
    st = {}
    current = 0
    for v in L:
        current += 1
        st[v] = current

    return st

if __name__ == '__main__':

    # An example from:
    # https://mathscinet.ams.org/mathscinet-getitem?mr=0848212
    edgelist = [
        ('t', 'g'),
        ('h', 'g'),
        ('b', 'f'),
        ('c', 'd'),
        ('f', 'c'),
        ('f', 'g'),
        ('a', 's'),
        ('a', 'b'),
        ('b', 's'),
        ('t', 'h'),
        ('d', 'g'),
        ('d', 's'),
        ('e', 'g'),
        ('c', 's'),
        ('a', 'e'),
        ]

    G = nx.Graph(edgelist)
    nx.draw(G, with_labels=True)
    plt.show()
    st_num = bipolar_orientation(G, 's', 't')
    print(st_num)
    H = nx.DiGraph()
    for v in G:
        for u in G.neighbors(v):
            if (st_num[v]<st_num[u]):
                H.add_edge(v,u)

    nx.draw(H, with_labels=True)
    plt.show()
