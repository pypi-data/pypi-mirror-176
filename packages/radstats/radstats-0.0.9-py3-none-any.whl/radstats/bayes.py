### Stephen Lawrence 2022

import numpy as np
import itertools

decimals = 20

def OR(probs):
    Pmarg = [None] * (2 ** len(probs))
    for i,truth in enumerate(itertools.product([True,False],repeat=len(probs))):
        Pmarg[i] = np.prod([p if truth[n] else 1 - p for n,p in enumerate(probs)])
    Pcond = np.ones(len(Pmarg))
    Pcond[-1] = 0
    return np.around(np.dot(Pcond,Pmarg),decimals)

def AND(probs):
    Pmarg = [None] * (2 ** len(probs))
    for i,truth in enumerate(itertools.product([True,False],repeat=len(probs))):
        Pmarg[i] = np.prod([p if truth[n] else 1 - p for n,p in enumerate(probs)])
    Pcond = np.zeros(len(Pmarg))
    Pcond[0] = 1
    return np.around(np.dot(Pcond,Pmarg),decimals)

def VOTE2(probs):
    Pmarg = [None] * (2 ** len(probs))
    for i,truth in enumerate(itertools.product([True,False],repeat=len(probs))):
        Pmarg[i] = np.prod([p if truth[n] else 1 - p for n,p in enumerate(probs)])
    Pcond = [sum(i) >= 2 for i in itertools.product([True,False],repeat=len(probs))]
    return np.around(np.dot(Pcond,Pmarg),decimals)