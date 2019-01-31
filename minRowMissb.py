from gurobipy import *
import numpy as np

def dram_optimization(solution, sequence, number_of_rows, number_of_columns):
    maxvariables = 10000

    dram_optimization(sequence, number_of_rows, number_of_columns)
    
    print('x')

def dram_optimization(sequence, number_of_rows, number_of_columns):
    print(sequence)
    number_of_elements = len(np.unique(sequence))
    
    c=[]
    for i in range(number_of_elements):
        c.append([])
        for j in range(number_of_elements):
            c[i].append(0)
    f=sequence[0]
    for s in sequence[1:]:
        c[f-1][s-1]+=1
        c[s-1][f-1]+=1
        f=s
    
    m = Model();
    #x[i,r]=1 object i is in row r
    x = m.addVars(number_of_elements,number_of_rows,vtype=GRB.BINARY)
    #n[i,j]=c objects i and j have produced c misses
    n = m.addVars(number_of_elements,number_of_elements)
    #object i can be in only one row
    m.addConstrs(x.sum(i,'*') == 1 for i in range(number_of_elements))
    #one row can hold at most number_of_columns elements
    m.addConstrs(x.sum('*',r) <= number_of_columns for r in range(number_of_rows))
    #indicator n[i,j] is set to c[i][j] if i and j are in different rows
    m.addConstrs(c[i][j]*(x[i,r] - x[j,r] - n[i,j]) <= 0  for i in range(number_of_elements) for j in range(number_of_elements) for r in range(number_of_rows))
    #count the number of misses twice because n[i][j]=n[j][i]
    m.setObjective(1/2*n.sum('*','*'))
    m.optimize()

    print('b=1 finished an execution')
