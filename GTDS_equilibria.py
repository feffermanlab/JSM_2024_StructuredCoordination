import time 
tic = time.perf_counter()
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

toc1 = time.perf_counter()
def gen_connected_graph(n,p):
    G=nx.erdos_renyi_graph(n,p)
    comps=list(nx.connected_components(G))
    for ii in np.arange(0,len(comps)-1):
        G.add_edge(random.choice(list(comps[ii])),random.choice(list(comps[ii+1])))
    
    return G

def find_eq(G,y0=None, iter_limit = 5000):
    if y0 is None:
        y0 = np.arange(0,len(G.nodes()))
    iter = 0
    orbit=list()
    orbit.append(y0)
    yold=np.asarray((-1,)*len(G.nodes()))
    while (orbit[-1]!=yold).any() and iter<iter_limit:
        yold=orbit[-1]
        orbit.append(F(G,yold))
        iter=iter+1 
    
    return [G,orbit,iter]

def F(G,y):
    ynew = np.zeros(len(y))
    for n in np.arange(0,len(y)):
        argmax = mode([y[i]for i in list(G.neighbors(n))])
        ynew[n]=random.choice(argmax)
    return ynew

def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))

toc2=time.perf_counter()

result = find_eq(gen_connected_graph(20,0.1))
print(result[1][-1])
print("Completed in {} iterations".format(result[2]))
toc3=time.perf_counter()
print("imporing: {}s".format(toc1-tic) )
print("defining: {}s".format(toc2-toc1))
print("running: {}s".format(toc3-toc2))
print("total: {}s".format(toc3-tic))
graph=result[0]


pos=nx.spring_layout(graph)
plt.figure()
ec=nx.draw_networkx_edges(graph,pos)
nc = nx.draw_networkx_nodes(graph, pos, nodelist=graph.nodes(),node_color = result[1][-3])
plt.legend()
plt.show()

plt.figure()
ec=nx.draw_networkx_edges(graph,pos)
nc = nx.draw_networkx_nodes(graph, pos, nodelist=graph.nodes(),node_color = result[1][-2])
plt.legend()
plt.show()

plt.figure()
ec=nx.draw_networkx_edges(graph,pos)
nc = nx.draw_networkx_nodes(graph, pos, nodelist=graph.nodes(),node_color = result[1][-1])
plt.legend()
plt.show()