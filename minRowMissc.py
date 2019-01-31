from gurobipy import *

# receives solution of the form [bank1, bank2, ..., bankn]
# bank1 = [row1, row2, ..., rowm]
def dram_optimization(solution, sequence, number_of_banks, number_of_rows):
    print('x')
