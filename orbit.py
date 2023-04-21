import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import random 

class Orbit:
    def __init__(self,G,y0=None,iter_limit=5000):
        self.graph = G
        result = self.__solve__(y0,iter_limit)
        self.solution = result[0]
        self.iter = result[1]
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
            nc = nx.draw_networkx_nodes(self.graph, pos, nodelist=self.graph.nodes(),node_color = self.solution[-(ii)],node_size = 20)
        plt.show()

    def __str__(self):
        n=len(self.graph.nodes())
        st= "Starting from a given coloring of a connected graph on {} vertices, the orbit {}".format(n,self.report)
        return st 

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
            orbit.append(self.__F__(yold).astype(int))
            iter=iter+1 
            if iter>=19:
                eq = (orbit[-1]==orbit[-2]).all() and (orbit[-1]==orbit[-3]).all()
                cycle2 = (orbit[-1]==orbit[-3]).all() and (orbit[-1]==orbit[-5]).all() and (orbit[-1]==orbit[-19]).all()
                cycle3 = (orbit[-1]==orbit[-4]).all() and (orbit[-1]==orbit[-7]).all() and (orbit[-1]==orbit[-19]).all()
            finished = iter>=iter_limit or eq or cycle2 or cycle3

        if eq:
            str="The orbit ended at an equilibrium"
        elif cycle2:
            str="The orbit ended in a 2 cycle"
        elif cycle3:
            str="The orbit ended in a 3 cycle"
        else: 
            str= "The orbit not result in an equilibrium or small limit cycle. A limit may exist, try again with a larger iter_limit"
        report = "terminated in {} iterations. {}".format(iter, str)
        return [orbit,iter, eq, cycle2, cycle3,report]
    
    def __F__(self,y):
        ynew = np.zeros(len(y))
        for n in np.arange(0,len(y)):
            argmax = self.__mode__([y[i]for i in list(self.graph.neighbors(n))])
            if y[n] in argmax:
                ynew[n]=y[n]
            else:
                ynew[n]=random.choice(argmax)
        return ynew

    def __mode__(self,array):
        most = max(list(map(array.count, array)))
        return list(set(filter(lambda x: array.count(x) == most, array)))
    
    def get_limit(self):
        if self.eq:
            return self.solution[-1]
        elif self.cycle2:
            return self.solution[-2:]
        elif self.cycle3:
            return self.solution[-3:]
        else:
            print("Orbit has no equilibrium or small limit cycle")
            return self.solution[-5:]
    
    def __animate__(self,framenumber, pos,cmap):
        cols = self.__getcolors__(cmap,framenumber)
        ec=nx.draw_networkx_edges(self.graph,pos)
        nc=nx.draw_networkx_nodes(self.graph, pos, 
                                  nodelist=self.graph.nodes(),
                                  node_color = cols,
                                  node_size = 20)
        title=plt.title('$t={}$'.format(framenumber))
        return(ec,nc,title)

    def animation(self):
        #Start by assigning colors to stratagies
        strats = list(set(self.solution[0]))
        stmax= max(strats)
        hsv = mpl.colormaps['hsv']
        cmap = hsv(np.linspace(0,hsv.N,stmax+1).astype(int))

        cols = self.__getcolors__(cmap,0)
        pos=nx.spring_layout(self.graph)
        fig = plt.figure()
        title =plt.title('$t=0$')
        ec=nx.draw_networkx_edges(self.graph,pos)
        nc = nx.draw_networkx_nodes(self.graph, pos, 
                                    nodelist=self.graph.nodes(),
                                    node_color = cols,
                                    node_size = 20)
        ani = animation.FuncAnimation(fig,self.__animate__, 
                                        frames=self.iter, 
                                        repeat=True,
                                        fargs = (pos,cmap),
                                        blit = True)
        plt.show()

    def __getcolors__(self,cmap,frame):
        y = self.solution[frame]
        n=len(y)
        cols = np.zeros((n,4))
        for ii in np.arange(0,n):
            cols[ii,:]=cmap[y[ii],:]    
        return cols