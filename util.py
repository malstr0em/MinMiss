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

#given a set of sets, considers their size as input and uses a greedy approach to seperate the sets into a partition
def binpacking_k(Adj,k,c):
    return
#given an nx graph does a min cut  
def min_st_cut(gr,s,t):
       
    nx.draw(gr, node_size=500,capacity='capacity')
    plt.show()    
    value, cut = nx.minimum_cut(gr, s, t, capacity='capacity')
    l_1,l_2=cut
        
    return l_1,l_2
    
#return a set of components, if the largest component would be to big it cuts it into two smaller pieces using a min cut
def min_cut_c(Adj,c):

    rows, cols = np.where(Adj != 0)     
    edges = zip(rows.tolist(), cols.tolist())
    edges3 = []
    for e in edges:
        u,v = e
        edges3.append((u,v,Adj[u,v]))
        
    gr = nx.Graph()
    gr.add_weighted_edges_from(edges3,'capacity')
    gr.add_nodes_from(range(len(Adj)))
    
    comps = list(nx.connected_component_subgraphs(gr))
    comps = sorted(comps, key=lambda x:len(x.nodes()), reverse=True)
    result = []
    
    for comp in comps:
        if(c < comp.order()):
            nodes=[i for i,j in comp.nodes(data=True)]

            l_1,l_2 = min_st_cut(comp,nodes[0],nodes[1])
            result=[l_1,l_2]+result
        else:
            result.append(comp.nodes())  
    return result

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
        
