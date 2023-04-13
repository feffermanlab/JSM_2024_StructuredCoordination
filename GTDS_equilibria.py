import time 
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import orbit


def gen_connected_graph(n,p):
    G=nx.erdos_renyi_graph(n,p)
    comps=list(nx.connected_components(G))
    for ii in np.arange(0,len(comps)-1):
        G.add_edge(random.choice(list(comps[ii])),random.choice(list(comps[ii+1])))
    
    return G

#def find_cliques(G,orbit):

myOrbit = orbit.Orbit(gen_connected_graph(20,0.1))

print(myOrbit.report)
myOrbit.draw(2)
