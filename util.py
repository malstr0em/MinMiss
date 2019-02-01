import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

def subsequence(elements,sequence):
    map = defaultdict(lambda : False)
    for e in np.nditer(np.ndarray.flatten(elements)):
        map[int(e)]=True
    return [s for s in sequence if map[s]]#for e in np.nditer(elements) if e==s]

def subsequenceslice(elements,sequence):
    map = defaultdict(lambda : False)
    for e in np.nditer(np.ndarray.flatten(elements)):
        map[int(e)]=True

    result=[]
    tmp=[]
    for s in sequence:
        if map[s]:
            tmp.append(s)
        else:
            if tmp!=[]:
                result.append(tmp)
            tmp=[]
            
    return result

def down_grade(sequence):
    uniques = np.unique(sequence)
    map = dict()
    for i in range(len(uniques)):
        map[uniques[i]]=i
    return [map[s] for s in sequence],uniques

def down_grade_slice(sequenceslice):
    tmpseq=[]
    for seq in sequenceslice:
        tmpseq += seq
    uniques = np.unique(tmpseq)
    map = dict()
    for i in range(len(uniques)):
        map[uniques[i]]=i
    return [[map[s] for s in k] for k in sequenceslice],uniques

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

def count_misses(solution, sequence):
    s_1=dict()
    for b in range(np.shape(solution)[0]):
        for r in range(np.shape(solution)[1]):
            for c in range(np.shape(solution)[2]):
                s_1[solution[b,r,c]]=(b,r)
    banks=[None]*np.shape(solution)[0]
    count=0
    for s in sequence:
        b,r=s_1[s]
        if banks[b]!=r:
            count+=1
            #print(str(s)+','+str(b)+','+str(r)+','+str(banks[b])+','+str(count))
            banks[b]=r
    return count

def count_missesb(solution, sequence):
    s_1=dict()
    for r in range(np.shape(solution)[0]):
        for c in range(np.shape(solution)[1]):
            s_1[solution[r,c]]=r
    banks=None
    count=0
    for seq in sequence:
        banks=None
        for s in seq:
            r=s_1[s]
            if banks!=r:
                count+=1
                #print(str(s)+','+str(r)+','+str(banks)+','+str(count))
                banks=r
    return count

def count_missesc(solution, sequence):
    return count_misses(np.expand_dims(solution,2),sequence)
        
