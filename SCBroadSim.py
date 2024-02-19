import networkx as nx
import orbit
import PartitionTools
import numpy as np
import pandas as pd
import random 
import argparse
import time


#"Global" Variables" 
vmin = 50
vmax = 450
vres = 5
n = 100
minExpd = 0.5
maxExpd = 20
reps = 20

#Total run number
r = 100

#For real run use 
#    vres = 5
#    n = 100
#    minExpd = 0.5
#    maxExpd = 20
#    reps = 10


##Read in arguments
parser = argparse.ArgumentParser()
#parser.add_argument("vmin", 
#                    help = "The minimum graph size", 
#                    type = int)
#parser.add_argument("vmax",
#                    help = "The max graph size",
#                    type = int)
#parser.add_argument("vres",
#                    help = "How many graph sizes to sample in range [vmin,vmax]",
#                    type = int)
parser.add_argument("Run",
                    help = "Which section of the total graph space to sample",
                    type = int)
#parser.add_argument("n",
#                    help = "number of graphs to generate of a particular size",
#                    type = int)
#parser.add_argument("minExpd",
#                    help = "Minimum mean degree",
#                    type = float)
#parser.add_argument("maxExpd",
#                    help = "Maximum mean degree",
#                    type = float)
#parser.add_argument("reps",
#                    help = "number of graphs generated with a particular mean degree",
#                    type = int)
args = parser.parse_args()


def main(minv, maxv, vres, n, minExpd, maxExpd, reps):
    ''' 
    Function to gather summary data about equilibrium partitions and the basin of stability for the consensus equilibrium
    
    Parameters
    ----
    minv: int
        The smallest number of vertices to observe
    maxv: int
        The largest number of vertices to observe
    vres: int
        The resolution to scan over the vertex space
    n: int
        The number of graphs in each series to test
    minExpd: float
        The minimum mean degree
    maxExpd: float
        The maximum mean degree
    reps: int
        The number of graphs with particular mean degree are generated

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
                       "ClusterNumber":[],
                       "EQ":[],
                       "Cycle2":[],
                       "Cycle3":[],
                       "Cycle4":[],
                       "modularity":[]
                       })
    
    for v in np.linspace(minv,maxv,vres):
        v=round(v)
        for p in np.linspace(minExpd/(v-1),maxExpd/(v-1),n):
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
                cycle4 = o.cycle4
                q=PartitionTools.OrbitModularity(o)
                edgenumber = g.number_of_edges()
                t = 2* edgenumber/ (v**2-v)
                nt = (2*(edgenumber-v-1))/(v**2-3*v+2)
                d = nx.diameter(g)
                deg = [val for (node, val) in g.degree()]

                df.loc[iters]=(v,t,nt,d,deg,clusternumber,eq,cycle2,cycle3, cycle4,q)
                iters = iters+1
    #Write to data file
    return(df)


if __name__=="__main__":
    starttime = time.time()
    print("estimated time: {} minutes".format((vmin +(args.Run/r)*(vmax-vmin))*0.0012*vres*n*reps/60))
    x = round(vmin +(args.Run/r)*(vmax-vmin))
    y = round(vmin +((args.Run +1)/r)*(vmax-vmin))
    df=main(x,
               y,
               vres,
               n,
               minExpd,
               maxExpd,
               reps)
    endtime = time.time()
    df.to_csv("Datafiles\SCBroadSim{}.csv".format(args.Run),index=False)
    print("attempting {} orbits took {} seconds".format(vres*n*reps,endtime-starttime))
