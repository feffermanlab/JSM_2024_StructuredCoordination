# Scructured Coordination

This repository contains a collection of tools for the analysis of an n-player, n-strategy coordination game on a network with neutral options. 
Considering the game as a dynamical system we describe orbits, equilibria, and stability.  

The Class Orbit is a (non-unique) solution to the initial value problem. Given a initial strategy profile (which will
later be thought of as partitions) and a graph, an instance of the class is produced by solving the IVP
with the best response replicator dynamic. The solution is a list of arrays which represent the strategy
each vertex in the graph is taking on at that time step. 

Using the Orbit class we can describe equilibrium partitions (which are those partitions corresponding to
equilibrium strategy profiles). SCCatalogue.py runs a script to find all equilibrium partitions among
connected graphs in the networkx Graph Atlas. 

SCBasinSim is a script which generates a random array of graphs and estimates the size of the basin of 
stability for the consensus equilibrium It has been parallelized to be run with the shell script JobBasinSim.srun.sh
Likewise, SCBroadSim is a script which generates a random array of graphs and measures their limiting behavior.
It also has been parallelized to run with the shell script JobBroadSim.srun.sh.
The python script and shell script DataCollect.py and JobDataCollect.srun.sh take the slices of simulation data from the
simulations mentioned above are compile it into one process. 

PartitionTools.py is a collection of tools which are used in the simulations to measure partitions

SCCatalogue, SCBasinSim, SCBroadSim, and PartitionTools all depend on orbit
SCBasinSim and SCBroadSim depend on PartitionTools

The Jupiter Notebook McAlisterProjectDemo.ipynb steps through the functionality of the orbit class. 
(note the visualizations are not supported on when run in VScode)
