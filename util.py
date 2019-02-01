import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

def subsequence(elements,sequence):
    map = defaultdict(lambda : False)
    for e in np.nditer(elements):
        map[int(e)]=True
    return [s for s in sequence if map[s]]#for e in np.nditer(elements) if e==s]

def down_grade(sequence):
    uniques = np.unique(sequence)
    map = dict()
    for i in range(len(uniques)):
        map[uniques[i]]=i
    return [map[s] for s in sequence],uniques

def min_cut(Adj,s,t):
    print(Adj)
    rows, cols = np.where(Adj != 0)
    print(rows)
    print(cols)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500)
    plt.show()

    nx.minimum_cut(gr, s, t, capacity='capacity')

    
    return 