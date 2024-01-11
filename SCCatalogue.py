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
    Atlas = nx.graph_atlas_g()[start:end]
    #order 2: 3
    #order 3: [4,5]
    #order 4: [6,11]
    #order 5: [26,52]
    #order 6: [75, 208]

    df = pd.DataFrame({"name":[],"n":[], "partition":[], "ClusterNumber":[]})
    configList = [[0],genConfigs(1),genConfigs(2),genConfigs(3),genConfigs(4),genConfigs(5),genConfigs(6)]
    graphnumber = start
    index = 0
    for G in Atlas:
        if(nx.is_connected(G)):
            print(graphnumber)
            n = G.number_of_nodes()
            partitions = configList[n]
            for p in partitions:
                o = orbit.Orbit(G,p,2)
                if (o.solution[0]==o.solution[1]).all():
                    df.loc[index]=(graphnumber, n, p, len(set(p)))
                    index = index +1
                    if len(set(p))>1:o.draw()
                    #if len(set(p))==1:o.draw()
        graphnumber= graphnumber +1
        #This cannot yet differentiate between partitions which are identical on the basis of graphical symetry. 
    decomposable =df[df['ClusterNumber']>1]
    decomposable.to_excel("Decomposable6.xlsx", sheet_name ="decomposable6", index = False)
    decomposable = list(set(decomposable['name']))
    print(decomposable)
    #for n in range(start,end):
    #   print(n)
    #    if not(n in decomposable): 
    #        print("true")
    #        nx.draw(Atlas[n-start])
    #        plt.show()
    return df


'''generates all the non-isomorphic partitions on n vertices with floor(n/2) parts'''
def genConfigs(n):
    fl = np.floor(n/2) 
    configs = list() #prepares an empty list to hold partitions
    m = fl**(n-1) # the total number of partitions to be made
    for i in np.arange(0,m):
        digits = numberToBase(i, fl) #converts current partition number into base fl
        #Ensure that the length of the partition is correct
        #Turn the partitions into "cannonical forms" so isomorphic duplicates are not added
        x=canonicalConfig(list(np.zeros(n-len(digits),dtype = int))+digits) 
        if not any( (c == x).all() for c in configs): #If it's not already there, add it.
            configs.append(x)

            #Here there is an improvement to be made. We should only add those partitions which do not
            #Parts of size 1. How can we test for this easily?

    return(configs)


''' Convert a number n into base b'''
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


'''take a partition and return the canonical isomorphic partition'''
def canonicalConfig(config):
    l = config
    cl = np.zeros(len(l),dtype= int)
    digits = list()
    for i in range(0,len(l)):
        if l[i] not in digits:
            digits.append(l[i])
        cl[i]=digits.index(l[i])
    return(cl)


print(main(75,209))
