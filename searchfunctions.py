import pandas as pd
import re
import numpy as np
import time
import subprocess
from emoji import emojize

# Random database stuff
dfsingles = pd.read_csv("3bld_stats/RanksSingle.csv")
singlesdata = dfsingles[["personId", "best", 
                         "worldRank", "countryRank"]].values
singlesdict = {row[2]: [row[0], row[1]] for row in singlesdata}


dfaverages = pd.read_csv("3bld_stats/RanksAverage.csv")
averagesdata = dfaverages[["personId", "best", 
                           "worldRank", "countryRank"]].values
persons = pd.read_csv("3bld_stats/Persons.csv")
names = persons[["id", "name", "countryId"]].values
id_to_name_d = {person[0]: person[1] for person in names}
id_to_country_d = {person[0]: person[2] for person in names}
name_to_id_d = {person[1]: person[0] for person in names}

dfcountries = pd.read_csv("3bld_stats/Countries.csv")
countries = dfcountries[["id", "iso2"]].values
countryd = {country[0]: country[1] for country in countries}

def timeformat(time):
    """ Takes xxxx format and adjusts it
        to xx:xx.xx if necessary
    """

    solvetime = float('{0:.2f}'.format(int(time) / 100.0))
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

def get_wr_result(message):
    """ Prints the result with a certain world ranking
    """
    rank = int(message[2]) - 1
    # Depending on if single or mean is requested, get wcaid, time, solvetype
    if message[3].lower() in ["single", "sg", "s"]:
        wcaid = singlesdata[rank][0]
        time = timeformat(singlesdata[rank][1])
        solvetype = "Single"
    if message[3].lower() in ["average", "mean", "mn", "a", "m", "avg"]:
        wcaid = averagesdata[rank][0]
        time = timeformat(averagesdata[rank][1])
        solvetype = "Average"

    # Gets name from wcaid
    name = id_to_name_d[wcaid]

    # Thought a dict would be a good thing to use for this
    return({"rank": rank + 1, "time": time, "name": name, "wcaid": wcaid, 
            "solvetype": solvetype, "ranktype": "WR", "country": ""})

def get_nr_result(message):
    """ Prints the result with a certain national ranking
    """
    rank = int(message[2])
    country = " ".join(message[4:]).lower()

    # This can probably be combined into one function so that it doesnt have 
    # to repeat in the search functions
    if message[3].lower() in ["single", "sg", "s"]:
        for row in singlesdata:
            if (getcountry(row[0]).lower() == country and int(row[3]) == rank):
                    wcaid = row[0]
                    time = timeformat(row[1])
                    solvetype = "Single"
                    country = getcountry(wcaid)
                    break
    elif message[3].lower() in ["average", "mean", "mn", 
                                "a", "m", "avg"]: 
        for row in averagesdata:
            if (getcountry(row[0]).lower() == country and int(row[3]) == rank):
                wcaid = row[0]
                time = timeformat(row[1])
                solvetype = "Mean"
                country = getcountry(wcaid)
                break
        
    name = id_to_name_d[wcaid]

    return({"rank": rank, "time": time, "name": name, "wcaid": wcaid, 
            "solvetype": solvetype, "ranktype": " NR", "country": country})


def getwcaprofile(wcaid):
    """ Wca link based on user request from discord. I still need to change
        this so that you can just input a name but that requires complicated
        stuff...
    """
    wcaid = message.upper()
    url = f"https://www.worldcubeassociation.org/persons/{wcaid}"
    return(url)

def getimagelink(wcaid):
    """ Scrapes wca website with given ID for profile photo
    """
    # My dad wrote a bash script for me, i have no idea how this shit works so 
    # just trust the process...
    
    bashscript = (f'''wget -O - https://www.worldcubeassociation.org/persons/{wcaid} 2>/dev/null | grep img | grep avatar | sed "s/.*src=\\\"//" | sed "s/\\\".*$//"''')
    link = subprocess.getoutput(bashscript)
    return(link)

def getname(wcaid):
    return(id_to_name_d[wcaid])

def getcountry(wcaid):
    return(id_to_country_d[wcaid])
