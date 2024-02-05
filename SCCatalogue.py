import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import pandas as pd
import copy 
from itertools import permutations
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
    df = pd.DataFrame({"name":[],
                       "n":[], 
                       "partition":[],
                        "degSQ":[],
                        "ClusterNumber":[],
                        "iso":[],
                        "isoto":[]})
    #generatie the lists of partitions to check once at the beginning of the method
    configList = [[0],genConfigs(1),genConfigs(2),genConfigs(3),genConfigs(4),genConfigs(5),genConfigs(6),genConfigs(7)]
    
    #Start counting graphs
    graphnumber = start
    index = 0

    for G in Atlas:
        #For each graph in the atlas, check to see if it's connected
        if(nx.is_connected(G)):

            #progress tracking
            if graphnumber%10 == 0:print('{} %% done'.format(graphnumber/end*100))

            n = G.number_of_nodes()
            partitions = configList[n]
            #Check every possible partition (Fewer then B(n))
            for p in partitions:
                #Generate the orbit with only 2 time steps 
                o = orbit.Orbit(G,p,2)
                if (o.solution[0]==o.solution[1]).all():
                    #If nothing changed between step 0 and 1, it's an equilibrium 
                    
                    #Find the degree sequence of each part of the partion
                    #Check to see if that partitioned degree sequence has been observed before 
                    #as a way of checking potential isomorphic partitions
                    s = degreeSeqs(o,np.floor(n/2))
                    t = df[df["name"]==graphnumber]
                    idx = t.index.tolist()
                    iso = False
                    isoto = -1
                    for j in idx:
                        r =t.loc[j,"degSQ"]
                        p1 = t.loc[j,"partition"]
                        ps = permutePartition(p)
                        for p2 in ps:
                            if isoDetect(G, p1, p2) : ##This almost works but we need to check all the partition permutation
                                iso = True 
                                isoto = j 
                                break
                            if iso:break 


                    #Check to see if parts of the partition are connected
                    con = True
                    for i in range(0,int(max(p))+1):
                        vs = o.solution[1]==i
                        l = [j for j, x in enumerate(vs) if x]
                        if len(l)>0 and not nx.is_connected(G.subgraph(l)):
                            con = False
                            break
                        

                    #add all the information to the data base the prepare consider the next partition    
                    if con : df.loc[index]=(graphnumber, n, p, s, len(set(p)),iso,isoto)
                    index = index +1
        graphnumber= graphnumber +1
    df.insert(0,"pnumber",df.index.tolist(),True)
    df.to_excel("PartitionCatalogue.xlsx", sheet_name="partitionCatalogue", index = False)
    print(df[df['iso']])
    print('there are {} isomorphisms'.format(
       len(df[df['iso']]["name"])))
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


def isoDetect(g, p1, p2):
    #nx.draw(g)
    #plt.show()
    G1 = copy.deepcopy(g)
    G2 = copy.deepcopy(g)
    n = len(g.nodes)
    #To G1 add pendant vertices to every node according to the part of the partition P1  it's in
    for i in np.arange(0,len(p1)):
        for j in np.arange(0,p1[i]+1):
            G1.add_node(n)
            G1.add_edge(i,n)
            n=n+1
    #To G2 add pendant vertices ot every node according to the part of the partition P2 it's in
    #nx.draw(G1)
    #plt.show()
    n=len(g.nodes)
    for i in np.arange(0,len(p2)):
        for j in np.arange(0,p2[i]+1):
            G2.add_node(n)
            G2.add_edge(i,n)
            n=n+1
    #nx.draw(G2)
    #plt.show()
    return(nx.is_isomorphic(G1, G2))

def permutePartition(p):
    l = list(permutations(range(0,max(p)+1)))
    #print(l)
    ret = list()
    for r in l:
        #print(r)
        s = np.zeros(len(p),dtype=int)
        for i in np.arange(len(p)):
            s[i] = int(r.index(p[i]))
        ret.append(s)
    return(ret)

#print(main(3,1253))


def test():
    #G= nx.graph_atlas_g()[31]
    #p1= [0,0,1,1,0]
    #p2 = [1,0,0,0,1]
    #print( isoDetect(G,p1,p2))

    print(permutePartition([0,0,1,1,0,1]))

#test()


def analysis():
    df = pd.read_excel("PartitionCatalogue.xlsx", sheet_name="partitionCatalogue")
    newdf = df[df['iso']==False]
    
    #find out how many different partitions there are for graphs on n vertices
    for i in range(2,8):
        tempdf = newdf[newdf['n']==i] 
        l = len(tempdf)
        print ('for graphs on {} vertices there are {} total partitions'.format(i,l))
        clusternumberlist= list()
        for j in range(1,max(tempdf['ClusterNumber'])+1):
            clusternumberlist.append(len(tempdf[tempdf['ClusterNumber']==j]))
            print('there are {} partitions with {} parts'.format(clusternumberlist[-1],j))

    
    
    for ik in range(2,8):
        print('for graphs on {} vertices'.format(ik))
        dfx = newdf[newdf['n']==ik]
        pcounts = list()
        for i in range(min(dfx['name']),max(dfx['name'])+1):
            pcounts.append( len(dfx[dfx['name']==i]['name']))
            if len(dfx[dfx['name']==i]['name'])==10: print(i)
        for j in range(min(pcounts),max(pcounts)+1):
            print('There are {} graphs with {} partitions'.format(pcounts.count(j), j ))
            

    #find out how many indecomposable 

analysis()