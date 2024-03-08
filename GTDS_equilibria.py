import time 
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import pandas as pd
import random
import orbit

def do_this():
    #print("We start by generating a random connected graph")
    n = 20
    p = 0.2
    #G = nx.watts_strogatz_graph(n,round(n*p),0)
    #G=nx.random_regular_graph(round(n*p),n)
    #G=nx.random_tree(n)
    #print("Then we can create an orbit object from this graph")
    #myOrbit = orbit.Orbit(G,[random.randint(0,40) for i in range(len(G.nodes))])
    #print(myOrbit.report)
    #cliques = find_cliques(myOrbit)
    #for i in range(1,len(cliques)):
    #print("Energy Threshold:{}".format(G.number_of_edges() - (n/2)))
    #print(myOrbit.energy)    
    #print("the orbit has a limit with {} cliques".format(len(cliques)))
    #myOrbit.draw(frames = (-1,), node_size= 50)
    #myOrbit.animation()
    
    #dfkreg = scan_kreg(1,1,10,2,100,1)
    #dfkreg.to_excel("Scan.xlsx", sheet_name ="kreg", index = False)
   
    #dfws = scan_ws(1,0.02,1,2,100,0,0.5)
    #dfws.to_excel("Scan.xlsx", sheet_name = "ws", index = False)

    #dfkreg = pd.read_excel("Scan.xlsx", sheet_name = "kreg")

    #n = len(dfkreg["n"])
    #eqs = dfkreg["equilibrium"].sum()
    #cycle2s = dfkreg["2cycle"].sum()
    #cycle3s = dfkreg["3cycle"].sum()
    
    #fig, ax = plt.subplots()
    #kreg = ax.scatter(x= dfkreg["Edge Density"],y = dfkreg["ClusterNumber"], c = dfkreg["n"], cmap = "seismic")
    #ax.set_title("Cluster Number by Edge Density among k-regular Graphs")
    #ax.set_xlabel("Edge Density")
    #ax.set_ylabel("Cluster Number")
    #fig.colorbar(kreg, label = "vertices")

    #ax.text(0.25, 20, 'n = {} \nEquilibria = {} \n2-cycles = {} \n3-cycles = {}'.format(n,eqs,cycle2s,cycle3s), style='italic',
    #    bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})

    #dfkreg.plot.scatter(x="Edge Density", y = "ClusterNumber", c = "equilibrium")
    #plt.show()
    
    #########------------------------------------------------
    dfws = pd.read_excel("Scan.xlsx", sheet_name = "ws")
    newdfew = dfws[(dfws["equilibrium"])|(dfws["2cycle"])]
    dfws = newdfew

    n = len(dfws["n"])
    eqs = dfws["equilibrium"].sum()
    cycle2s = dfws["2cycle"].sum()
    cycle3s = dfws["3cycle"].sum()
    
    fig, ax = plt.subplots()
    ws = ax.scatter(x= dfws["Edge Density"],y = dfws["ClusterNumber"], c = dfws["n"], cmap = "seismic")
    ax.set_title("Cluster Number by Edge Density among \nWatts Strogatz Random Graphs")
    ax.set_xlabel("Edge Density")
    ax.set_ylabel("Cluster Number")
    fig.colorbar(ws, label = "vertices")

    ax.text(0.27, 14, 'n = {} \nEquilibria = {} \n2-cycles = {} \n3-cycles = {}'.format(n,eqs,cycle2s,cycle3s), style='italic',
        bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})

    #dfkreg.plot.scatter(x="Edge Density", y = "ClusterNumber", c = "equilibrium")
    plt.show()
    


def scan_kreg(resn, resk, repeat, minn, maxn, mink):
    df = pd.DataFrame({"Run Number":[], "n":[], "Edge Density":[], 
                        "ClusterNumber":[],
                        "equilibrium":[],"2cycle":[], "3cycle":[],
                        "EndTime":[]})
    index = 1
    for n in np.arange(minn,maxn,resn):
        print("n={}".format(n))
        for k in np.arange(mink,n/2,resk):
            k=round(k)
            for r in np.arange(repeat): 
                if (n*k)%2 ==0:
                    G=nx.random_regular_graph(k,n)
                    if nx.is_connected(G)== True:
                        myOrbit = orbit.Orbit(G,[random.randint(0,40) for i in range(len(G.nodes))])
                        NodeNumber=myOrbit.size
                        df.loc[index] = [index,NodeNumber,myOrbit.graph.number_of_edges()/(NodeNumber*(NodeNumber-1)/2),
                             count_cliques(myOrbit),
                             myOrbit.eq, myOrbit.cycle2, myOrbit.cycle3, myOrbit.iter] 
                        index=index+1
    print(df)
    return(df)

def scan_ws(resn, resp, repeat, minn, maxn, minp, maxp):
    df = pd.DataFrame({"Run Number":[], "n":[], "Edge Density":[], 
                        "ClusterNumber":[],
                        "equilibrium":[],"2cycle":[], "3cycle":[],
                        "EndTime":[]})
    index = 1
    for n in np.arange(minn,maxn,resn):
        print("n={}".format(n))
        for p in np.arange(minp,maxp, resp):
            for k in np.arange(2,n/2):
                k = round(k)
                for r in np.arange(repeat): 
                    G = nx.watts_strogatz_graph(n,k,p)
                    if nx.is_connected(G)== True:
                        myOrbit = orbit.Orbit(G,[random.randint(0,40) for i in range(len(G.nodes))])
                        NodeNumber=myOrbit.size
                        df.loc[index] = [index,NodeNumber,myOrbit.graph.number_of_edges()/(NodeNumber*(NodeNumber-1)/2),
                            count_cliques(myOrbit),
                            myOrbit.eq, myOrbit.cycle2, myOrbit.cycle3, myOrbit.iter] 
                        index=index+1
    print(df)
    return(df)

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

def count_cliques(orbit):
    Q=find_cliques(orbit)
    return(len(Q))      


