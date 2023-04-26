import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import random 

class Orbit:
    '''A solution to the IVP for the GTDS


    Attributes
    ----------
        graph : nx.Graph
            the graph on which the IVP is solved 
        solution : list 
            a sequence of colorings, colors are represented as integers
        iter : int
            The length of the solution
        eq : bool
            True if the solution ends in an equilibrium
        cycle2 : bool
            True if the solution ends in a two-cycle
        cycle3 : bool
            True if the solution ends in a three-cycle
        report : str
            A string which describes the solution and its limit. 
    Methods
    ---------
        draw(n=1, dim=None)
            Shows a figure with the final n steps of orbit colored on the graph
        get_limit()
            Returns the last coloring in the orbit it the orbit ends in an equilibrium,
            the last two colorings if the orbit ends in a two-cycle, and the last three
            if the orbit ends in a three-cycle
        animate()
            Shows an animation of the orbit starting from the initial coloring
    '''

    def __init__(self,G,y0=None,iter_limit=5000):
        '''
        Constructs all necessary attributes of the Orbit object
        
        Parameters
        ----------
        G : nx.Graph
            A graph on which to solve the IVP
        y0 : list, optional
            A list of ints of the same length as the number of vertices in G
            which describes the initial color of each vertex
        iter_limit : int, optional
            The upper iteration limit for the __solve()__ function. By default it is
            set to 5000
        '''
        self.graph = G
        result = self.__solve__(y0,iter_limit)
        self.solution = result[0]
        self.iter = result[1]
        self.eq= result[2]
        self.cycle2= result[3]
        self.cycle3= result[4]
        self.report = result[5]

    def draw(self,n=1, dim=None):
        '''
        Draws the last n colorings of the orbit arranged as subplots

        Parameters
        ----------
        n : int, optional
            The number of colorings to be drawn. Given value 1 by default
        dim : tuple, optional
            The dimensions of the subplots as (rows,columns). By default it will be calculated
            to be as close to square as possible
        '''
        #calculate dimensions
        if dim == None:
            r = int(np.floor(np.sqrt(n)))
            c = int(np.ceil(n/r))
        else:
            r=dim[0]
            c=dim[1]
        
        #get position so that each frame uses the same arrangement
        pos=nx.spring_layout(self.graph)

        plt.figure()
        for ii in np.arange(1,n+1):
            plt.subplot(r,c,ii)
            ec=nx.draw_networkx_edges(self.graph,pos)
            nc = nx.draw_networkx_nodes(self.graph, 
                                        pos, 
                                        nodelist=self.graph.nodes(),
                                        node_color = self.solution[-(ii)],
                                        node_size = 20)
        plt.show()

    def __str__(self):
        '''
        A method to return a description of the orbit as a string

        Returns
        --------
        str
        '''
        n=len(self.graph.nodes())
        st= "Starting from a given coloring of a connected graph on {} vertices, the orbit {}".format(n,self.report)
        return st 

    def __solve__(self,y0=None, iter_limit = 5000):
        '''
        A hidden method to find a solution to the IVP given initial data

        parameters
        ----------
        y0 : list
            A list of ints of the same length as the number of vertices in G
            which describes the initial color of each vertex
        iter_limit : int, optional
            The maximum number of steps the solver will take while searching for a limit.
            By default it is given the value 5000

        Returns
        -------
            sol : list
                the sequence of colorings resulting from the initial data and the update rule
            iter : int
                The number of iterations it took to reach a limit
            eq : bool
                True if the solution reached an equilibrium
            cycle2 : bool
                True if the solution reached a 2 cycle
            cycle3 : bool 
                True if the solution reached a 3 cycle
            report : str
                A string describing the solution 
        '''

        #if no initial data is given, give each vertex a different color
        if y0 is None:
            y0 = np.arange(0,len(self.graph.nodes()))
        
        # start solution with initial data
        iter = 0
        sol=list()
        sol.append(y0)
        
        #prepare to check termination conditions
        finished = False
        eq=False
        cycle2 = False
        cycle3=False

        while not finished:
            #Add a new coloring according to the update rule
            sol.append(self.__F__(sol[-1]).astype(int))
            iter=iter+1 
            #Check to see if the solution has reached a limit
            if iter>=19:
                eq = (sol[-1]==sol[-2]).all() and (sol[-1]==sol[-3]).all()
                cycle2 = (sol[-1]==sol[-3]).all() and (sol[-1]==sol[-5]).all() and (sol[-1]==sol[-19]).all()
                cycle3 = (sol[-1]==sol[-4]).all() and (sol[-1]==sol[-7]).all() and (sol[-1]==sol[-19]).all()
            finished = iter>=iter_limit or eq or cycle2 or cycle3

        # Once the solution has reached a limit, build the report 
        if eq:
            str="The orbit ended at an equilibrium"
        elif cycle2:
            str="The orbit ended in a 2 cycle"
        elif cycle3:
            str="The orbit ended in a 3 cycle"
        else: 
            str= "The orbit not result in an equilibrium or small limit cycle. A limit may exist, try again with a larger iter_limit"
        report = "terminated in {} iterations. {}".format(iter, str)

        #return a list of 6 different objects
        return [sol,iter, eq, cycle2, cycle3,report]
    
    def __F__(self,y):
        '''
        A hidden method for generating the next coloring given the current coloring

        Parameters
        ----------
        y : np.array 
            The current coloring of the graph
        
        Returns
        -------
        ynew : np.array
            The vector of best responses to y
        '''
        ynew = np.zeros(len(y))
        for n in np.arange(0,len(y)):
            #get the set of best responses for vertex n
            argmax = self.__mode__([y[i]for i in list(self.graph.neighbors(n))])

            #break ties according to the tie breaking protocol 
            if y[n] in argmax:
                ynew[n]=y[n]
            else:
                ynew[n]=random.choice(argmax)
        return ynew

    def __mode__(self,array):
        '''
        A hidden method for finding the mode of an array

        Parameters
        ----------
        array : iterable
        
        Returns
        --------
        mode : list
            a list of objects which were present the greatest number of times in array
        '''
        most = max(list(map(array.count, array)))
        return list(set(filter(lambda x: array.count(x) == most, array)))
    
    def get_limit(self):
        '''
        A method to retreive the limit of an orbit

        Returns
        --------
        limit : list
            The colorings which together make up the limit of the orbit
        '''
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
        '''
        A hidden method to update the figure in the animate() method

        Parameters
        ----------
        framenumber : int

        pos : artist
            A parameter used to determine the position of the edges and nodes in the frame
        cmap : colormap
            A colormap which associates colors as described by self.soltion to RGB colors.

        Returns
        --------
        ec : Artist 
            The artist object which draws the edges of the graph
        nc : Artist
            The artist object which draws the nodes of the graph
        title : Artist
            The artist object which draws the title of the graph

        '''
        cols = self.__getcolors__(cmap,framenumber)
        ec=nx.draw_networkx_edges(self.graph,pos)
        nc=nx.draw_networkx_nodes(self.graph, pos, 
                                  nodelist=self.graph.nodes(),
                                  node_color = cols,
                                  node_size = 20)
        title=plt.title('$t={}$'.format(framenumber))
        return(ec,nc,title)

    def animation(self):
        '''
        Method to show an animation of the Orbit, starting from the intial condition
        and ending at the limit
        '''

        #Start by assigning colors to stratagies
        strats = list(set(self.solution[0]))
        stmax= max(strats)
        hsv = mpl.colormaps['hsv']
        cmap = hsv(np.linspace(0,hsv.N,stmax+1).astype(int))

        #calls __getcolors__ to get a list of colors from the strategies
        cols = self.__getcolors__(cmap,0)

        #make a position object so each frame has the graph in the same layout
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
        return ani 

    def __getcolors__(self,cmap,frame):
        ''' 
        A hidden method to make a list of RGB from a list step in the soluiton

        Parameters
        ---------
        cmap : colormap
            A colormap associating colors in the solution to actual RGB colors
        frame : int
            The frame number

        Returns
        ---------
        cols : np.array
            A list with the same length as the number of vertices in the graph which associates
            a vertex to an RGB color by the color given in self.solution[frame]
        '''

        y = self.solution[frame]
        n=len(y)
        cols = np.zeros((n,4))
        for ii in np.arange(0,n):
            cols[ii,:]=cmap[y[ii],:]    
        return cols