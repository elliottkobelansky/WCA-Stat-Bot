import pandas as pd
import re
import numpy as np
import time

# Random database stuff
dfsingles = pd.read_csv("3bld_stats/RanksSingle.csv")
singlesdata = dfsingles[["personId", "best"]].values
dfaverages = pd.read_csv("3bld_stats/RanksAverage.csv")
averagesdata = dfaverages[["personId", "best"]].values
persons = pd.read_csv("3bld_stats/Persons.csv")
names = persons[["id", "name"]].values
namesdict = {person[0]: person[1] for person in names}
 


def timeformat(solvetime):
    """ Takes xx.xx format and adjusts it
        to xx:xx.xx if necessary
    """
    solvetime = float(solvetime)
    # Do nothing if number is less than one minute
    if float(solvetime) < 60.00:
        return('{0:.2f}'.format(solvetime))

    # Format m:s.ms if more than a minute
    if float(solvetime) >= 60.00:
        # Miliseconds (this should be centiseconds but im lazy to change)
        solvetime_ms = int(round(solvetime - int(solvetime), 2) * 100)
        # Add leading 0 if necessary
        if solvetime_ms < 10:
            solve_time_ms = f"0{solvetime_ms}"
        # Seconds (without ms)
        solvetime_s = int(solvetime) % 60
        # Add leading 0 if seconds bad
        if solvetime_s < 10:
            solvetime_s = f"0{solvetime_s}"
        # Minutes
        solvetime_m = int(int(solvetime) / 60)
        return(f"{solvetime_m}:{solvetime_s}.{solvetime_ms}")

def wrsingle(message):
    """ Prints the single with a certain world ranking
    """
    rank = int(message[2]) - 1
    # Gets name from WCA ID
    wcaid = singlesdata[rank][0]
    name = f"{namesdict[wcaid]} ({wcaid})"
    # Need to format this better. Should get time in xx:xx.xx format
    time = timeformat('{0:.2f}'.format(int(singlesdata[rank][1]) / 100.0))
    # Print out in nice fashion
    return(f"**WR{rank + 1} Single: {time} by {name}**")

def wraverage(message):
    """ Prints the single with a certain world ranking
    """
    rank = int(message[2]) - 1
    # Gets WCA ID (NEED TO CHANGE THIS TO NAME)
    wcaid = averagesdata[rank][0]
    name = f"{namesdict[wcaid]} ({wcaid})"
    # Need to format this better. Should get time in xx:xx.xx format
    time = timeformat('{0:.2f}'.format(int(averagesdata[rank][1]) / 100.0))
    # Print out in nice fashion
    return(f"**WR{rank + 1} Average: {time} by {name}**")

