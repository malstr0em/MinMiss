import numpy as np
import pylab as plt
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
    if tmp!=[]:
        result.append(tmp)
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

def safeify(partition,Adj,c):
    #find l_1 and l_2,l_3
    l_1=None
    l_=[]
    for l in partition:
        if len(l)>c:
            l_1=l
        else:
           l_.append(l)

    if l_1 is None:
        return partition
    else:
        while len(l_1)>c:
            #search for cheapest node in l_1
            cheapest=l_1[0]
            cheapestC=0
            cheapestP=0
            
            assignment = dict()
            for e in l_1:
                assignment[e]=0
            x=1
            for l_x in l_:
                for e in l_x:
                    assignment[e]=x
                x+=1
                cheapestC_=len(l_)*[0]
            for n in range(len(Adj)):
                edgeweight=Adj[cheapest,n]
                if assignment[n]==0:
                    cheapestC+=edgeweight
                else:
                    cheapestC_[assignment[n]-1]-=edgeweight
            min_=cheapestC_[0]
            for i in range(len(cheapestC_)-1):
                if cheapestC_[i+1]<min_:
                    min_=cheapestC_[i+1]
                    cheapestP=i
            cheapestC+=min_
            
            for i in l_1[1:]:
                cost=0
                cost_=len(l_)*[0]
                costP=0
                for n in range(len(Adj)):
                    edgeweight=Adj[i,n]
                    if assignment[n]==0:
                        cost+=edgeweight
                    else:
                        cost_[assignment[n]-1]-=edgeweight
                costmin_=cost_[0]
                for i in range(len(cost_)-1):
                    if cost_[i+1]<costmin_:
                        costmin_=cost_[i+1]
                        costP=i
                cost+=costmin_
                if cost<cheapestC:
                    cheapest=i
                    cheapestC=cost
                    cheapestP=costP
            #move to l_2
            l_1.remove(cheapest)
            assignment[cheapest]=cheapestP+1
            l_[cheapestP].append(cheapest)
    improvement=True
    if len(l_)==1:
        l_1,l_[0],_=swap(l_1,l_[0],Adj,c)
    if len(l_)==2:
        while improvement:
            improvement=False
            l_1,l_[0],itmp=swap(l_1,l_[0],Adj,c)
            improvement=improvement or itmp
            l_1,l_[1],itmp=swap(l_1,l_[1],Adj,c)
            improvement=improvement or itmp
            l_[0],l_[1],itmp=swap(l_[0],l_[1],Adj,c)
            improvement=improvement or itmp
    return [l_1]+l_

#given a set of sets, considers their size as input and uses a greedy approach to seperate the sets into a partition
def binpacking_k(partition,k,c):
    bins=[]
    for _ in range(k):
        bins.append([])
    for s in partition:
        smallest = 0
        for b in range(k-1):
            if len(bins[b+1])<len(bins[smallest]):
                smallest=b+1
        bins[smallest]+=s
    return bins
#given an nx graph does a min cut  
def min_st_cut(Adj,gr,c):
    print(gr.edges(data=True))
    node = list(gr.nodes())[0]
    bfs = nx.bfs_tree(gr,node)
    queue = [(0,node)]
    while queue != []:
        start=queue.pop(0)
        depth , element = start
        for s in bfs.successors(element):
            queue.append((depth+1,s))
    bfs = nx.bfs_tree(gr,start[1])
    queue = [(0,start[1])]
    while queue != []:
        end=queue.pop(0)
        depth , element = end
        for s in bfs.successors(element):
            queue.append((depth+1,s))
    value, cut = nx.minimum_cut(gr, start[1], end[1])
    l_1,l_2=cut
    l_1=list(l_1)
    l_2=list(l_2)
    if (len(l_2)>len(l_1)):
        l_1,l_2=l_2,l_1
    while len(l_1)>c:
        #search for cheapest node in l_1
        cheapest=None
        cheapestC=np.inf
        assignment = dict()
        for e in l_1:
            assignment[e]=0
        for e in l_2:
            assignment[e]=1
        for i in l_1:
            cost=0
            for n in gr.neighbors(i):
                edgeweight=gr[i][n]['capacity']
                assi=assignment.get(n)
                if not assi is None:
                    if assi==0:
                        cost+=edgeweight
                    else:
                        cost-=edgeweight
            if cost<cheapestC:
                cheapest=i
                cheapestC=cost
        #move to l_2
        l_1.remove(cheapest)
        assignment[cheapest]=1
        l_2.append(cheapest)
    l_1,l_2,_=swap(l_1,l_2,Adj,c)
    print(l_1,l_2)
    nx.draw(gr,with_labels=True)
    plt.show()
    return l_1,l_2

def swap(l_1,l_2,Adj,c):
    changed=False
    nodes=len(Adj)
    improvement=True
    assignment = dict()
    for e in l_1:
        assignment[e]=0
    for e in l_2:
        assignment[e]=1
    space1=c-len(l_1)
    space2=c-len(l_2)
    while improvement:
        improvement=False
        #search for cheapest node in l_1
        cheapest1=None
        cheapestC1=np.inf
        for i in l_1:
            cost=0
            for n in range(nodes):
                edgeweight=Adj[i,n]
                assi=assignment.get(n)
                if not assi is None:
                    if assi==0:
                        cost+=edgeweight
                    else:
                        cost-=edgeweight
            if cost<cheapestC1:
                cheapest1=i
                cheapestC1=cost
        #search for cheapest node in l_2
        cheapest2=None
        cheapestC2=np.inf
        for i in l_2:
            cost=0
            for n in range(nodes):
                edgeweight=Adj[i,n]
                assi=assignment.get(n)
                if not assi is None:
                    if assi==1:
                        cost+=edgeweight
                    else:
                        cost-=edgeweight
            if cost<cheapestC2:
                cheapest2=i
                cheapestC2=cost
        betweenedge = 2*Adj[cheapest1,cheapest2]
        if (cheapestC1<0 and cheapestC2<0 and
            cheapestC1+cheapestC2+betweenedge<0):
            #swap cheapest1 and cheapest2
            l_1.remove(cheapest1)
            l_2.remove(cheapest2)
            l_1.append(cheapest2)
            l_2.append(cheapest1)
            assignment[cheapest1]=1
            assignment[cheapest2]=0
            improvement=True
            changed=True
        elif cheapestC1<0 and space2>0:
            #move to l_2
            l_1.remove(cheapest1)
            assignment[cheapest1]=1
            l_2.append(cheapest1)
            space2-=1
            space1+=1
            improvement=True
            changed=True
        elif cheapestC2<0 and space1>0:
            #move to l_1
            l_2.remove(cheapest2)
            assignment[cheapest2]=0
            l_1.append(cheapest2)
            space1-=1
            space2+=1
            improvement=True
            changed=True
        elif cheapestC1+cheapestC2+betweenedge<0:
            #swap cheapest1 and cheapest2
            l_1.remove(cheapest1)
            l_2.remove(cheapest2)
            l_1.append(cheapest2)
            l_2.append(cheapest1)
            assignment[cheapest1]=1
            assignment[cheapest2]=0
            improvement=True
            changed=True
    return l_1,l_2,changed
    
#return a set of components, if the largest component would be to big it cuts it into two smaller pieces using a min cut
def min_cut_c(Adj,c):
    rows, cols = np.where(Adj != 0)     
    edges = zip(rows.tolist(), cols.tolist())
    edges3 = []
    for e in edges:
        u,v = e
        edges3.append((u,v,Adj[u,v]))  
    gr = nx.Graph()
    gr.add_weighted_edges_from(edges3,weight='capacity')
    gr.add_nodes_from(range(len(Adj)))
    comps = list(nx.connected_component_subgraphs(gr))
    comps = sorted(comps, key=lambda x:len(x.nodes()), reverse=True)
    result = []
    for comp in comps:
        if(c < comp.order()):
            l_1,l_2 = min_st_cut(Adj,comp,c)
            result=[l_1,l_2]+result
        else:
            result.append(list(comp.nodes()))  
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
        
