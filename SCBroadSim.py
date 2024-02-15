import networkx as nx
import orbit
import PartitionTools
import numpy as np
import pandas as pd
import random 

def main(minv, maxv, vres, n, minp, maxp, reps):
    ''' 
    Function to gather summary data about equilibrium partitions and the basin of stability for the consensus equilibrium
    
    Parameters
    ----
    series: Iterable
        The list of graph sizes to run
    n: int
        The number of graphs in each series to test
###CHANGE SO THAT WE USE EXPECTED DEGREE
    minp: float
        The minimum value of p in the Erdos-Reyni random graph algorithm
    maxp: float
        The maximum value of p in the Erdos-Renyi random graph algorithm
    reps: int
        The number of graphs with particular p values are generated

    Returns 
    ----
    df : pandas.DataFrame
        a dataframe which includes all the data from the simulation. 
    '''
    iters = 0
    df = pd.DataFrame({"Graph Size":[],
                       "ED":[],
                       "NormED":[],
                       "Diameter":[],
                       "DegreeSequence":[],
                       "EQ":[],
                       "Cycle2":[],
                       "Cycle3":[],
                       "Cycle4":[],
                       "modularity":[]
                       })
    
    for v in range(minv,maxv+1):
        #edit p space here too
        for p in np.linspace(minp,maxp,n):
            for i in range(0,reps):
                g=nx.erdos_renyi_graph(v,p)
                if not nx.is_connected(g):break
                #run an orbit
                o = orbit.Orbit(g,random.sample(range(0,v),v))
                #determine cluster number
                clusternumber=PartitionTools.count_cliques(o)
                eq=o.eq 
                cycle2 = o.cycle2
                cycle3 = o.cycle3 
                
                if eq: #find modularity
#UNFINISHED!!!! BELOW HERE IS INCORRECT
                edgenumber = g.number_of_edges()
                t = 2* edgenumber/ (v**2-v)
                nt = (2*(edgenumber-v-1))/(v**2-3*v+2)
                d = nx.diameter(g)
                deg = [val for (node, val) in g.degree()]

                df.loc[iters]=(v,t,nt,d,deg,)
                iters = iters+1
    #Write to data file
    return(df)