import networkx as nx
import random
import numpy as np


def ntangle(g,subn, n):
    
    i = 0
    dist = np.zeros(n)
    nodes = g.nodelist()
    while i<n:
        sg = g.subgraph(random.sample(nodes,subn))
        if(sg.is_connected()):
            x=sg.number_of_edges()
            #compute normalized edge density
            t = (x-(subn-1))/(subn**2/2-3*subn/2+1)
            dist[i]=t
            i = i+1 

    return(dist) 

def ntangle_compare(g1,g2, subns = None, n = None):
    subsizes = list()
    if subns == None:
        #Fill out a list of subn "logarithmicly"
        m = min(g1.number_of_nodes, g2.number_of_nodes)/10
        
        r=3
        while r<m:
            subsizes.append(r)
            r=r+(1*10**(int(r/10)))
    else:
        subsizes = subns

    for x in subsizes:
        d1 = ntangle(g1,x,n)
        d2 = ntangle(g2,x,n)
        ##compute the Kolmogorov-Smirnov statistic
        d1.sort()
        d2.sort()

