import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

Fig2()