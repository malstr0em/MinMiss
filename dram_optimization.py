from gurobipy import *

m=Model()
vars = m.addVars(10,10,vtype=GRB.BINARY)
m.addConstrs(vars.sum(i,'*') == 2 for i in range(10))
m.optimize()

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
    print('x')
