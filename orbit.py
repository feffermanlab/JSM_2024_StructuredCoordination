import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random 

class Orbit:
    def __init__(self,G,y0=None,iter_limit=5000):
        self.graph = G
        result = self.__solve__(y0,iter_limit)
        self.solution = result[0]
        self.eq= result[2]
        self.cycle2= result[3]
        self.cycle3= result[4]
        self.report = result[5]

    def draw(self,n=1, dim=None):
        if dim == None:
            r = int(np.floor(np.sqrt(n)))
            c = int(np.ceil(n/r))
        else:
            r=dim[0]
            c=dim[1]
        pos=nx.spring_layout(self.graph)
        plt.figure()
        for ii in np.arange(1,n+1):
            plt.subplot(r,c,ii)
            ec=nx.draw_networkx_edges(self.graph,pos)
            nc = nx.draw_networkx_nodes(self.graph, pos, nodelist=self.graph.nodes(),node_color = self.solution[-(ii)])
        plt.show()


    def __solve__(self,y0=None, iter_limit = 5000):
        if y0 is None:
            y0 = np.arange(0,len(self.graph.nodes()))
        iter = 0
        orbit=list()
        orbit.append(y0)
        yold=np.asarray((-1,)*len(self.graph.nodes()))
        finished = False
        eq=False
        cycle2 = False
        cycle3=False
        while not finished:
            yold=orbit[-1]
            orbit.append(self.__F__(yold))
            iter=iter+1 
            if iter>=100:
                eq = (orbit[-1]==orbit[-2]).all() and (orbit[-1]==orbit[-3]).all()
                cycle2 = (orbit[-1]==orbit[-3]).all() and (orbit[-1]==orbit[-5]).all()
                cycle3 = (orbit[-1]==orbit[-4]).all() and (orbit[-1]==orbit[-7]).all()
            finished = iter>=iter_limit or eq or cycle2 or cycle3

        if eq:
            str="Resulted in an equilibrium"
        elif cycle2:
            str="Resulted in a 2 cycle"
        elif cycle3:
            str="Resulted in a 3 cycle"
        else: 
            str= "Did not result in an equilibrium or small limit cycle"
        report = "Finished in {} iterations. {}".format(iter, str)
        return [orbit,iter, eq, cycle2, cycle3,report]
    
    def __F__(self,y):
        ynew = np.zeros(len(y))
        for n in np.arange(0,len(y)):
            argmax = self.__mode__([y[i]for i in list(self.graph.neighbors(n))])
            ynew[n]=random.choice(argmax)
        return ynew

    def __mode__(self,array):
        most = max(list(map(array.count, array)))
        return list(set(filter(lambda x: array.count(x) == most, array)))