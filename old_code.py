# -*- coding: utf-8 -*-
import sys
import math
import random
import itertools
import numpy as np
import matplotlib.pyplot as plt
from gurobi import *
import os


def read_sequence(file_path):
    '''
    ﻿Reads a *.seq-file and returns a list corresponding to the sequence in the file
    :param file_path: a string containing the relative path to the *.seq-file
    :return: sequence: ﻿a list containing the sequence of the *.seq file
    '''

    sequence = list()
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, file_path)

    try:
        with open(file_path, "r") as f:
            print("Reading Sequence...")
            for line in f:
                sequence.append(int(line))

        print("Sequence read\nNumber of Elements: {1} \nLength: {0}".format(len(sequence), len(set(sequence))))
        return sequence

    except IOError as e:
        print(os.strerror(e.errno))
        exit()

    return sequence

def dram_optimization(sequence, number_of_banks, number_of_rows, number_of_columns):
    
    m = Model("shittyIP")
    number_of_elements = len(np.unique(sequence)) #not ugly
    print(number_of_elements)
    
    
    
    #create variables
    #vars = tupledict()
    #for i in range(number_of_elements):
    #    for b in range(number_of_banks):
    #        for r in range(number_of_rows):
    #            
    #           vars[i,b,r] = m.addVar(name=str(i)+'i '+str(b)+'b '+str(r)+'r', vtype=GRB.BINARY)
    vars = m.addVars(number_of_elements,number_of_rows,vtype=GRB.BINARY)
    
    m.update()
    
    print("done with vars")
    
    #Constrains
    for b in range(number_of_banks):
        for r in range(number_of_rows):
            m.addConstr(sum(vars[i,r] for i in range(number_of_elements)) <= number_of_columns)
                
    for i in range(number_of_elements):
        m.addConstr(sum(vars[i,r] for r in range(number_of_rows) for b in range(number_of_banks)) == 1)

    
    
    #model.setObjective(x + y, GRB.MAXIMIZE)    
    m.optimize()
    
    if m.SolCount == 0:
        print('No solution found, optimization status = %d' % m.Status)
    else:
        print('Solution found, objective = %g' % m.ObjVal)
        #print(m.getVars())
        #for v in m.getVars():
        #    if v.X != 0.0:
        #        print('%s %g' % (v.VarName, v.X))

    
    banks = dict()
    rows = dict()
    hits = 0
    misses = len(sequence) - hits
    

    
    return hits,misses,banks,rows

def c1OPT(Solution,sequence, number_of_banks, number_of_rows, number_of_columns):
    
    number_of_elements = len(np.unique(sequence))
    
    if(number_of_banks):
        return
        
    
    step_size = math.floor(math.log(number_of_banks))
    print(step_size)
    
    if (step_size <= 1):
        step_size = 2
        
    
    
    return




file_path = os.path.relpath("/home/blueuser/Documents/Int.Prog./Sequences/11520_644456.seq")

sequence = read_sequence(file_path)

number_of_banks = 1
number_of_rows = 150
number_of_columns = 150
dram_optimization(sequence, number_of_banks, number_of_rows, number_of_columns)