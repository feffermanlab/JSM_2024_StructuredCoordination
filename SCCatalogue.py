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
    #order 3: [6,7]
    #order 4: [13,18]
    #order 5: [26,52]
    #order 6: [75, 208]
    #order 7: [270, 1252]

    #Set up a dataframe to collect the relavent information
    df = pd.DataFrame({"name":[],"n":[], "partition":[], "degSQ":[],"ClusterNumber":[], "iso":[]})
    #generatie the lists of partitions to check once at the beginning of the method
    configList = [[0],genConfigs(1),genConfigs(2),genConfigs(3),genConfigs(4),genConfigs(5),genConfigs(6),genConfigs(7)]
    
    #Start counting graphs
    graphnumber = start
    index = 0

    for G in Atlas:
        #For each graph in the atlas, check to see if it's connected
        if(nx.is_connected(G)):
            if graphnumber%10 == 0:print(graphnumber)

            n = G.number_of_nodes()
            partitions = configList[n]

            #Check every possible partition (Fewer then B(n))
            for p in partitions:
                #Generate the orbit with only 2 time steps 
                o = orbit.Orbit(G,p,2)
                if (o.solution[0]==o.solution[1]).all():
                    #If nothing changed between step 0 and 1, it's an equilibrium 
                    s = degreeSeqs(o,np.floor(n/2)) #Find the degree sequence of each part of the partion
                    
                    #Check to see if that partitioned degree sequence has been observed before 
                    #as a way of checking potential isomorphic partitions
                    t = df[df["name"]==graphnumber]
                    iso = False
                    for r in t['degSQ']:
                        iso = r == s 

                    #add all the information to the data base the prepare consider the next partition    
                    df.loc[index]=(graphnumber, n, p, s, len(set(p)),iso)
                    index = index +1
        graphnumber= graphnumber +1

    df.to_excel("PartitionCatalogue.xlsx", sheet_name="partitionCatalogue", index = False)
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

'''Take a partition of a graph and return a set of degree sequences for each part'''
def degreeSeqs(orbit, max):
    sol = orbit.solution[1]
    g = orbit.graph
    degSet = list()
    for i in range(0,int(max)):
        vs = sol==i
        s = [j for j, x in enumerate(vs) if x]
        deg = g.degree(s)
        ret = [int(x[1]) for x in deg]
        ret.sort()
        degSet.append(ret)
        degSet.sort()
    return(degSet)

print(main(3,1253))
