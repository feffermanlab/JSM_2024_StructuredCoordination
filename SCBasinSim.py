import networkx as nx
import orbit
import PartitionTools
import numpy as np
import pandas as pd
import random 

def main(series, n, minp, maxp, reps,m ):
    ''' 
    Function to gather summary data about equilibrium partitions and the basin of stability for the consensus equilibrium
    
    Parameters
    ----
    series: Iterable
        The list of graph sizes to run
    n: int
        The number of graphs in each series to test
    minp: float
        The minimum value of p in the Erdos-Reyni random graph algorithm
    maxp: float
        The maximum value of p in the Erdos-Renyi random graph algorithm
    reps: int
        The number of graphs with particular p values are generated
    m: int
        The number of orbits generated from a graph

    Returns 
    ----
    df : pandas.DataFrame
        a dataframe which includes all the data from the simulation. 
    '''

    print('This run will attempt at most () orbits'.format(n*reps*m))
    iters = 0
    df = pd.DataFrame({"Graph Size":[],
                       "NormED":[],
                       "Diameter":[],
                       #"Girth":[],
                       #"Kemeny":[],
                       "ClusterDist":[]
                       })
    
    for v in series:
        print("Working on series-{}".format(v))
        for p in np.linspace(minp,maxp,n):
            for i in range(0,reps):
                g=nx.erdos_renyi_graph(v,p)
                if not nx.is_connected(g):break
                dist = np.zeros(m, dtype= int)
                for x in range(0,m):
                    #run an orbit
                    o = orbit.Orbit(g,random.sample(range(0,v),v))
                    #determine cluster number
                    dist[x]=PartitionTools.count_cliques(o)
                #Build cluster distribution
                e = max(dist)
                pdf = np.zeros(e+1)
                for j in range(0,e+1):
                    pdf[j] = sum(k == j for k in dist)
                edgenumber = g.number_of_edges()
                t = (2*(edgenumber-v-1))/(v**2-3*v+2)
                d = nx.diameter(g)
                #girth = nx.girth(g)
                #kemeny = nx.kemeny_constant(g)
                df.loc[iters]=(v,t,d,pdf)
                iters = iters+1
    #Write to data file
    return(df)

print(main([50],100,0.05,0.3,10,10))