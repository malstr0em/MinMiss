from gurobipy import *
import numpy as np
from util import subsequenceslice, down_grade_slice, min_cut_c, count_missesb

iterations = 1

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
        for _ in range(iterations):
            for i in range(number_of_rows-maxrows+1):
                low = i
                high = i+maxrows
                sub = subsequenceslice(cursol[low:high],sequence)
                if(len(sub)!=0):
                    subsol=_dram_optimization(sub, maxrows, number_of_columns)
                    #print(str(count_missesb(subsol,sub))+','+str(count_missesb(cursol[low:high],sub)))
                    if (count_missesb(subsol,sub)<count_missesb(cursol[low:high],sub)):
                        cursol=np.concatenate((cursol[:low],subsol,cursol[high:]))
    return cursol

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
            c[f-1,s-1]+=1
            c[s-1,f-1]+=1
            f=s
        
    print(min_cut_c(c,number_of_columns))


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
