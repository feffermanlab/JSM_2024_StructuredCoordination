import time 
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import random
import orbit

def do_this():
    print("We start by generating a random connected graph")
    n = 50 
    p = 0.1
    G=nx.random_regular_graph(round(n*p),n)
    print("Then we can create an orbit object from this graph")
    myOrbit = orbit.Orbit(G,[random.randint(0,40) for i in range(len(G.nodes))])
    print(myOrbit.report)
    cliques = find_cliques(myOrbit)
    print("the orbit has a limit with {} cliques".format(len(cliques)))
    myOrbit.draw(frames=(-3,-2,-1))
    myOrbit.animation()
    
    




def gen_connected_graph(n,p):
    ''' 
    function to generate a connected graph

    Parameters
    -----------
    n : int
        The number of vertices in the graph
    p : float
        The edge liklihood value for the Erdos Renyi graph generation

    Returns 
    ----------
    G : nx.Graph
        A conneceted graph
    '''

    #start by generating a random Erdos Renyi Graph
    G=nx.erdos_renyi_graph(n,p)

    #get a list of connected components and connect them 
    comps=list(nx.connected_components(G))
    for ii in np.arange(0,len(comps)-1):
        G.add_edge(random.choice(list(comps[ii])),random.choice(list(comps[ii+1])))
    
    return G

def find_cliques(sol):
    '''
    A function to return the cliques of a equilibrium coloring

    Parameters
    ----------
    sol : Orbit
        The orbit to be analyzed
    
    Returns
    -------
    Q : list 
        A list of networkx.Graph objects, each of which are a clique of the limit of sol.
    '''
    
    G=sol.graph
    lim = sol.get_limit()
    Q=list()
    if sol.eq:
        config = lim
        strats = list(set(config))
        for ii in strats:
            locs = (config == ii)
            clique=G.subgraph(np.asarray(G.nodes)[locs]).copy()
            Q.append(clique)
    elif sol.cycle2:
        config1=lim[0]
        config2=lim[1]
        strats = list(set(config1))
        alts = G.subgraph(np.asarray(G.nodes)[config1 != config2])
        Q=Q+[alts.subgraph(c).copy() for c in nx.connected_components(alts)]
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

#This function is a work in progress, I will not call it below
def count_cliques(n,p,count):
    clique_count = np.zeros(count)
    for ii in np.arange(0,count):
        cliques = find_cliques(orbit.Orbit(gen_connected_graph(n,p)))
        clique_count[ii] = len(cliques)
    return clique_count        


#do_this()