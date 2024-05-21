import pandas as pd
import numpy as np
import os.path

jobrange = range(0,100)

BroadDf = pd.read_csv("./DataFiles/SCBroadSim_CP0.csv")

for i in jobrange[1:]:
    path = "./DataFiles/SCBroadSim_CP{}.csv".format(i)
    if os.path.isfile(path):
        BroadDf = pd.concat((BroadDf, pd.read_csv(path)))
BroadDf.to_csv("./DataFiles/SCBroadSim_CPComplete.csv", index = False)