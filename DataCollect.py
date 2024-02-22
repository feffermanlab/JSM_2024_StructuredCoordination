import pandas as pd
import numpy as np
import os.path

jobrange = range(0,100)
BasinDf = pd.read_csv("./DataFiles/SCBasinResults0.csv")

for i in jobrange[1:]:
    path = "./DataFiles/SCBasinResults{}.csv".format(i)
    if os.path.isfile(path):
        BasinDf = pd.concat((BasinDf, pd.read_csv(path)))
BasinDf.to_csv("./DataFiles/SCBasinSimComplete.csv", index = False)


BroadDf = pd.read_csv("./DataFiles/SCBroadSim0.csv")

for i in jobrange[1:]:
    path = "./DataFiles/SCBroadSim{}.csv".format(i)
    if os.path.isfile(path):
        BasinDf = pd.concat((BasinDf, pd.read_csv(path)))
BasinDf.to_csv("./DataFiles/SCBroadSimComplete.csv", index = False)