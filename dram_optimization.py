from gurobipy import *
from read_sequence import read_sequence
import numpy as np
from util import count_misses
import random as rm
import time as tm

from minRowMissb import dram_optimization as optb
from minRowMissc import dram_optimization as optc

#Calculates a feasible allocation for sequence
#param sequence : list
#param number_of_banks : an integer specifying the number of banks
#param number_of_rows : an integer specifying the number of rows
#param number_of_columns : an integer specifying the number of columns
#return:
#hits : an integer specifying the number of row hits with respect to the returned allocation
#misses : an integer specifying the number of row misses with respect to the returned allocation
#banks : a dictionary specifying to which bank an element is allocated to;
#the keys are the elements of the sequence and the values are the integers
#from 1 up to number_of_banks
#rows : a dictionary specifying to which row an element is allocated to;
#the keys are the elements of the sequence and the values are the integers
#from 1 up to number_of_rows
def dram_optimization(sequence, number_of_banks, number_of_rows, number_of_columns,time=np.inf):
    uniques = np.unique(sequence)
    if len(uniques)>number_of_banks*number_of_rows*number_of_columns:
        return "No feasible Solution"
    glstart=tm.time()
    solutionchain = []
    solutionchain.append(trivial_solutiont(sequence, number_of_banks, number_of_rows, number_of_columns))
    best_solution=dram_optimization_sub(trivial_solution(sequence, number_of_banks, number_of_rows, number_of_columns), sequence, number_of_banks, number_of_rows, number_of_columns,min(time-(tm.time()-glstart),time/4))
    best_misses = count_misses(best_solution, sequence)
    #print(str(best_misses)+100*' ')
    while True:
        solutionchain.append(trivial_solution1(sequence, number_of_banks, number_of_rows, number_of_columns))
        solutionchain.append(trivial_solution2(sequence, number_of_banks, number_of_rows, number_of_columns))
        for solution in solutionchain:
            if tm.time()-glstart>time:
                return 'Best Solution found has '+str(best_misses)+' misses'
            test_solution = dram_optimization_sub(solution, sequence, number_of_banks, number_of_rows, number_of_columns,min(time-(tm.time()-glstart),time/4))
            test_misses = count_misses(test_solution, sequence)
            #print(str(test_misses)+100*' ')
            if test_misses<best_misses:
                best_solution = test_solution
                best_misses = test_misses
        

def dram_optimization_sub(solution, sequence, number_of_banks, number_of_rows, number_of_columns,time=np.inf):
    lstart=tm.time()
    current_solution = solution
    current_misses=count_misses(current_solution,sequence)
    temporary_solution = current_solution
    improvements=True
    while improvements:
        for b in range(number_of_banks):
            if tm.time()-lstart>time:
                return current_solution
            improvements=False
            solpart=optb(current_solution[b],sequence,number_of_rows,number_of_columns,time-(tm.time()-lstart))
            #print(solpart)
            temporary_solution[b]=solpart
            temporary_misses=count_misses(temporary_solution,sequence)
            if(temporary_misses<current_misses):
                improvements=True
                current_solution=temporary_solution
                current_misses=temporary_misses
                #print(current_solution)
                #print(str(current_misses)+100*' ',end='\r')
    return current_solution

def trivial_solution(sequence, number_of_banks, number_of_rows, number_of_columns):
    result = np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    x=0
    for j in range(number_of_rows):
        for k in range(number_of_columns):
            for i in range(number_of_banks):
                if x<len(uniques):
                    result[i,j,k]=uniques[x]
                    x+=1
    return result

def trivial_solutiont(sequence, number_of_banks, number_of_rows, number_of_columns):
    result = np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    x=0
    for k in range(number_of_columns):
        for j in range(number_of_rows):
            for i in range(number_of_banks):
                if x<len(uniques):
                    result[i,j,k]=uniques[x]
                    x+=1
    return result

def trivial_solution1(sequence, number_of_banks, number_of_rows, number_of_columns):
    result = np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    rm.shuffle(uniques)
    x=0
    for k in range(number_of_columns):
        for j in range(number_of_rows):
            for i in range(number_of_banks):
                if x<len(uniques):
                    result[i,j,k]=uniques[x]
                    x+=1
    return result

def trivial_solution2(sequence, number_of_banks, number_of_rows, number_of_columns):
    result = np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    rm.shuffle(uniques)
    x=0
    for j in range(number_of_rows):
        for k in range(number_of_columns):
            for i in range(number_of_banks):
                if x<len(uniques):
                    result[i,j,k]=uniques[x]
                    x+=1
    return result

np.set_printoptions(edgeitems=20,linewidth=250)

maxtime=1*5

sequence1 = read_sequence('Sequences/10_50.seq')
sequence2 = read_sequence('Sequences/99_500.seq')
sequence3 = read_sequence('Sequences/190_950.seq')
sequence4 = read_sequence('Sequences/278_1400.seq')
sequence5 = read_sequence('Sequences/546_2750.seq')
sequence6 = read_sequence('Sequences/792_19024.seq')
sequence7 = read_sequence('Sequences/4224_8402.seq')
sequence8 = read_sequence('Sequences/6121_12155.seq')
sequence9 = read_sequence('Sequences/10336_453358.seq')
sequence10 = read_sequence('Sequences/10400_294960.seq')
sequence11 = read_sequence('Sequences/11296_316796.seq')
sequence12 = read_sequence('Sequences/11520_644456.seq')
sequence13 = read_sequence('Sequences/131072_393216.seq')
sequence14 = read_sequence('Sequences/356400_1198800.seq')

#dram_optimization(sequence14,1,1024,512)

for i in range(3):
    banks=2**i
    print('#'*100)
    print('Sequence1 number of banks:'+str(banks))
    print(dram_optimization(sequence1,banks,4,4,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence2 number of banks:'+str(banks))
    print(dram_optimization(sequence2,banks,16,8,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence3 number of banks:'+str(banks))
    print(dram_optimization(sequence3,banks,16,16,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence4 number of banks:'+str(banks))
    print(dram_optimization(sequence4,banks,32,16,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence5 number of banks:'+str(banks))
    print(dram_optimization(sequence5,banks,32,32,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence6 number of banks:'+str(banks))
    print(dram_optimization(sequence6,banks,32,32,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence7 number of banks:'+str(banks))
    print(dram_optimization(sequence7,banks,128,64,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence8 number of banks:'+str(banks))
    print(dram_optimization(sequence8,banks,128,64,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence9 number of banks:'+str(banks))
    print(dram_optimization(sequence9,banks,128,128,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence10 number of banks:'+str(banks))
    print(dram_optimization(sequence10,banks,128,128,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence11 number of banks:'+str(banks))
    print(dram_optimization(sequence11,banks,128,128,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence12 number of banks:'+str(banks))
    print(dram_optimization(sequence12,banks,128,128,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence13 number of banks:'+str(banks))
    print(dram_optimization(sequence13,banks,128,128,maxtime))
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence14 number of banks:'+str(banks))
    print(dram_optimization(sequence14,banks,1024,512,maxtime))
    #input("Go on? Press Anykey!")
