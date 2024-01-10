import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import pandas as pd
import random
import orbit

''' This script seeks to catalogue all of the equilibrium partitions in 
    connected graphs with at most 6 vertices
    
    It will traverse the entire networkx atlas and test every partition'''


def main(start,end):
    Atlas = nx.graph_atlas_g()[start:end]#
    df = pd.DataFrame({"name":[],"n":[], "partition":[], "ClusterNumber":[]})
    graphnumber = start
    index = 0
    for G in Atlas:
        if(nx.is_connected(G)):
            print(graphnumber)
            n = G.number_of_nodes()
            partitions = genConfigs(n)
            for p in partitions:
                o = orbit.Orbit(G,p,2)
                if (o.solution[0]==o.solution[1]).all():
                    df.loc[index]=(graphnumber, n, p, len(set(p)))
                    index = index +1
            graphnumber= graphnumber +1
    return df


def genConfigs(n):
    fl = np.floor(n/2) 
    configs = list()
    m = fl**(n-1)
    for i in np.arange(0,m):
        digits = numberToBase(i, fl)
        x=canonicalConfig(list(np.zeros(n-len(digits),dtype = int))+digits)
        if not any( (c == x).all() for c in configs):
            configs.append(x)
    return(configs)



def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def canonicalConfig(config):
    l = config
    cl = np.zeros(len(l),dtype= int)
    digits = list()
    for i in range(0,len(l)):
        if l[i] not in digits:
            digits.append(l[i])
        cl[i]=digits.index(l[i])
    return(cl)


print(main(29,50))
