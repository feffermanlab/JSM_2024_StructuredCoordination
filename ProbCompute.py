import pandas as pd
import PartitionTools
import argparse

r=100

parser = argparse.ArgumentParser()

parser.add_argument("Run",
                    help = "Which section of the total graph space to sample",
                    type = int)

args = parser.parse_args()


def computeProb(run):
    df = pd.read_csv("./DataFiles/SCBroadSim_MD_C.csv")
    l = df.shape[0]
    start = round(run/r*l)
    end = round((run+1)/r*l)

    df = df.iloc[start:end]
    
    conProb = list()
    for i in range(0,df.shape[0]):
        n = df.iloc[i]['Graph Size']
        p = df.iloc[i]['MeanDegree']/(n-1)
        conProb.append(PartitionTools.ConnectedProb(n,p))
    df.insert(9,"connectedProbability", conProb)

    df.to_csv("./DataFiles/SCBroadSim_CP{}.csv".format(args.Run),index=False)

if __name__ == "__main__":
    computeProb(args.Run)