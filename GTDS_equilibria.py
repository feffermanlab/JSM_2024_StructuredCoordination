import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

def gen_connected_graph(n,p):
    G=nx.erdos_renyi_graph(n,p)
    comps=list(nx.connected_components(G))
    for ii in np.arange(0,len(comps)-1):
        G.add_edge(random.choice(list(comps[ii])),random.choice(list(comps[ii+1])))
    
    return G

print("working")
nx.draw(gen_connected_graph(50,0.01))
plt.show()