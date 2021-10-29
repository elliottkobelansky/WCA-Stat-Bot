import pandas as pd
import re
import numpy as np

dfsingles = pd.read_csv("3bld_stats/RanksSingle.csv")
singlesdata = dfsingles[["personId", "best"]].values
dfaverages = pd.read_csv("3bld_stats/RanksAverage.csv")
averagesdata = dfaverages[["personId", "best"]].values


def wrsingle(message):
    """ Prints the single with a certain world ranking
    """
    rank = int(message[2]) - 1
    # Gets WCA ID (NEED TO CHANGE THIS TO NAME)
    name = singlesdata[rank][0]
    # Need to format this better. Should get time in xx:xx.xx format
    time = '{0:.2f}'.format(int(singlesdata[rank][1]) / 100.0)
    # Print out in nice fashion
    return(f"**WR{rank + 1} Single: {time} by {name}**")

def wraverage(message):
    """ Prints the single with a certain world ranking
    """
    rank = int(message[2]) - 1
    # Gets WCA ID (NEED TO CHANGE THIS TO NAME)
    name = averagesdata[rank][0]
    # Need to format this better. Should get time in xx:xx.xx format
    time = '{0:.2f}'.format(int(averagesdata[rank][1]) / 100.0)
    # Print out in nice fashion
    return(f"**WR{rank + 1} Average: {time} by {name}**")

def timeformat(time):
    """ Takes xx.xx format and adjusts it
        to xx:xx.xx if necessary
    """
    if time < 60:
        pass
    if time > 60:
        pass