import subprocess
from emoji import emojize
import sqlite3

# Import WCA.db (sql database)
con = sqlite3.connect("../WCA.db")
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


def getimagelink(wcaid):
    """ Scrapes wca website with given ID for profile photo
    """
    # My dad wrote a bash script for me, i have no idea how this shit works so 
    # just trust the process...
    
    bashscript = (f'''wget -O - https://www.worldcubeassociation.org/persons/{wcaid} 2>/dev/null | grep img | grep avatar | sed "s/.*src=\\\"//" | sed "s/\\\".*$//"''')
    link = subprocess.getoutput(bashscript)
    if link == "": link="https://www.worldcubeassociation.org/assets/missing_avatar_thumb-12654dd6f1aa6d458e80d02d6eed8b1fbea050a04beeb88047cb805a4bfe8ee0.png"
    return(link)


def parsemessage(message):

    ranktype = message[1]
    rank = int(message[2])
    # "Single" or "Average"
    solvetype = single_or_avg(message[3])
    event = message[-1]
    # "world", "continent", or "country"
    regiontype = getregiontype(ranktype)

    if regiontype == "continent": region = getcontinent(ranktype)
    elif regiontype == "country": 
        region = getcountry(message[4:-1])
    elif regiontype == "world":
        region = "world"

    return(ranktype, rank, solvetype, regiontype, region, event)


def single_or_avg(string):
    """ Determines whether a string is referring to single or avg"""
    if string in ["single", "sg", "s"]: return("Single")
    elif string in ["average", "mean", "mn", "a", "m", "avg"]: return("Average")
    else: return(1)


def getregiontype(string):
    """Returns region type for a given string"""
    if string.lower() == "wr": return("world")
    elif string.lower() == "nr": return("country")
    elif string.lower() in ["afr", "nar", "eur", "asr", "er", "sar", "ocr"]:
        return("continent")
    else: return(1)


def getcontinent(string):
    """Returns full continent name for a given 'code' """
    string = string.lower()
    continentdict = {"afr": "Africa", "nar": "North America", "asr": "Asia",
                     "er": "Europe", "eur": "Europe", "sar": "South America",
                     "ocr": "Oceania"}

    return(continentdict[string])


def formatresult(time, eventid):
    if eventid == "333fm": return(time)
    elif eventid == "333mbf": return(uf.mbldformat(time))
    else: return(timeformat(time))


def getcountry(string):
    """Returns a country id for a given string. This is sorta like a search function"""
    string = " ".join(string).lower().replace("'", "_")
    db.execute(f'''SELECT id FROM Countries WHERE id LIKE ?''', [f'%{string}%'])
    return(db.fetchone()[0])