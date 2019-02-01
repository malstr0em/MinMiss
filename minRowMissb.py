from gurobipy import *
import numpy as np
from util import subsequence, down_grade

#solution of form bank1=[row1,row2,...,rowm]
#row1=[col1,col2,...,colk]
def dram_optimization(solution, sequence, number_of_rows, number_of_columns):
    #number_of_elements = len(np.unique(sequence))
    #maxvariables = 10000
    maxrows = 3#max(int((maxvariables/(number_of_columns*number_of_columns+number_of_columns))**(.5)),2)
    cursol=solution
    if (number_of_rows<=maxrows):
        return _dram_optimization(sequence, number_of_rows, number_of_columns)
    else:
        for i in range(number_of_rows-maxrows+1):
            low = i
            high = i+maxrows
            sub = subsequence(cursol[low:high],sequence)
            if(len(sub)!=0):
                subsol=_dram_optimization(sub, maxrows, number_of_columns)
                cursol=np.concatenate((cursol[:low],subsol,cursol[high+1:]))
    return cursol

def _dram_optimization(sequence, number_of_rows, number_of_columns):
    print('*'*100)
    print('Entered b Optimization')
    print('Setting up Normal Form')
    down,uniques = down_grade(sequence)
    number_of_elements = len(uniques)

    print('Counting Misses')
    c=[]
    for i in range(number_of_elements):
        c.append([])
        for j in range(number_of_elements):
            c[i].append(0)
    f=down[0]
    for s in down[1:]:
        c[f-1][s-1]+=1
        c[s-1][f-1]+=1
        f=s

    print('Setting up b Optimization')
    m = Model();
    #m.setParam('OutputFlag',False)
    print('Adding Variables')
    #x[i,r]=1 object i is in row r
    x = m.addVars(number_of_elements,number_of_rows,vtype=GRB.BINARY,name='x')
    #n[i,j]=c objects i and j have produced c misses
    n = m.addVars(number_of_elements,number_of_elements,name='n')
    print('Adding Constraints')
    #object i can be in only one row
    m.addConstrs(x.sum(i,'*') == 1 for i in range(number_of_elements))
    #one row can hold at most number_of_columns elements
    m.addConstrs(x.sum('*',r) <= number_of_columns for r in range(number_of_rows))
    #indicator n[i,j] is set to c[i][j] if i and j are in different rows
    m.addConstrs(c[i][j]*(x[i,r] - x[j,r]) - n[i,j] <= 0  for i in range(number_of_elements) for j in range(number_of_elements) for r in range(number_of_rows))
    #count the number of misses twice because n[i][j]=n[j][i]
    print('Adding Objective')
    m.setObjective(1/2*n.sum('*','*'),GRB.MINIMIZE)
    print('Optimizing')
    m.optimize()
    x=m.getVars()
    result = []
    for r in range(number_of_rows):
        result.append([])
        for i in range(number_of_elements):
            if x[i*number_of_rows+r].x==1:
                result[r].append(uniques[i])
                
    return np.array([x+[0]*(number_of_columns-len(x)) for x in result])
