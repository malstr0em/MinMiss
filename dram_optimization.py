from gurobipy import *
from read_sequence import read_sequence
import numpy as np
from util import count_misses,subsequence,mapc
import random as rm
import time as tm
import math

from minRowMissb import dram_optimization as optb
from minRowMissc import dram_optimization as optc

'''Calculates a feasible allocation for sequence
param sequence : list
param number_of_banks : an integer specifying the number of banks
param number_of_rows : an integer specifying the number of rows
param number_of_columns : an integer specifying the number of columns
return:
hits : an integer specifying the number of row hits with respect to the returned allocation
misses : an integer specifying the number of row misses with respect to the returned allocation
banks : a dictionary specifying to which bank an element is allocated to;
the keys are the elements of the sequence and the values are the integers
from 1 up to number_of_banks
rows : a dictionary specifying to which row an element is allocated to;
the keys are the elements of the sequence and the values are the integers
from 1 up to number_of_rows
time : (optional) sets the maximum amount of seconds for finding a solution. Default is 5 minutes
'''
def dram_optimization(sequence, number_of_banks, number_of_rows, number_of_columns,time=300):
    timemeasure = tm.time()
    uniques = np.unique(sequence)
    if len(uniques)>number_of_banks*number_of_rows*number_of_columns:
        return -np.inf,np.inf,dict(),dict()
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
                #print ('Best Solution found has '+str(best_misses)+' misses')
                misses = count_misses(best_solution, sequence)
                hits = len(sequence)-misses
                banks = dict()
                rows = dict()
                for b in range(len(best_solution)):
                    for r in range(len(best_solution[b])):
                        for c in best_solution[b][r]:
                            banks[c]=b
                            rows[c]=r
                return hits,misses,banks,rows
                
            test_solution = dram_optimization_sub(solution, sequence, number_of_banks, number_of_rows, number_of_columns,min(time-(tm.time()-glstart),time/4))
            test_misses = count_misses(test_solution, sequence)
            #print(str(test_misses)+100*' ')
            if test_misses<best_misses:
                best_solution = test_solution
                best_misses = test_misses
    misses = count_misses(best_solution, sequence)
    hits = len(sequence)-misses
    banks = dict()
    rows = dict()
    for b in range(len(best_solution)):
        for r in range(len(best_solution[b])):
            for c in best_solution[b][r]:
                banks[c]=b
                rows[c]=r
    return hits,misses,banks,rows

def dram_optimization_sub(solution, sequence, number_of_banks, number_of_rows, number_of_columns,time=np.inf):
    lstart=tm.time()
    current_solution = solution
    current_misses=count_misses(current_solution,sequence)
    temporary_solution = current_solution
    improvements=True
    if number_of_banks>1:
        while improvements:
            if tm.time()-lstart>time:
                current_solution_tmp=np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
                x=0
                struct = []
                for r in range(number_of_rows):
                    for b in range(number_of_banks):
                        struct.append((b,x))
                    x+=1
                for i,t in zip(current_solution[0],struct):
                    b,x=t
                    current_solution_tmp[b,x]=i
                current_solution=current_solution_tmp
                return current_solution
            improvements=False
            solpart=optb(current_solution[0],subsequence(current_solution[0],sequence),len(current_solution[0]),number_of_columns,time-(tm.time()-lstart))
            temporary_solution[0]=solpart
            temporary_misses=count_misses(temporary_solution,sequence)
            if(temporary_misses<current_misses):
                improvements=True
                current_solution=temporary_solution
                current_misses=temporary_misses
        current_solution_tmp=np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
        x=0
        struct = []
        for r in range(number_of_rows):
            for b in range(number_of_banks):
                struct.append((b,x))
            x+=1
        for i,t in zip(current_solution[0],struct):
            b,x=t
            current_solution_tmp[b,x]=i
        current_solution=current_solution_tmp
        current_solution_mapped, sequence_mapped, mapping = mapc(current_solution,sequence)
        current_solution_mapped=optc(current_solution_mapped,sequence_mapped,number_of_banks,number_of_rows,time-(tm.time()-lstart))
        temporary_solution=np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
        for b in range(len(temporary_solution)):
            for r in range(len(temporary_solution[b])):
                temporary_solution[b,r]=mapping[current_solution_mapped[b,r]]
        temporary_misses=count_misses(temporary_solution,sequence)
        if(temporary_misses<current_misses):
            current_solution=temporary_solution
            current_misses=temporary_misses
    improvements=True
    while improvements:
        improvements=False
        for b in range(number_of_banks):
            if tm.time()-lstart>time:
                return current_solution
            temporary_solution=current_solution
            solpart=optb(current_solution[b],subsequence(current_solution[b],sequence),number_of_rows,number_of_columns,time-(tm.time()-lstart))
            temporary_solution[b]=solpart
            temporary_misses=count_misses(temporary_solution,sequence)
            if(temporary_misses<current_misses):
                improvements=True
                current_solution=temporary_solution
                current_misses=temporary_misses

        if not improvements and number_of_banks>1:
            current_solution_mapped, sequence_mapped, mapping = mapc(current_solution,sequence)
            current_solution_mapped=optc(current_solution_mapped,sequence_mapped,number_of_banks,number_of_rows,time-(tm.time()-lstart))
            temporary_solution=np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
            for b in range(len(temporary_solution)):
                for r in range(len(temporary_solution[b])):
                    temporary_solution[b,r]=mapping[current_solution_mapped[b,r]]
            temporary_misses=count_misses(temporary_solution,sequence)
            if(temporary_misses<current_misses):
                improvements=True
                current_solution=temporary_solution
                current_misses=temporary_misses
    return current_solution

def dram_optimization_wrapper(sequence, number_of_banks, number_of_rows, number_of_columns,time=np.inf):
    epsilon=2
    timemeasure=tm.time()
    hits,misses,banks,rows=dram_optimization(sequence, number_of_banks, number_of_rows, number_of_columns,time-epsilon)
    print(str(round(tm.time()-timemeasure,2))+' seconds elapsed. Solution has '+str(misses)+' misses.')

def trivial_solution(sequence, number_of_banks, number_of_rows, number_of_columns):
    number_of_rows_initial=number_of_banks*number_of_rows
    result = np.zeros((1, number_of_rows_initial, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    x=0
    for j in range(number_of_rows_initial):
        for k in range(number_of_columns):
                if x<len(uniques):
                    result[0,j,k]=uniques[x]
                    x+=1
    return result

def trivial_solutiont(sequence, number_of_banks, number_of_rows, number_of_columns):
    number_of_rows_initial=number_of_banks*number_of_rows
    result = np.zeros((1, number_of_rows_initial, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    x=0
    for k in range(number_of_columns):
        for j in range(number_of_rows_initial):
                if x<len(uniques):
                    result[0,j,k]=uniques[x]
                    x+=1
    return result

def trivial_solution1(sequence, number_of_banks, number_of_rows, number_of_columns):
    number_of_rows_initial=number_of_banks*number_of_rows
    result = np.zeros((1, number_of_rows_initial, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    rm.shuffle(uniques)
    x=0
    for j in range(number_of_rows_initial):
        for k in range(number_of_columns):
                if x<len(uniques):
                    result[0,j,k]=uniques[x]
                    x+=1
    return result

def trivial_solution2(sequence, number_of_banks, number_of_rows, number_of_columns):
    number_of_rows_initial=number_of_banks*number_of_rows
    result = np.zeros((1, number_of_rows_initial, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    rm.shuffle(uniques)
    x=0
    for k in range(number_of_columns):
        for j in range(number_of_rows_initial):
                if x<len(uniques):
                    result[0,j,k]=uniques[x]
                    x+=1
    return result

#np.set_printoptions(edgeitems=20,linewidth=250)

import argparse
parser = argparse.ArgumentParser(description=("Solves multiple instances of the Minimum Row Misses Problem,"
                                 "without guarantees for optimality."))
parser.add_argument('-t', '--time', default=60, type=int,
                        help="Maximum amount of time for each solution search")

args = parser.parse_args()

maxtime=args.time

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

print('Do you realize this file now has options? try --help for options')

for i in range(3):
    banks=2**i
    print('#'*100)
    print('Sequence1 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence1,banks,4,4,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence2 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence2,banks,16,8,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence3 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence3,banks,16,16,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence4 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence4,banks,32,16,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence5 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence5,banks,32,32,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence6 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence6,banks,32,32,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence7 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence7,banks,128,64,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence8 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence8,banks,128,64,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence9 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence9,banks,128,128,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence10 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence10,banks,128,128,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence11 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence11,banks,128,128,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence12 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence12,banks,128,128,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence13 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence13,banks,128,128,maxtime)
    #input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence14 number of banks:'+str(banks))
    dram_optimization_wrapper(sequence14,banks,1024,512,maxtime)
    #input("Go on? Press Anykey!")
