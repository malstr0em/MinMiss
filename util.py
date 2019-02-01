import numpy as np
from collections import defaultdict

def subsequence(elements,sequence):
    map = defaultdict(lambda : False)
    for e in np.nditer(elements):
        map[int(e)]=True
    return [s for s in sequence if map[s]]#for e in np.nditer(elements) if e==s]

def down_grade(sequence):
    uniques = np.unique(sequence)
    map = dict()
    for i in range(len(uniques)):
        map[uniques[i]]=i
    return [map[s] for s in sequence],uniques
