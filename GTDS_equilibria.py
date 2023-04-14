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

def find_cliques(sol):
    G=sol.graph
    lim = sol.get_limit()
    Q=list()
    if sol.eq:
        config = lim
        strats = list(set(config))
        for ii in strats:
            locs = (config == ii)
            clique=G.subgraph(np.asarray(G.nodes)[locs])
            Q.append(clique)
        return Q 

    elif sol.cycle2:
        cofig1=lim[0]
        config2=lim[1]
    return("not yet supported")


#myOrbit = orbit.Orbit(gen_connected_graph(20,0.2))
#G=nx.complete_bipartite_graph(4,2)
G=gen_connected_graph(20,0.2)
myOrbit = orbit.Orbit(G,[random.randint(0,4) for i in range(len(G.nodes))])
print(myOrbit.report)
print(find_cliques(myOrbit))
#limit = myOrbit.get_limit()
#print(np.shape(np.asarray(myOrbit.get_limit())))

#myOrbit.draw(2)
