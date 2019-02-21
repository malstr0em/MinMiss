from util import count_missesc,subsequence
import numpy as np
import random as rm
import time as tm
import math

# receives solution of the form [bank1, bank2, ..., bankn]
# bank1 = [row1, row2, ..., rowm]
def dram_optimization(solution, sequence, number_of_banks, number_of_rows, time=np.inf):
    glstart=tm.time()
    current_solution = solution
    current_misses = count_missesc(current_solution,sequence)
    combinations = []
    for i in range(number_of_banks):
        for j in range(number_of_banks):
            if i<j:
                combinations.append((i,j))
    for i,j in combinations:
        for _ in range(int(math.log(number_of_rows,2))):
            if tm.time()-glstart>time:
                return current_solution
            cut_solution = np.hstack([current_solution[i],current_solution[j]])
            test_solution_part = shuffle(cut_solution, number_of_rows)
            test_solution = current_solution
            test_solution[i]=test_solution_part[0]
            test_solution[j]=test_solution_part[1]
            test_misses = count_missesc(test_solution,sequence)
            if test_misses<current_misses:
                current_solution=test_solution
                current_misses=test_misses
    return current_solution    

def shuffle(solution, number_of_rows):
    result = np.zeros((2, number_of_rows), dtype=int)
    elements=np.ndarray.flatten(solution)
    rm.shuffle(elements)
    x=0
    for b in range(2):
        for r in range(number_of_rows):
            result[b,r]=elements[x]
            x+=1
    return result
    
