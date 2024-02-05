import networkx as nx
import random
import numpy as np


def ntangle(g,subn, n):
    
    i = 0
    dist = np.zeros(n)
    nodes = list(g)
    while i<n:
        sg = g.subgraph(random.sample(nodes,subn))
        if(nx.is_connected(sg)):
            x=sg.number_of_edges()
            #compute normalized edge density
            t = (x-(subn-1))/(subn**2/2-3*subn/2+1)
            dist[i]=t
            i = i+1 

    return(dist) 

def ntangle_compare(g1,g2, subns = None, n = 100, KSresolution = 1000):
    subsizes = list()
    if subns == None:
        #Fill out a list of subn "logarithmicly"
        m = min(g1.number_of_nodes(), g2.number_of_nodes())/10
        
        r=3
        while r<m:
            subsizes.append(r)
            r=r+(1*10**(int(r/10)))
    else:
        subsizes = subns
        
    Dn = list()
    for x in subsizes:
        d1 = ntangle(g1,x,n)
        d2 = ntangle(g2,x,n)

        print("computing Kolmogorov-Smironov Statistic for n= {}".format(x))
        ##compute the Kolmogorov-Smirnov statistic
        div = np.linspace(0,max(max(d1),max(d2)),KSresolution)
        cdf1=np.zeros(KSresolution)
        cdf2=np.zeros(KSresolution)
        for i in range(0,KSresolution):
            cdf1[i] = sum(j<=div[i] for j in d1)
            cdf2[i] = sum(j<=div[i] for j in d2)
        Dn.append(max(abs(cdf1-cdf2)))
    return(Dn)
        
