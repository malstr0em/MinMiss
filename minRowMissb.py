from gurobipy import *
import numpy as np
import random as rm
from util import subsequenceslice, down_grade_slice, min_cut_c, count_missesb,binpacking_k,safeify
import time as tm

#solution of form bank1=[row1,row2,...,rowm]
#row1=[col1,col2,...,colk]
def dram_optimization(solution, sequence, number_of_rows, number_of_columns,time=np.inf):
    #number_of_elements = len(np.unique(sequence))
    #maxvariables = 10000
    #max(int((maxvariables/(number_of_columns*number_of_columns+number_of_columns))**(.5)),2)
    if (number_of_rows<=2):
        return _dram_optimization(sequence, number_of_rows, number_of_columns)
    else:
        cursol=[]
        nullsol=[]
        for row in solution:
            if isnull(row):
                nullsol.append(row)
            else:
                cursol.append(row)
        #print("Trying to find improvement")
        start=tm.time()
        iterator = []
        for i in range(len(cursol)):
            for j in range(len(cursol)):
                if i<j:
                    iterator.append((i,j))
        rm.shuffle(iterator)
        itcount=len(iterator)
        count=0
        for i,j in iterator:
            row1 = cursol[i]
            row2 = cursol[j]
            if len(nullsol)!=0:
                testsol=np.vstack([row1,row2,nullsol[0]])
                sub = subsequenceslice(testsol,sequence)
                if(len(sub)!=0):
                    subsol=_dram_optimization(sub, 3, number_of_columns)
                    if (count_missesb(subsol,sub)<count_missesb(testsol,sub)):
                        cursol[i]=subsol[0]
                        cursol[j]=subsol[1]
                        if not isnull(subsol[2]):
                            cursol.append(subsol[2])
                            nullsol.pop()
                            #print("Finished searching for Improvement")
                            return np.vstack(cursol+nullsol)
            else:
                testsol=np.vstack([row1,row2])
                sub = subsequenceslice(testsol,sequence)
                if(len(sub)!=0):
                    subsol=_dram_optimization(sub, 2, number_of_columns)
                    #print(str(count_missesb(subsol,sub))+','+str(count_missesb(cursol[low:high],sub)))
                    if (count_missesb(subsol,sub)<count_missesb(testsol,sub)):
                        cursol[i]=subsol[0]
                        cursol[j]=subsol[1]
                        if isnull(subsol[1]):
                            #print("Finished searching for Improvement")
                            return np.vstack(cursol+nullsol)
            count+=1
            end=tm.time()
            percent=count/itcount
            if percent!=0:
                timetill=(end-start)/percent
                timetill=timetill-end+start
            else:
                timetill=10**10
            if end-start>time:
                return np.vstack(cursol+nullsol)
            #print(str(int(100*percent))+'%, estimated seconds till completion:'+str(int(timetill+1))+100*' ',end='\r')
    #print("Finished searching for Improvement"+100*' ')
    return np.vstack(cursol+nullsol)

def _dram_optimization(sequenceslice, number_of_rows, number_of_columns):
    #print('*'*100)
    #print('Entered b Optimization')
    #print('Setting up Normal Form')
    down,uniques = down_grade_slice(sequenceslice)
    number_of_elements = len(uniques)

    #print('Counting Misses')
    c=np.zeros((number_of_elements,number_of_elements), int)
    for seq in down:
        f=seq[0]
        for s in seq[1:]:
            if f!=s:
                c[f-1,s-1]+=1
                c[s-1,f-1]+=1
                f=s

    partition=min_cut_c(c,number_of_columns)
    binpack = binpacking_k(partition,number_of_rows,number_of_columns)
    binpack = safeify(binpack,c,number_of_columns)
    binpack=[[uniques[i] for i in b]for b in binpack]
    #print(binpack)
    result = np.zeros((number_of_rows,number_of_columns),dtype=int)
    for i in range(len(binpack)):
        for j in range(len(binpack[i])):
            result[i,j]=binpack[i][j]
    return result

    #print('Setting up b Optimization')
    m = Model();
    m.setParam('OutputFlag',False)
    #print('Adding Variables')
    #x[i,r]=1 object i is in row r
    x = m.addVars(number_of_elements,number_of_rows,vtype=GRB.BINARY,name='x')
    #n[i,j]=c objects i and j have produced c misses
    n = m.addVars(number_of_elements,number_of_elements,name='n')
    #print('Adding Constraints')
    #object i can be in only one row
    m.addConstrs(x.sum(i,'*') == 1 for i in range(number_of_elements))
    #one row can hold at most number_of_columns elements
    m.addConstrs(x.sum('*',r) <= number_of_columns for r in range(number_of_rows))
    #indicator n[i,j] is set to c[i][j] if i and j are in different rows
    m.addConstrs(c[i,j]*(x[i,r] - x[j,r]) - n[i,j] <= 0  for i in range(number_of_elements) for j in range(number_of_elements) for r in range(number_of_rows))
    #count the number of misses twice because n[i][j]=n[j][i]
    #print('Adding Objective')
    m.setObjective(1/2*n.sum('*','*'),GRB.MINIMIZE)
    #print('Optimizing')
    m.optimize()
    x=m.getVars()
    tmp_res = []
    for r in range(number_of_rows):
        tmp_res.append([])
        for i in range(number_of_elements):
            if x[i*number_of_rows+r].x==1:
                tmp_res[r].append(uniques[i])
    result = np.zeros((number_of_rows,number_of_columns),dtype=int)
    for i in range(len(tmp_res)):
        for j in range(len(tmp_res[i])):
            result[i,j]=tmp_res[i][j]
    return result#np.array([x+[0]*(number_of_columns-len(x)) for x in result])

def over2(n):
    return (n*(n+1))/2

def over2m(m,n):
    return over2(m)-over2(m-n)

def isnull(l):
    for i in l:
        if i!=0:
            return False
    return True
