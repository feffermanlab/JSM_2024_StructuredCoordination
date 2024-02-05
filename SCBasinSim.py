import networkx as nx
import orbit
import numpy as np
import pandas as pd

def main(series, n, minp, maxp, reps,m ):
    iters = 0
    df = pd.DataFrame({"Graph Size":[],
                       "NormED":[],
                       "Diameter":[],
                       "Girth":[],
                       "Kemeny":[],
                       "ClusterDist":[]
                       })
    
    for v in series:
        print("Working on series-{}".format(v))
        ps = np.linspace(minp,maxp,n)
        for p in ps:
            for i in range(0,reps):
                g=nx.erdos_renyi_graph(v,p)
                dist = np.zeros(m)
                for x in range(0,m):
                    #run an orbit
                    o = orbit.Orbit(g)
                    #determine cluster number
                    dist[x]=count_cliques(o)
                #Build cluster distribution
                e = max(dist)
                pdf = np.zeros(e+1)
                for j in range(0,e+1):
                    pdf[j] = sum(k == j for k in dist)
                edgenumber = g.number_of_edges()
                t = (2*(edgenumber-v-1))/(v**2-3*v+2)
                d = nx.diameter(g)
                girth = nx.girth(g)
                kemeny = nx.kemeny_constant(g)
                df.loc[iters]=(v,t,d,girth,kemeny,pdf)
                iters = iters+1
    #Write to data file

    

                


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





main()