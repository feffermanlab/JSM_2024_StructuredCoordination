import networkx as nx
import orbit
import PartitionTools
import numpy as np
import pandas as pd
import random 
import argparse

##Read in arguments
parser = argparse.ArgumentParser()
parser.add_argument("series", 
                    help = "The size of graphs in this series", 
                    type = int)
parser.add_argument("n",
                    help = "number of graphs to be generated in this serires",
                    type = int)
parser.add_argument("minExpd",
                    help = "Minimum mean degree",
                    type = float)
parser.add_argument("maxExpd",
                    help = "Maximum mean degree",
                    type = float)
parser.add_argument("reps",
                    help = "number of graphs generated with a particular mean degree",
                    type = int)
parser.add_argument("m",
                    help = "Number of orbits to run on a single graph",
                    type = int)

args = parser.parse_args()


def main(series, n, minExpd, maxExpd, reps,m ):
    ''' 
    Function to gather summary data about equilibrium partitions and the basin of stability for the consensus equilibrium
    
    Parameters
    ----
    series: int
        graph size to run
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
    
    v = series 
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
                elif o.cycle2:lims[x]=2
                elif o.cycle3:lims[x]=3
                elif o.cycle4:lims[x]=4
                else:lims[x]=0

            #Build cluster distribution
            e = max(dist)
            pdf = np.zeros(e+1)
            for j in range(0,e+1):
                pdf[j] = sum(k == j for k in dist)

            #Build Limit Dist:
            limDist=np.zeros(5) 
            for j in range(0,4):
                limDist[j] = sum(k==j for k in lims)  
            edgenumber = g.number_of_edges()
            t = 2* edgenumber/ (v**2-v)
            nt = (2*(edgenumber-v-1))/(v**2-3*v+2)
            d = nx.diameter(g)
            deg = [val for (node, val) in g.degree()]
            df.loc[iters]=(v,t,nt,d,deg,limDist,pdf)
            iters = iters+1
    #return dataframe
    return(df)


#when run for real:
#series [50,100,150,200,400]
#n = 200
#minEcpd=0.5
#maxExpd =20
#reps = 10
#m = 100

# This will run 1,000,000 orbits  

if __name__=="__main__":
    df = main(args.series,args.n,args.minExpd,args.maxExpd,args.reps,args.m)
    print(df)
    df.to_csv("DataFiles\SCBasinResults{}.csv".format(args.series),index = True)