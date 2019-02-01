from gurobipy import *
from read_sequence import read_sequence
import numpy as np
from util import count_misses

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
def dram_optimization(sequence, number_of_banks, number_of_rows, number_of_columns):
    print(sequence)
    current_solution = trivial_solution(sequence,number_of_banks,number_of_rows,number_of_columns)
    current_misses=count_misses(current_solution,sequence)
    print(current_solution)
    print("Trivial solution has:"+str(current_misses)+" misses.")
    if (number_of_banks==1):
        temporary_solution=np.expand_dims(optb(current_solution[0],sequence,number_of_rows,number_of_columns),0)
        temporary_misses=count_misses(temporary_solution,sequence)
        print(temporary_solution)
        if(temporary_misses<current_misses):
            current_solution=temporary_solution
            current_misses=temporary_misses
            print("Better solution found with:"+str(current_misses)+" misses.")
    else:
        print('')
    print("Best solution found has:"+str(current_misses)+" misses.")

def trivial_solution(sequence, number_of_banks, number_of_rows, number_of_columns):
    result = np.zeros((number_of_banks, number_of_rows, number_of_columns),dtype=int)
    uniques = np.unique(sequence)
    x=0
    print('Setting up trivial solution')
    for i in range(number_of_banks):
        for j in range(number_of_rows):
            for k in range(number_of_columns):
                if x<len(uniques):
                    result[i,j,k]=uniques[x]
                    x+=1
    print('Finished setting up trivial solution')
    return result

from minRowMissb import dram_optimization as optb
from minRowMissc import dram_optimization as optc

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

for i in range(1):
    banks=2**i
    print('#'*100)
    print('Sequence1 number of banks:'+str(banks))
    dram_optimization(sequence1,banks,4,4)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence2 number of banks:'+str(banks))
    dram_optimization(sequence2,banks,16,8)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence3 number of banks:'+str(banks))
    dram_optimization(sequence3,banks,16,16)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence4 number of banks:'+str(banks))
    dram_optimization(sequence4,banks,32,16)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence5 number of banks:'+str(banks))
    dram_optimization(sequence5,banks,32,32)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence6 number of banks:'+str(banks))
    dram_optimization(sequence6,banks,32,32)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence7 number of banks:'+str(banks))
    dram_optimization(sequence7,banks,128,64)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence8 number of banks:'+str(banks))
    dram_optimization(sequence8,banks,128,64)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence9 number of banks:'+str(banks))
    dram_optimization(sequence9,banks,128,128)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence10 number of banks:'+str(banks))
    dram_optimization(sequence10,banks,128,128)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence11 number of banks:'+str(banks))
    dram_optimization(sequence11,banks,128,128)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence12 number of banks:'+str(banks))
    dram_optimization(sequence12,banks,128,128)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence13 number of banks:'+str(banks))
    #dram_optimization(sequence13,banks,128,128)
    input("Go on? Press Anykey!")
    print('#'*100)
    print('Sequence14 number of banks:'+str(banks))
    dram_optimization(sequence14,banks,1024,512)
    input("Go on? Press Anykey!")
