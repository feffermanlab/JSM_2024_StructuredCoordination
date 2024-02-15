import networkx as nx
import orbit
import PartitionTools
import numpy as np
import pandas as pd
import random 

def main(series, n, minExpd, maxExpd, reps,m ):
    ''' 
    Function to gather summary data about equilibrium partitions and the basin of stability for the consensus equilibrium
    
    Parameters
    ----
    series: Iterable
        The list of graph sizes to run
    n: int
        The number of graphs in each series to test
    minExpd: float
        The minimum average degree for random graph generation
    maxExpd: float
        The maximum average degree for random graph generation
    reps: int
        The number of graphs with a particular p value to be are generated
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
                       "ED":[],
                       "NormED":[],
                       "Diameter":[],
                       "DegreeSequence":[],
                       "LimitDist":[],
                       "ClusterDist":[]
                       })
    
    for v in series:
        print("Working on series-{}".format(v))
        for p in np.linspace(minExpd/(v-1),maxExpd/(v-1),n):
            for i in range(0,reps):
                g=nx.erdos_renyi_graph(v,p)
                if not nx.is_connected(g):break
                dist = np.zeros(m, dtype= int)
                lims = np.zeros(m, dtype = int)
                for x in range(0,m):
                    #run an orbit
                    o = orbit.Orbit(g,random.sample(range(0,v),v))
                    #determine cluster number
                    dist[x]=PartitionTools.count_cliques(o)
                    if o.eq:lims[x]=1
                    else:
                        if o.cycle2:lims[x]=2
                        else:
                            if o.cycle3:lims[x]=3
                            else:lims[x]=0

                #Build cluster distribution
                e = max(dist)
                pdf = np.zeros(e+1)
                for j in range(0,e+1):
                    pdf[j] = sum(k == j for k in dist)

                #Build Limit Dist:
                limDist=np.zeros(4) 
                for j in range(0,4):
                    limDist[j] = sum(k==j for k in lims)  
                edgenumber = g.number_of_edges()
                t = 2* edgenumber/ (v**2-v)
                nt = (2*(edgenumber-v-1))/(v**2-3*v+2)
                d = nx.diameter(g)
                deg = [val for (node, val) in g.degree()]
                #girth = nx.girth(g)
                #kemeny = nx.kemeny_constant(g)
                df.loc[iters]=(v,t,nt,d,deg,limDist,pdf)
                iters = iters+1
    #Write to data file
    return(df)


#when run for real:
#series [50,100,150,200,400]
#n = 200
#minEcpd=1.5
#maxExpd =8
#reps = 10
#m = 100

# This will run 1,000,000 orbits  


print(main([50,100],10,1,20,1,50))
#main([50,100,150,200,300],200,1.5,8,10,100).pd.to_csv("SCBasinResults.csv",index = True)