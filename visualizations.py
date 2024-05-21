import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean 
import PartitionTools



#frequency of admitted partitions
def Fig1():
    g1 = [1,0,0,0,0,0,0,0,0,0]
    g2 = [1,0,0,0,0,0,0,0,0,0]
    g3 = [2,0,0,0,0,0,0,0,0,0]
    g4 = [4,2,0,0,0,0,0,0,0,0]
    g5 = [13,8,0,0,0,0,0,0,0,0]
    g6 = [48,43,13,6,2,0,0,0,0,0]
    g7 = [319,297,128,56,25,15,8,3,1,1]

    normg1 = np.divide(g1,sum(g1))
    normg2 = np.divide(g2,sum(g2))
    normg3 = np.divide(g3,sum(g3))
    normg4 = np.divide(g4,sum(g4))
    normg5 = np.divide(g5,sum(g5))
    normg6 = np.divide(g6,sum(g6))
    normg7 = np.divide(g7,sum(g7))

    X = np.arange(1,11)
    fig = plt.figure()
    ax = plt.gca()
    #pg1, = ax.plot(X , normg1, color = 'b', alpha = 1/7)
    #pg2, = ax.plot(X + 1/7, normg2, color = 'b',  alpha = 2/7)
    #pg3, =ax.plot(X + 2/7, normg3, color = 'b',  alpha = 3/7)
    pg4 =ax.bar(X-3/10, normg4, color = 'b', width = 1/5, alpha = 1/4)
    pg5 =ax.bar(X -1/10, normg5, color = 'b',  width = 1/5, alpha = 2/4)
    pg6 =ax.bar(X + 1/10, normg6, color = 'b', width = 1/5, alpha = 3/4)
    pg7 =ax.bar(X + 3/10, normg7, color = 'b', width = 1/5, alpha = 1)

    plt.xlabel("number of partitions")
    plt.ylabel("proportion of graphs") 
    plt.title("frequency of admitted partitions")
    ax.set_xticks([1,2,3,4,5,6,7,8,9,10], labels = ['1','2','3','4','5','6','7','8','9','10'
    ])
    ax.legend(labels = ["Order 4 - 6 graphs", "Order 5 - 21 graphs", "Order 6 - 112 graphs ", "Order 7 - 853 graphs"])
    plt.show()

    fig = plt.figure()
    ax = plt.gca()
    #pg1, = ax.plot(X , normg1, color = 'b', alpha = 1/7)
    #pg2, = ax.plot(X + 1/7, normg2, color = 'b',  alpha = 2/7)
    #pg3, =ax.plot(X + 2/7, normg3, color = 'b',  alpha = 3/7)
    pg4, =ax.plot(X, normg4, color = 'b', alpha = 1/4)
    pg5, =ax.plot(X , normg5, color = 'b',alpha = 2/4)
    pg6, =ax.plot(X , normg6, color = 'b',alpha = 3/4)
    pg7, =ax.plot(X , normg7, color = 'b', alpha = 1)

    plt.xlabel("number of partitions")
    plt.ylabel("proportion of graphs") 

    ax.legend(labels = ["Order 4 - 6 graphs", "Order 5 - 21 graphs", "Order 6 - 112 graphs ", "Order 7 - 853 graphs"])

    plt.show()

#frequency of partitions with n parts
def Fig2():
    g4 = [6,2,0]
    g5 = [21,8,0]
    g6 = [112,79,16]
    g7 = [858,808,174]

    normg4 = np.divide(g4,sum(g4))
    normg5 = np.divide(g5,sum(g5))
    normg6 = np.divide(g6,sum(g6))
    normg7 = np.divide(g7,sum(g7))

    X = np.arange(1,4)
    fig = plt.figure()
    ax = plt.gca()
    #pg1, = ax.plot(X , normg1, color = 'b', alpha = 1/7)
    #pg2, = ax.plot(X + 1/7, normg2, color = 'b',  alpha = 2/7)
    #pg3, =ax.plot(X + 2/7, normg3, color = 'b',  alpha = 3/7)
    pg4 =ax.bar(X-3/10, normg4, color = 'b', width = 1/5, alpha = 1/4)
    pg5 =ax.bar(X -1/10, normg5, color = 'b',  width = 1/5, alpha = 2/4)
    pg6 =ax.bar(X + 1/10, normg6, color = 'b', width = 1/5, alpha = 3/4)
    pg7 =ax.bar(X + 3/10, normg7, color = 'b', width = 1/5, alpha = 1)

    plt.xlabel("number of parts")
    plt.ylabel("proportion of partitions") 
    plt.title("frequency of partitions with n parts")
    ax.set_xticks([1,2,3], labels = ['1','2','3'])
    ax.legend(labels = ["Order 4 - 8 partitions", "Order 5 - 29 partitions", "Order 6 - 207 partitions ", "Order 7 - 1835 paritions"])
    plt.show()

#Basin of Stability for Consensus Equilibrium by Mean Degree
def Fig3():
    TotalBasindf = pd.read_csv("./DataFiles/SCBasinSimComplete.csv")

    #compute Trivial equilibrium basin size
    sizes = list()
    non_conv_sol = 0
    for i in range(0,len(TotalBasindf['Graph Size'])):
        dist = TotalBasindf.iloc[i]['ClusterDist']
        dist = [int(s.lstrip()) for s in dist[1:-1].split('.')[:-1]]
        sizes.append(dist[1]/sum(dist[1:]))
        non_conv_sol = non_conv_sol+dist[0]

    TotalBasindf.insert(7,"BasinSize",sizes)

    print("Thre are {} non convergent solutions".format(non_conv_sol))
    #compute MeanDegree
    meanDegree = list()
    for i in range(0,len(TotalBasindf['Graph Size'])):
        ddist = TotalBasindf.iloc[i]['DegreeSequence']
        ddist = [int(s) for s in ddist[1:-1].split(',')]
        meanDegree.append(mean(ddist))
    TotalBasindf.insert(5, "MeanDegree", meanDegree)

    S50Basindf = TotalBasindf[TotalBasindf['Graph Size']==50]
    S100Basindf = TotalBasindf[TotalBasindf['Graph Size']==100]
    S150Basindf = TotalBasindf[TotalBasindf['Graph Size']==150]
    S200Basindf = TotalBasindf[TotalBasindf['Graph Size']==200]
    S400Basindf = TotalBasindf[TotalBasindf['Graph Size']==400]
    
    #print(S50Basindf)

    fig = plt.figure()
    ax = fig.gca()

    l50 = ax.scatter(S50Basindf['ED'],S50Basindf['BasinSize'], c = "b")
    l100 = ax.scatter(S100Basindf['ED'],S100Basindf['BasinSize'], c = "r")
    l150 = ax.scatter(S150Basindf['ED'],S150Basindf['BasinSize'], c = "orange")
    l200 = ax.scatter(S200Basindf['ED'],S200Basindf['BasinSize'], c = "g")
    l400 = ax.scatter(S400Basindf['ED'],S400Basindf['BasinSize'], c = "violet")

    plt.xlabel("Edge Density")
    plt.ylabel("Relative size of basin of stability") 
    plt.title("Basin of Stability for Consensus Equilibrium by Edge Density")

    ax.legend(labels = ["50", "100", "150 ", "200", "400"], title = "Graph Order")
    plt.show()

    fig = plt.figure()
    ax = fig.gca()

    l50 = ax.scatter(S50Basindf['NormED'],S50Basindf['BasinSize'], c = "b")
    l100 = ax.scatter(S100Basindf['NormED'],S100Basindf['BasinSize'], c = "r")
    l150 = ax.scatter(S150Basindf['NormED'],S150Basindf['BasinSize'], c = "orange")
    l200 = ax.scatter(S200Basindf['NormED'],S200Basindf['BasinSize'], c = "g")
    l400 = ax.scatter(S400Basindf['NormED'],S400Basindf['BasinSize'], c = "violet")
    plt.show()

    fig = plt.figure()
    ax = fig.gca()

    l50 = ax.scatter(S50Basindf['MeanDegree'],S50Basindf['BasinSize'], c = "b")
    l100 = ax.scatter(S100Basindf['MeanDegree'],S100Basindf['BasinSize'], c = "r")
    l150 = ax.scatter(S150Basindf['MeanDegree'],S150Basindf['BasinSize'], c = "orange")
    l200 = ax.scatter(S200Basindf['MeanDegree'],S200Basindf['BasinSize'], c = "g")
    l400 = ax.scatter(S400Basindf['MeanDegree'],S400Basindf['BasinSize'], c = "violet")

    plt.xlabel("Mean Degree")
    plt.ylabel("Relative size of Basin of Stability") 
    plt.title("Basin of Stability for Consensus Equilibrium by Mean Degree")

    ax.legend(labels = ["50", "100", "150 ", "200", "400"], title = "Graph Order")
    plt.show()
    
    
def Fig3A():
    TotalBasindf = pd.read_csv("./DataFiles/SCBasinSim_CP.csv")
    S50Basindf = TotalBasindf[TotalBasindf['Graph Size']==50]
    S100Basindf = TotalBasindf[TotalBasindf['Graph Size']==100]
    S150Basindf = TotalBasindf[TotalBasindf['Graph Size']==150]
    S200Basindf = TotalBasindf[TotalBasindf['Graph Size']==200]
    S400Basindf = TotalBasindf[TotalBasindf['Graph Size']==400]
    
    fig = plt.figure()
    ax = fig.gca()

    z50 = np.polyfit(10**(S50Basindf['connectedProbability']),10**(S50Basindf['BasinSize']),1)
    p50 = np.poly1d(z50)

    z100 = np.polyfit(10**(S100Basindf['connectedProbability']),10**(S100Basindf['BasinSize']),1)
    p100 = np.poly1d(z100)

    z150 = np.polyfit(10**(S150Basindf['connectedProbability']),10**(S150Basindf['BasinSize']),1)
    p150 = np.poly1d(z150)

    z200 = np.polyfit(10**(S200Basindf['connectedProbability']),10**(S200Basindf['BasinSize']),1)
    p200 = np.poly1d(z200)
    
    z400 = np.polyfit(10**(S400Basindf['connectedProbability']),10**(S400Basindf['BasinSize']),1)
    p400 = np.poly1d(z400)

    l50 = ax.scatter(10**(S50Basindf['connectedProbability']),10**(S50Basindf['BasinSize']), c = "b")
    l100 = ax.scatter(10**(S100Basindf['connectedProbability']),10**(S100Basindf['BasinSize']), c = "r")
    l150 = ax.scatter(10**S150Basindf['connectedProbability'],10**(S150Basindf['BasinSize']), c = "orange")
    l200 = ax.scatter(10**S200Basindf['connectedProbability'],10**S200Basindf['BasinSize'], c = "g")
    l400 = ax.scatter(10**S400Basindf['connectedProbability'],10**S400Basindf['BasinSize'], c = "violet")
    plt.plot(10**(S50Basindf['connectedProbability']),p50(10**(S50Basindf['connectedProbability'])),c="b")
    plt.plot(10**(S100Basindf['connectedProbability']),p100(10**(S100Basindf['connectedProbability'])),c="r")
    plt.plot(10**(S150Basindf['connectedProbability']),p150(10**(S150Basindf['connectedProbability'])),c="orange")
    plt.plot(10**(S200Basindf['connectedProbability']),p200(10**(S200Basindf['connectedProbability'])),c="g")
    plt.plot(10**(S400Basindf['connectedProbability']),p400(10**(S400Basindf['connectedProbability'])),c="violet")

    plt.xlabel("Probability of Connectedness")
    plt.ylabel("Relative size of Basin of Stability") 
    plt.title("Basin of Stability for Consensus Equilibrium by Probability of Connectedness")

    xtics = np.linspace(1,10,5)
    xticlabs = [np.round(np.log10(item),2) for item in xtics ]
    plt.xticks(ticks = xtics, labels= xticlabs)

    ytics = np.linspace(1,10, 5)
    yticlabs = [np.round(np.log10(item),2) for item in ytics ]
    plt.yticks(ticks = ytics, labels= yticlabs)

    plt.ylim(1,10)
    plt.xlim(1,10)

    ax.legend(labels = ["50", "100", "150 ", "200", "400"], title = "Graph Order")
    plt.show()   

#Mean Cluster Number by Graph Diameter
def Fig4():
    TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSimComplete.csv")
    fig = plt.figure()
    ax = fig.gca()

    X = range(2,9)
    Y1 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(50,99)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        Y1. append(mean(tempdf["ClusterNumber"]))  

    Y2 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(100,149)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        if not tempdf.empty: Y2. append(mean(tempdf["ClusterNumber"]))  
        else: Y2.append(np.nan)

    Y3 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(150,199)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        if not tempdf.empty: Y3. append(mean(tempdf["ClusterNumber"])) 
        else: Y3.append(np.nan)

    Y4 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(200,249)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        if not tempdf.empty: Y4. append(mean(tempdf["ClusterNumber"])) 
        else: Y4.append(np.nan)

    Y5 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(250,299)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        if not tempdf.empty: Y5. append(mean(tempdf["ClusterNumber"])) 
        else: Y5.append(np.nan)


    Y6 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(300,349)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        if not tempdf.empty: Y6. append(mean(tempdf["ClusterNumber"])) 
        else: Y6.append(np.nan)

    Y7 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(350,399)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        if not tempdf.empty: Y7. append(mean(tempdf["ClusterNumber"])) 
        else: Y7.append(np.nan)

    Y8 = list()
    for x in X:
        tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(400,450)]
        tempdf = tempdf[tempdf["Diameter"]== x]
        if not tempdf.empty: Y8. append(mean(tempdf["ClusterNumber"])) 
        else: Y8.append(np.nan)
    
    plt.xlabel( "Graph Diameter")
    plt.ylabel("Mean Cluster Number")
    plt.title("Mean Cluster Number by Graph Diameter")

    s1 = ax.plot(X, Y1)
    s2 = ax.plot(X, Y2)
    s3 = ax.plot(X, Y3)
    s4 = ax.plot(X, Y4)
    s5 = ax.plot(X, Y5)
    s6 = ax.plot(X, Y6)
    s7 = ax.plot(X, Y7)
    s8 = ax.plot(X, Y8)


    ax.legend(title = "Graph Order", labels = ["50-99","100-149","150-199","200-249","250-299","300-349","350-399","400-450"])
   
    plt.show()

#Cluster Number by Edge Density
def Fig5():

    #TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSimComplete.csv")
    TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSim_MD_C.csv")

    Total = TotalBroaddf.shape[0]

    eq = (TotalBroaddf[TotalBroaddf["EQ"]]).shape[0]
    print(eq)
    
    cycle2 = (TotalBroaddf[TotalBroaddf["Cycle2"]]).shape[0]
    print(cycle2)

    cycle3 = (TotalBroaddf[TotalBroaddf["Cycle3"]]).shape[0]
    print(cycle3)

    cycle4 = (TotalBroaddf[TotalBroaddf["Cycle4"]]).shape[0]
    print(cycle4)

    non_conv = Total - eq - cycle2 - cycle3 - cycle4 
    print(non_conv)

    fig = plt.figure()
    ax = fig.gca()

    p1 = ax.scatter(TotalBroaddf["ED"], TotalBroaddf["ClusterNumber"],c=TotalBroaddf["Graph Size"])

    ax.text(0.32, 18, 'n = {} \nEquilibria = {} \n2-cycles = {} \n3-cycles = {} \n4-cycles = {} \nnon convergent = {}'.format(Total,eq,cycle2,cycle3,cycle4,non_conv), style='italic',
        bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})


    plt.xlabel( "Edge Density")
    plt.ylabel("Cluster Number")
    plt.title("Cluster Number by Edge Density")

    fig.colorbar(p1, label = "Graph Order")
    plt.show()

    # EQdf = TotalBroaddf[TotalBroaddf["EQ"]]
    # fig = plt.figure()
    # ax = fig.gca()

    # p1 = ax.scatter(EQdf["ED"], EQdf["ClusterNumber"],c=EQdf["Graph Size"])

    # plt.xlabel( "Edge Density")
    # plt.ylabel("Cluster Number")
    # plt.title("Cluster Number by Edge Density (among equilibria)")

    # fig.colorbar(p1, label = "Graph Order")
    # #plt.show()

    # c2df = TotalBroaddf[TotalBroaddf["Cycle2"]]
    # fig = plt.figure()
    # ax = fig.gca()

    # p1 = ax.scatter(c2df["ED"], c2df["ClusterNumber"],c=c2df["Graph Size"])

    # plt.xlabel( "Edge Density")
    # plt.ylabel("Cluster Number")
    # plt.title("Cluster Number by Edge Density (among 2-cycles)")

    # fig.colorbar(p1, label = "Graph Order")
    #plt.show()

#Cluster Number by Mean Degree
def Fig6():
    #TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSimComplete.csv")
    
    #meanDegree = list()
    #for i in range(0,len(TotalBroaddf['Graph Size'])):
    #    ddist = TotalBroaddf.iloc[i]['DegreeSequence']
    #    ddist = [int(s) for s in ddist[1:-1].split(',')]
    #    meanDegree.append(mean(ddist))
    #TotalBroaddf.insert(5, "MeanDegree", meanDegree)

    #TotalBroaddf.to_csv("./DataFiles/SCBroadSimWithMeanDegree.csv")
    #TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSimWithMeanDegree.csv")
    TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSim_MD_C.csv")
    
    Total = TotalBroaddf.shape[0]   
    
    eq = (TotalBroaddf[TotalBroaddf["EQ"]]).shape[0]
    print(eq)
    
    cycle2 = (TotalBroaddf[TotalBroaddf["Cycle2"]]).shape[0]
    print(cycle2)

    cycle3 = (TotalBroaddf[TotalBroaddf["Cycle3"]]).shape[0]
    print(cycle3)

    cycle4 = (TotalBroaddf[TotalBroaddf["Cycle4"]]).shape[0]
    print(cycle4)

    non_conv = Total - eq - cycle2 - cycle3 - cycle4 
    print(non_conv)

    fig = plt.figure()
    ax = fig.gca()

    p1 = ax.scatter(TotalBroaddf["MeanDegree"], TotalBroaddf["ClusterNumber"],c=TotalBroaddf["Graph Size"])

    ax.text(17, 18, 'n = {} \nEquilibria = {} \n2-cycles = {} \n3-cycles = {} \n4-cycles = {} \nnon convergent = {}'.format(Total,eq,cycle2,cycle3,cycle4,non_conv), style='italic',
        bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})


    plt.xlabel( "Mean Degree")
    plt.ylabel("Cluster Number")
    plt.title("Cluster Number by Mean Degree")

    fig.colorbar(p1, label = "Graph Order")
    plt.show()

#Cluster Number by Centralization
def Fig7():
   # TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSimWithMeanDegree.csv")
    
    #centralization = list()
    #for i in range(0,len(TotalBroaddf['Graph Size'])):
    #    ddist = TotalBroaddf.iloc[i]['DegreeSequence']
    #    ddist = [int(s) for s in ddist[1:-1].split(',')]
    #    centralization.append(np.std(ddist))
    #TotalBroaddf.insert(6, "Centralization", centralization)

    #TotalBroaddf.to_csv("./DataFiles/SCBroadSim_MD_C.csv")

    TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSim_MD_C.csv")

    Total = TotalBroaddf.shape[0]  
    
    eq = (TotalBroaddf[TotalBroaddf["EQ"]]).shape[0]
    print(eq)
    
    cycle2 = (TotalBroaddf[TotalBroaddf["Cycle2"]]).shape[0]
    print(cycle2)

    cycle3 = (TotalBroaddf[TotalBroaddf["Cycle3"]]).shape[0]
    print(cycle3)

    cycle4 = (TotalBroaddf[TotalBroaddf["Cycle4"]]).shape[0]
    print(cycle4)

    non_conv = Total - eq - cycle2 - cycle3 - cycle4 
    print(non_conv)


    fig = plt.figure()
    ax = fig.gca()

    p1 = ax.scatter(TotalBroaddf["Centralization"], TotalBroaddf["ClusterNumber"],c=TotalBroaddf["Graph Size"])

    ax.text(4.25, 18, 'n = {} \nEquilibria = {} \n2-cycles = {} \n3-cycles = {} \n4-cycles = {} \nnon convergent = {}'.format(Total,eq,cycle2,cycle3,cycle4,non_conv), style='italic',
        bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})

    plt.xlabel( "Centralization")
    plt.ylabel("Cluster Number")
    plt.title("Cluster Number by Centralization")

    fig.colorbar(p1, label = "Graph Order")
    plt.show()

#Heat map of Equilibrium Proportion    
def Fig8():
    TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSim_MD_C.csv")

    minissimumMD = min(TotalBroaddf["MeanDegree"])
    maxissimumMD = max(TotalBroaddf["MeanDegree"])
    xres =40
    yres =40

    X = np.zeros((yres,xres))
    for i in range(0,xres):
        print(i)
        for j in range(0,xres):
            minsize = 50+(i/yres)*400
            maxsize = 50+((i+1)/yres)*400
            minMD = minissimumMD+(j/xres)*(maxissimumMD-minissimumMD)
            maxMD = minissimumMD+((j+1)/xres)*(maxissimumMD-minissimumMD)
            Tempdf = TotalBroaddf[TotalBroaddf["Graph Size"].between(minsize,maxsize,inclusive="left")]
            Tempdf = Tempdf[Tempdf["MeanDegree"].between(minMD,maxMD,inclusive="left")]
            if not Tempdf.empty: X[yres -1-i,j]= Tempdf[Tempdf["EQ"]].shape[0]/Tempdf.shape[0]
            else: X[yres-1-i,j]=np.nan 
    print(X)

    fig = plt.figure()
    ax = fig.gca()

    p1 = ax.imshow(X)

    Y = np.linspace(50,450,1000)
    X1= [((np.log(y)-np.log(-np.log(0.1)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X2= [((np.log(y)-np.log(-np.log(0.2)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X3= [((np.log(y)-np.log(-np.log(0.3)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X4= [((np.log(y)-np.log(-np.log(0.4)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X5= [((np.log(y)-np.log(-np.log(0.5)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X6= [((np.log(y)-np.log(-np.log(0.6)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X7= [((np.log(y)-np.log(-np.log(0.7)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X8= [((np.log(y)-np.log(-np.log(0.8)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X9= [((np.log(y)-np.log(-np.log(0.9)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]

    ploty = [(450-y)*yres/400 for y in Y]

    l1  = ax.plot(X1, ploty, c='k')
    l2  = ax.plot(X2, ploty, c='k')
    l3  = ax.plot(X3, ploty, c='k')
    l4  = ax.plot(X4, ploty, c='k')
    l5  = ax.plot(X5, ploty, c='k')
    l6  = ax.plot(X6, ploty, c='k')
    l7  = ax.plot(X7, ploty, c='k')
    l8  = ax.plot(X8, ploty, c='k')
    l9  = ax.plot(X9, ploty, c='k')

    xtics = np.linspace(-0.5,xres-0.5, 5)
    xticlabs = [np.round(minissimumMD + item /xres*(maxissimumMD-minissimumMD)) for item in xtics ]
    plt.xticks(ticks = xtics, labels= xticlabs)

    ytics = np.linspace(-0.5,yres-0.5, 5)
    yticlabs = [np.round(450 - item /yres*(400)) for item in np.linspace(0,yres,5) ]
    plt.yticks(ticks = ytics, labels= yticlabs)

    plt.ylim(yres-0.5,-0.5)

    plt.xlabel("Mean Degree")
    plt.ylabel("Graph Order")
    plt.title("Heat map of Equilibrium Proportion")

    fig.colorbar(p1, label = "Equilibrium Proportion")

    plt.show()

    #showing 4 cycles
    ncdf = TotalBroaddf[TotalBroaddf["EQ"]==False]
    ncdf = ncdf[ncdf["Cycle2"]==False]
    c4x = [xres*(item-minissimumMD)/(maxissimumMD-minissimumMD)for item in ncdf["MeanDegree"]]
    c4y = [yres*(450-item)/400 for item in ncdf["Graph Size"]]

    fig = plt.figure()
    ax = fig.gca()

    p1 = ax.imshow(X)
    p2 = ax.scatter(c4x,c4y,c='black', s = 1)

    xtics = np.linspace(-0.5,xres-0.5, 5)
    xticlabs = [np.round(minissimumMD + item /xres*(maxissimumMD-minissimumMD)) for item in xtics ]
    plt.xticks(ticks = xtics, labels= xticlabs)

    ytics = np.linspace(-0.5,yres-0.5, 5)
    yticlabs = [np.round(450 - item /yres*(400)) for item in np.linspace(0,yres,5) ]
    plt.yticks(ticks = ytics, labels= yticlabs)
    plt.ylim(yres-0.5,-0.5)
    plt.xlabel("Mean Degree")
    plt.ylabel("Graph Order")
    plt.title("Heat map of Equilibrium Proportion (with non-convergent solutions)")

    fig.colorbar(p1, label = "Equilibrium Proportion")

    plt.show()

#Heat map of Cluster Number
def Fig9():
    TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSim_MD_C.csv")
    Stabledf = TotalBroaddf[TotalBroaddf["Cycle4"]==False]


    minissimumMD = min(Stabledf["MeanDegree"])
    maxissimumMD = max(Stabledf["MeanDegree"])
    xres =60
    yres =60

    X = np.zeros((yres,xres))
    for i in range(0,xres):
        print(i)
        for j in range(0,xres):
            minsize = 50+(i/yres)*400
            maxsize = 50+((i+1)/yres)*400
            minMD = minissimumMD+(j/xres)*(maxissimumMD-minissimumMD)
            maxMD = minissimumMD+((j+1)/xres)*(maxissimumMD-minissimumMD)
            Tempdf = Stabledf[Stabledf["Graph Size"].between(minsize,maxsize,inclusive="left")]
            Tempdf = Tempdf[Tempdf["MeanDegree"].between(minMD,maxMD,inclusive="left")]
            if not Tempdf.empty:
                X[yres-1-i,j]= mean(Tempdf["ClusterNumber"])
            else: X[yres-1-i,j]=np.nan 
    print(X)

    fig = plt.figure()
    ax = fig.gca()

    p1 = ax.imshow(X)

    Y = np.linspace(50,450,1000)
    X1= [((np.log(y)-np.log(-np.log(0.1)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X2= [((np.log(y)-np.log(-np.log(0.2)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X3= [((np.log(y)-np.log(-np.log(0.3)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X4= [((np.log(y)-np.log(-np.log(0.4)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X5= [((np.log(y)-np.log(-np.log(0.5)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X6= [((np.log(y)-np.log(-np.log(0.6)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X7= [((np.log(y)-np.log(-np.log(0.7)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X8= [((np.log(y)-np.log(-np.log(0.8)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X9= [((np.log(y)-np.log(-np.log(0.9)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]

    ploty = [(450-y)*yres/400 for y in Y]

    l1  = ax.plot(X1, ploty, c='w')
    l2  = ax.plot(X2, ploty, c='w')
    l3  = ax.plot(X3, ploty, c='w')
    l4  = ax.plot(X4, ploty, c='w')
    l5  = ax.plot(X5, ploty, c='w')
    l6  = ax.plot(X6, ploty, c='w')
    l7  = ax.plot(X7, ploty, c='w')
    l8  = ax.plot(X8, ploty, c='w')
    l9  = ax.plot(X9, ploty, c='w')

    xtics = np.linspace(-0.5,xres-0.5, 5)
    xticlabs = [np.round(minissimumMD + item /xres*(maxissimumMD-minissimumMD)) for item in xtics ]
    plt.xticks(ticks = xtics, labels= xticlabs)

    ytics = np.linspace(-0.5,yres-0.5, 5)
    yticlabs = [np.round(450 - item /yres*(400)) for item in np.linspace(0,yres,5) ]
    plt.yticks(ticks = ytics, labels= yticlabs)

    plt.ylim(yres-0.5,-0.5)

    plt.xlabel("Mean Degree")
    plt.ylabel("Graph Order")
    plt.title("Heat map of Average Cluster Number")

    fig.colorbar(p1, label = "Average Cluster Number")

    plt.show()
    

def Fig10():
        #TotalBroaddf=pd.read_csv("./DataFiles/SCBroadSim_CPComplete.csv")
    #conProb = list()
    #for i in range(0,len(TotalBroaddf['Graph Size'])):
       # n = TotalBroaddf.iloc[i]['Graph Size']
      #  p = TotalBroaddf.iloc[i]['MeanDegree']/(n-1)
     #   conProb.append(PartitionTools.ConnectedProb(n,p))
    #TotalBroaddf.insert(9,"connectedProbability", conProb)

    #TotalBroaddf.to_csv("./DataFiles/SCBroadSim_CP.csv")
    TotalBroaddf = pd.read_csv("./DataFiles/SCBroadSim_CPComplete.csv")
    Stabledf = TotalBroaddf[TotalBroaddf["Cycle4"]==False]


    minissimumMD = min(Stabledf["MeanDegree"])
    maxissimumMD = max(Stabledf["MeanDegree"])
    xres =60
    yres =60

    X = np.zeros((yres,xres))
    for i in range(0,xres):
        print(i)
        for j in range(0,xres):
            minsize = 50+(i/yres)*400
            maxsize = 50+((i+1)/yres)*400
            minMD = minissimumMD+(j/xres)*(maxissimumMD-minissimumMD)
            maxMD = minissimumMD+((j+1)/xres)*(maxissimumMD-minissimumMD)
            Tempdf = Stabledf[Stabledf["Graph Size"].between(minsize,maxsize,inclusive="left")]
            Tempdf = Tempdf[Tempdf["MeanDegree"].between(minMD,maxMD,inclusive="left")]
            if not Tempdf.empty:
                X[yres-1-i,j]= mean(Tempdf["connectedProbability"])
            else: X[yres-1-i,j]=np.nan 
    print(X)

    fig = plt.figure()
    ax = fig.gca()

    p1 = ax.imshow(X)

    Y = np.linspace(50,450,1000)
    X1= [((np.log(y)-np.log(-np.log(0.1)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X2= [((np.log(y)-np.log(-np.log(0.2)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X3= [((np.log(y)-np.log(-np.log(0.3)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X4= [((np.log(y)-np.log(-np.log(0.4)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X5= [((np.log(y)-np.log(-np.log(0.5)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X6= [((np.log(y)-np.log(-np.log(0.6)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X7= [((np.log(y)-np.log(-np.log(0.7)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X8= [((np.log(y)-np.log(-np.log(0.8)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]
    X9= [((np.log(y)-np.log(-np.log(0.9)))-minissimumMD)*xres/(maxissimumMD-minissimumMD) for y in Y]

    ploty = [(450-y)*yres/400 for y in Y]

    l1  = ax.plot(X1, ploty, c='k')
    l2  = ax.plot(X2, ploty, c='k')
    l3  = ax.plot(X3, ploty, c='k')
    l4  = ax.plot(X4, ploty, c='k')
    l5  = ax.plot(X5, ploty, c='k')
    l6  = ax.plot(X6, ploty, c='k')
    l7  = ax.plot(X7, ploty, c='k')
    l8  = ax.plot(X8, ploty, c='k')
    l9  = ax.plot(X9, ploty, c='k')

    xtics = np.linspace(-0.5,xres-0.5, 5)
    xticlabs = [np.round(minissimumMD + item /xres*(maxissimumMD-minissimumMD)) for item in xtics ]
    plt.xticks(ticks = xtics, labels= xticlabs)

    ytics = np.linspace(-0.5,yres-0.5, 5)
    yticlabs = [np.round(450 - item /yres*(400)) for item in np.linspace(0,yres,5) ]
    plt.yticks(ticks = ytics, labels= yticlabs)


    plt.ylim(yres-0.5,-0.5)


    plt.xlabel("Mean Degree")
    plt.ylabel("Graph Order")
    plt.title("Heat map of probability of connectedness")

    fig.colorbar(p1, label = "probability of connectedness")

    plt.show()

#def connectProb():
    #calculate connected probability on Basin Data
    # TotalBasindf = pd.read_csv("./DataFiles/SCBasinSimComplete.csv")

    # #compute Trivial equilibrium basin size
    # sizes = list()
    # non_conv_sol = 0
    # for i in range(0,len(TotalBasindf['Graph Size'])):
    #     dist = TotalBasindf.iloc[i]['ClusterDist']
    #     dist = [int(s.lstrip()) for s in dist[1:-1].split('.')[:-1]]
    #     sizes.append(dist[1]/sum(dist[1:]))
    #     non_conv_sol = non_conv_sol+dist[0]

    # TotalBasindf.insert(7,"BasinSize",sizes)

    # print("Thre are {} non convergent solutions".format(non_conv_sol))
    # #compute MeanDegree
    # meanDegree = list()
    # for i in range(0,len(TotalBasindf['Graph Size'])):
    #     ddist = TotalBasindf.iloc[i]['DegreeSequence']
    #     ddist = [int(s) for s in ddist[1:-1].split(',')]
    #     meanDegree.append(mean(ddist))
    # TotalBasindf.insert(5, "MeanDegree", meanDegree)

    # conProb = list()
    # for i in range(0,len(TotalBasindf['Graph Size'])):
    #     n = TotalBasindf.iloc[i]['Graph Size']
    #     p = TotalBasindf.iloc[i]['MeanDegree']/(n-1)
    #     conProb.append(PartitionTools.ConnectedProb(n,p))
    # TotalBasindf.insert(9,"connectedProbability", conProb)

    # TotalBasindf.to_csv("./DataFiles/SCBasinSim_CP.csv")
    # print('Basin Simulation Complete')




#connectProb()
        
#Fig3A()

#Fig3()
#Fig4()
#Fig5()
#Fig6()
#Fig7()
#Fig8()
Fig9()
#Fig10()