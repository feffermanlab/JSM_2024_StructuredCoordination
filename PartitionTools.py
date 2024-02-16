import networkx as nx
import random
import numpy as np
import orbit 

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

def ntangle(g,subn, n):
    
    i = 0
    dist = np.zeros(n)
    nodes = list(g)
    while i<n:
        sg = g.subgraph(random.sample(nodes,subn))
        if(nx.is_connected(sg)):
            x=sg.number_of_edges()
            #compute normalized edge density
            t = (x-(subn-1))/(subn**2/2-3*subn/2+1)
            dist[i]=t
            i = i+1 

    return(dist) 

def ntangle_compare(g1,g2, subns = None, n = 100, KSresolution = 1000):
    subsizes = list()
    if subns == None:
        #Fill out a list of subn "logarithmicly"
        m = min(g1.number_of_nodes(), g2.number_of_nodes())/10
        
        r=3
        while r<m:
            subsizes.append(r)
            r=r+(1*10**(int(r/10)))
    else:
        subsizes = subns
        
    Dn = list()
    for x in subsizes:
        d1 = ntangle(g1,x,n)
        d2 = ntangle(g2,x,n)

        print("computing Kolmogorov-Smironov Statistic for n= {}".format(x))
        ##compute the Kolmogorov-Smirnov statistic
        div = np.linspace(0,max(max(d1),max(d2)),KSresolution)
        cdf1=np.zeros(KSresolution)
        cdf2=np.zeros(KSresolution)
        for i in range(0,KSresolution):
            cdf1[i] = sum(j<=div[i] for j in d1)
            cdf2[i] = sum(j<=div[i] for j in d2)
        Dn.append(max(abs(cdf1-cdf2)))
    return(Dn)



def OrbitModularity(sol):
    if not sol.eq: return (2)
    G= sol.graph

    #turn solution into list of vertex sets
    p = sol.get_limit()
    part = list()
    for i in list(set(p)):
        l= p == i 
        parti = [j for j, x in enumerate(l) if x ]
        part.append(parti)
    q = nx.community.modularity(G,part)
    return(q)


def test():
    G = nx.erdos_renyi_graph(10,0.4)
    o = orbit.Orbit(G)
    q =OrbitModularity(o)
    return(q)




