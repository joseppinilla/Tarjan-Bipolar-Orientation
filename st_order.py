# Bipolar orientation or st-orientation
# Jose Pinilla

from doubly import LL

def bipolar_orientation(G, s, t, ST_Num=False):
    ''' Get Bipolar orientation from graph

    Params:
        G - Undirected graph adjacency {<node_name>:[<neighbor_nodes>]}
        s - S node
        t - T node
        ST_Num - (bool) True=Return ST-Numbering (dict), False=Return ST/Bipolar Orientation (adj_dict)
    Returns:
        H - Bipolar Orientation graph adjancency {<node_name>:[<neighbor_nodes>]}

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
        for w in G[v]:
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

    # ST-Numbering
    st = {}
    current = 0
    for v in L:
        current += 1
        st[v] = current
    if ST_Num:
        return st

    # ST-Orientation
    H = {}
    for v in G:
        H[v] = []
        for u in G[v]:
            if (st[v]<st[u]):
                H[v] += u
    return H

if __name__ == '__main__':


    import networkx as nx
    import matplotlib.pyplot as plt
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

    st_orient = bipolar_orientation(G.adj, 's', 't')

    H = nx.DiGraph(st_orient)

    nx.draw(H, with_labels=True)
    plt.show()
