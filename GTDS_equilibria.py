import time 
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import matplotlib.colors as mcolors
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
    elif sol.cycle2:
        config1=lim[0]
        config2=lim[1]
        strats = list(set(config1))
        Q.append(nx.connected_components(G.subgraph(np.asarray(G.nodes)[config1 != config2])))
        for ii in strats:
            t1 = (config1 == ii)
            t2 = (config1 == config2)
            locs = np.logical_and(t1,t2)
            if locs.any():
                clique = G.subgraph(np.asarray(G.nodes)[locs])
                Q.append(clique)
    else:
        print("There is no equilibrium or 2-cycle in this orbit")
    return Q 

def count_cliques(n,p,count):
    clique_count = np.zeros(count)
    for ii in np.arange(0,count):
        cliques = find_cliques(orbit.Orbit(gen_connected_graph(n,p)))
        clique_count[ii] = len(cliques)
    return clique_count        

#myOrbit = orbit.Orbit(gen_connected_graph(20,0.2))
#G=nx.complete_bipartite_graph(4,2)


G=gen_connected_graph(40,0.1)
myOrbit = orbit.Orbit(G,[random.randint(0,40) for i in range(len(G.nodes))])
cliques = find_cliques(myOrbit)
print(myOrbit.report)
n=len(cliques)
myOrbit.animation()
#limit = myOrbit.get_limit()
#print(np.shape(np.asarray(myOrbit.get_limit())))
#if myOrbit.eq:
#   myOrbit.draw()
#else:
#    myOrbit.draw(2)
#print(cliques)
print("This orbit has a limit with {} cliques".format(n))

#clique_counts = count_cliques(100,0.02,100)
#print(clique_counts)
#print(np.arange(clique_counts.min(),clique_counts.max()+1))
#plt.hist(clique_counts,bins = np.arange(clique_counts.min(),clique_counts.max()+1))
#plt.show()