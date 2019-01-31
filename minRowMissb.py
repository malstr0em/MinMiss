from gurobipy import *

def dram_optimization(solution, sequence, number_of_rows, number_of_columns):
    maxvariables = 10000
    
    print('x')
