import pandas as pd
import re
import numpy as np
import time
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request

# Random database stuff
dfsingles = pd.read_csv("3bld_stats/RanksSingle.csv")
singlesdata = dfsingles[["personId", "best", "worldRank"]].values
singlesdict = {row[2]: [row[0], row[1]] for row in singlesdata}


dfaverages = pd.read_csv("3bld_stats/RanksAverage.csv")
averagesdata = dfaverages[["personId", "best"]].values
persons = pd.read_csv("3bld_stats/Persons.csv")
names = persons[["id", "name"]].values
id_to_name_d = {person[0]: person[1] for person in names}
name_to_id_d = {person[1]: person[0] for person in names}

 


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
    name = f"{id_to_name_d[wcaid]} ({wcaid})"
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
    name = f"{id_to_name_d[wcaid]} ({wcaid})"
    # Need to format this better. Should get time in xx:xx.xx 
    time = timeformat('{0:.2f}'.format(int(averagesdata[rank][1]) / 100.0))
    # Print out in nice fashion
    return(f"**WR{rank + 1} Average: {time} by {name}**")

def getimagelink(message):
    """ Scrapes wca website with given ID for profile photo
    """

    # Source: https://pyshark.com/download-images-from-a-web-page-using-python/
    # I have no idea how some of this shit works but it does its job so im not
    # gonna complain
    
    # Wca link based on user request from discord. I still need to change this
    # so that you can just put in a name but that requires some shenanigans so
    # thats for later
    wcaid = message[2]
    url = f"https://www.worldcubeassociation.org/persons/{wcaid}"

    http = httplib2.Http()
    response, content = http.request(url)
    images = BeautifulSoup(content, features='html5lib').find_all('img')
    image_links = []

    for image in images:
        image_links.append(image['src'])

    # prob not a great idea to hardcode this to the 4th item in the array but
    # its always the fourth image for a given wca profile so like :/
    link = image_links[3]
    return(link)

def getname(wcaid):
    return(id_to_name_d[wcaid])
