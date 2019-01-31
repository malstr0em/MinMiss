from gurobipy import *
from read_sequence import read_sequence

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

from minRowMissb import dram_optimization as optb
from minRowMissc import dram_optimization as optc

sequence1 = read_sequence('Sequences/10_50.seq')
optb(sequence1,4,4)
optc(sequence1,4,4)
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
