from gurobipy import *
from read_sequence import read_sequence
import numpy as np

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
    ts = trivial_solution(sequence,number_of_banks,number_of_rows,number_of_columns)
    if (number_of_banks==1):
        print(optb(ts[0],sequence,number_of_rows,number_of_columns))
    else:
        print(ts)

def trivial_solution(sequence, number_of_banks, number_of_rows, number_of_columns):
    result = np.ndarray((number_of_banks, number_of_rows, number_of_columns))
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

dram_optimization(sequence14,1,1024,512)

for i in range(1):
    banks=2**i
    print('#'*100)
    print('Sequence1 number of banks:'+str(banks))
    dram_optimization(sequence1,banks,4,4)
    print('#'*100)
    print('Sequence2 number of banks:'+str(banks))
    dram_optimization(sequence2,banks,16,8)
    print('#'*100)
    print('Sequence3 number of banks:'+str(banks))
    dram_optimization(sequence3,banks,16,16)
    print('#'*100)
    print('Sequence4 number of banks:'+str(banks))
    dram_optimization(sequence4,banks,32,16)
    print('#'*100)
    print('Sequence5 number of banks:'+str(banks))
    dram_optimization(sequence5,banks,32,32)
    print('#'*100)
    print('Sequence6 number of banks:'+str(banks))
    dram_optimization(sequence6,banks,32,32)
    print('#'*100)
    print('Sequence7 number of banks:'+str(banks))
    dram_optimization(sequence7,banks,128,64)
    print('#'*100)
    print('Sequence8 number of banks:'+str(banks))
    dram_optimization(sequence8,banks,128,64)
    print('#'*100)
    print('Sequence9 number of banks:'+str(banks))
    dram_optimization(sequence9,banks,128,128)
    print('#'*100)
    print('Sequence10 number of banks:'+str(banks))
    dram_optimization(sequence10,banks,128,128)
    print('#'*100)
    print('Sequence11 number of banks:'+str(banks))
    dram_optimization(sequence11,banks,128,128)
    print('#'*100)
    print('Sequence12 number of banks:'+str(banks))
    dram_optimization(sequence12,banks,128,128)
    print('#'*100)
    print('Sequence13 number of banks:'+str(banks))
    #dram_optimization(sequence13,banks,128,128)
    print('#'*100)
    print('Sequence14 number of banks:'+str(banks))
    dram_optimization(sequence14,banks,1024,512)
