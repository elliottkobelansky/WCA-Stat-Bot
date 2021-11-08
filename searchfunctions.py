import pandas as pd
import numpy as np
import subprocess
import sqlite3

# Import WCA.db (sql database)
con = sqlite3.connect("3bld_stats/WCA.db")
db = con.cursor()

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
            solvetime_ms = f"0{str(solvetime_ms)}"
        # Seconds (without ms)
        solvetime_s = int(solvetime) % 60
        # Add leading 0 if seconds bad
        if solvetime_s < 10:
            solvetime_s = f"0{solvetime_s}"
        # Minutes
        solvetime_m = int(int(solvetime) / 60)
        return(f"{solvetime_m}:{solvetime_s}.{solvetime_ms}")

def mbldformat(n):
    # Taken from README of wca export 
    difference = 99 - int(f"{n[0]}{n[1]}")
    time = int(f"{n[2]}{n[3]}{n[4]}{n[5]}{n[6]}") 
    seconds = time % 60
    minutes = int((time - seconds)/60)
    if minutes < 10: minutes = f"0{minutes}"
    if seconds < 10: seconds = f"0{seconds}"
    time = f"{minutes}:{seconds}"

    missed = int(f"{n[7]}{n[8]}")
    solved = difference + missed
    attempted = solved + missed

    return(f"{solved}/{attempted} in {time}")



def get_wr_result(message):
    """ Prints the result with a certain world ranking
    """
    rank = message[2]
    event = message[4]

    if ";" in event or "\'" in event: return 0

    # Depending on if single or mean is requested, get wcaid, time, solvetype
    elif message[3].lower() in ["single", "sg", "s"]:
        db.execute(f'''SELECT Persons.name, Persons.id, best, worldRank, 
                       countryid, Events.name, eventid FROM (RanksSingle JOIN Persons ON
                       RanksSingle.personId=Persons.id) JOIN Events ON 
                       RanksSingle.eventID=Events.id WHERE eventid LIKE "%{event}%" 
                       AND worldRank={rank}''')
        solvetype = ' Single'
        searchresults = db.fetchone()

    elif message[3].lower() in ["average", "mean", "mn", "a", "m", "avg"]:
        db.execute(f'''SELECT Persons.name, Persons.id, best, worldRank, 
                       countryid, Events.name, eventid FROM (RanksAverage JOIN Persons 
                       ON RanksAverage.personId=Persons.id) JOIN Events ON 
                       RanksAverage.eventID=Events.id WHERE eventid LIKE "%{event}%" 
                       AND worldRank={rank}''')
        solvetype = ' Average'
        searchresults = db.fetchone()

    name = searchresults[0]
    wcaid = searchresults[1]
    rank = searchresults[3]
    country = searchresults[4]
    event = searchresults[5]
    eventid = searchresults[6]
    rawtime = searchresults[2]
    if eventid == "333fm" and solvetype == ' Average': time = '{0:.2f}'.format(int(rawtime)/100.0)
    elif eventid not in ["333mbf", "333fm"]: time = timeformat(searchresults[2])
    elif eventid == "333mbf": time = mbldformat(searchresults[2])
    if event == "333mbf": solvetype = "" 


    # Thought a dict would be a good thing to use for this
    return({'name': name, "wcaid": wcaid, "time": time, "rank": rank,
            'event': event, 'ranktype': 'WR', "solvetype": solvetype,
            'region': '', 'rawtime': rawtime, 'eventid': eventid})

def get_nr_result(message):
    """ Prints the result with a certain national ranking
    """

    rank = int(message[2])
    event = message[-1]
    country = " ".join(message[4:-1]).lower()

    if ";" in event or "\'" in event: return 0
    if ";" in country or "\'" in country: return 0

    # This can probably be combined into one function so that it doesnt have 
    # to repeat in the search functions
    if message[3].lower() in ["single", "sg", "s"]:     
        db.execute(f'''SELECT Persons.name, Persons.id, best, countryRank, 
                    countryid, Events.name, eventId FROM (RanksSingle JOIN Persons ON
                    RanksSingle.personId=Persons.id) JOIN Events ON 
                    RanksSingle.eventID=Events.id WHERE eventid LIKE "%{event}%" 
                    AND countryRank={rank} AND countryid LIKE "%{country}%"''')
        solvetype = ' Single'
        searchresults = db.fetchone()

    elif message[3].lower() in ["average", "mean", "mn", "a", "m", "avg"]: 
        db.execute(f'''SELECT Persons.name, Persons.id, best, countryRank, 
                countryid, Events.name, eventId FROM (RanksAverage JOIN Persons 
                ON RanksAverage.personId=Persons.id) JOIN Events ON 
                RanksAverage.eventID=Events.id WHERE eventid LIKE "%{event}%" 
                AND countryRank={rank} AND countryid LIKE "%{country}%"''')
        solvetype = ' Average'
        searchresults = db.fetchone()

    name = searchresults[0]
    wcaid = searchresults[1]
    rank = searchresults[3]
    country = searchresults[4]
    event = searchresults[5]
    eventid = searchresults[6]
    rawtime = searchresults[2]
    if eventid == "333fm": time = rawtime
    elif eventid not in ["333mbf", "333fm"]: time = timeformat(searchresults[2])
    elif eventid == "333mbf": time = mbldformat(searchresults[2])
    if event == "333mbf": solvetype = ""

    return({'name': name, "wcaid": wcaid, "time": time, "rank": rank,
            'event': event, 'ranktype': ' NR', "solvetype": solvetype,
            'region': country, 'eventid': eventid, "rawtime": rawtime})


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

def getavgtimes(dict):
    # actual spaghetti code pepelaugh
    db.execute(f'''SELECT value1, value2, value3, value4, value5 FROM RESULTS WHERE
                eventID="{dict['eventid']}" AND personId="{dict['wcaid']}" AND average={dict['rawtime']}''')
    searchresults = list(db.fetchone())
    
    # Put brackets around non-counting times. This is the worst code ive done by far
    if len(searchresults) == 5:
        maxtemp = 0
        mintemp = 0
        maxcounter = 0
        mincounter = 0
        
    minvalue = min(searchresults)
    maxvalue = max(searchresults)
    minindex = searchresults.index(minvalue)
    maxvalue = searchresults.index(maxvalue)

    if dict['eventid'] != "333fm":
        searchresults = [timeformat(i) for i in searchresults if i != "0" and i != "0"]
    else:
        searchresults = [i for i in searchresults if i != "0"]


    
    if len(searchresults) == 5:
        searchresults[maxvalue] = f'({searchresults[maxvalue]})'
        searchresults[minindex] = f'({searchresults[minindex]})'
                
    print(searchresults)

    return(searchresults)