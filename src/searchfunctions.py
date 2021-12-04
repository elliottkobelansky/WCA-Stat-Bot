import sqlite3
import subprocess
import re
from emoji import emojize


# Import WCA.db (sql database)
con = sqlite3.connect("WCA.db")
db = con.cursor()


def getavgtimes(dict):

    # actual spaghetti code pepelaugh
    db.execute(f'''SELECT value1, value2, value3, value4, value5 FROM RESULTS WHERE
                eventID="{dict['eventid']}" AND personId="{dict['wcaid']}" AND average={dict['best']}''')
    searchresults = db.fetchone()
    searchresults = [float(x) for x in searchresults]
    minvalue = min(searchresults)
    maxvalue = max(searchresults)
    minindex = searchresults.index(minvalue)
    maxvalue = searchresults.index(maxvalue)

    results = [ResultTime(i, dict['eventid'], dict['solvetype']).ftime
               for i in searchresults if int(i) != 0 and int(i) != -1]

    if len(results) == 5:
        results[maxvalue] = f'({results[maxvalue]})'
        results[minindex] = f'({results[minindex]})'

    if len(results) == 3:
        return(f"Times: {results[0]}, {results[1]}, {results[2]}")
    if len(results) == 5:
        return(f"Times: {results[0]}, {results[1]}, {results[2]}, {results[3]}, {results[4]}")

    return(searchresults)


def SQLgetResult(ResultRequest):
    """Selects: WCAID, PR, Rank, Country, Event Name and EventID
       For a given region (country, continent, or world)
       Solvetype (Single or Mean), event, and country.
    """

    query = f'''SELECT Persons.id, best, Events.name, eventid 
                
                    FROM ((Ranks{ResultRequest.solvetype} JOIN Persons ON
                          Ranks{ResultRequest.solvetype}.personId=Persons.id)
                    JOIN Events ON Ranks{ResultRequest.solvetype}.eventID=Events.id)
                    JOIN Countries ON countryid = Countries.id
                    
                    WHERE eventid LIKE ? 
                    AND {ResultRequest.region.regiontype}Rank=? '''
    args = [f'%{ResultRequest.event}%', ResultRequest.rank]

    if ResultRequest.region.regiontype in {'continent', 'country'}:
        query += f'AND {ResultRequest.region.regiontype}id LIKE ?'
        args.append(f'%{ResultRequest.region.region}%')

    db.execute(query, args)
    return(db.fetchone())


def getresult(message):
    """Returns a dict of results e.g. !wca nr 3 s canada bf will return
       A dict of different aspects of that result.  
    """
    R = ResultRequest(message)
    wcaid, best, event, eventid = \
        SQLgetResult(R)

    # MBLD means dont exist... (yet????)
    if eventid == "333mbf":
        solvetype = ""

    resultdict = {'wcaid': wcaid, 'best': best, 'rank': R.rank,
                  'event': event, 'ranktype': R.region.ranktype,
                  'solvetype': R.solvetype, 'eventid': eventid}

    return(resultdict)

def getwrs():
    """Returns a list of tuples
    """
    # Returns list in the form of [Name, eventid, best, (s or a)]
    db.execute("SELECT * FROM RanksSingle WHERE WorldRank = 1")
    wrs = [list(i)[:3] + ["Single"] for i in db.fetchall()]
    db.execute("SELECT * FROM RanksAverage WHERE WorldRank = 1")
    wraverages = [list(i)[:3] + ["Average"] for i in db.fetchall()]
    wrs.extend(wraverages)
    for row in wrs:
        db.execute("SELECT name FROM Persons WHERE id=?", [row[0]])
        row[0] = re.sub("\((.*?)\)", "", db.fetchone()[0])
        row[2] = ResultTime(row[2], row[1], row[3]).formatresult(row[2], row[1], row[3])
        row[1] = getevent(row[1])
        
    wrs = [x for x in wrs if x[1] != 0]
    return(wrs) 

def get_person_wca_id(namelist):

    query = ("SELECT id FROM Persons WHERE subid = 1") \
        + (" AND name LIKE ?") * len(namelist)

    for i in range(len(namelist)):
        namelist[i] = f"%{namelist[i]}%"

    db.execute(query, namelist)
    results = db.fetchall()
    results = [x[0] for x in results]
    return(results[0])

def getevent(id):
    eventdict = {
        "222": "2x2",
        "333": "3x3",
        "444": "4x4",
        "555": "5x5",
        "666": "6x6",
        "777": "7x7",
        "333oh": "OH",
        "333bf": "3BLD",
        "333fm": "FMC",
        "333mbf": "MBLD",
        "clock": "Clock",
        "minx": "Mega",
        "pyram": "Pyra",
        "skewb": "Skewb",
        "sq1": "SQ1",
        "444bf": "4BLD",
        "555bf": "5BLD"
    }
    try:
        return eventdict[id]
    except:
        return(0)

def sort_events(x):
    eventlist = [
        "Event",
        "3x3",
        "2x2",
        "4x4",
        "5x5",
        "6x6",
        "7x7",
        "3BLD",
        "FMC",
        "OH",
        "Clock",
        "Mega",
        "Pyra",
        "Skewb",
        "SQ1",
        "4BLD",
        "5BLD",
        "MBLD"
    ]
    return(eventlist.index(x))

def get_top_x(x, solvetype, region, event):
    query = f"SELECT * FROM Ranks{solvetype} WHERE eventid = ? ORDER BY cast(worldRank as INTEGER) LIMIT ?"
    args = [event, x]
    db.execute(query, args)
    return db.fetchall()

print(get_top_x(25, "Single", "3", "333bf"))

class WcaPerson:
    '''Class that represents a Person in the WCA db
    '''

    def __init__(self, wcaid):
        self.wcaid = wcaid
        self.name = self.get_person_name()   

    def get_name(self):
        db.execute("SELECT name FROM Persons WHERE id=?", [self.wcaid])
        name = db.fetchone()[0]
        return(name)

    def get_country(self):
        db.execute(
            "SELECT countryid FROM Persons WHERE id=? AND subid=1", [self.wcaid])
        country = db.fetchone()[0]
        return(country)

    def get_wca_link(self):
        wcalink = f"https://www.worldcubeassociation.org/persons/{self.wcaid}"
        return(wcalink)

    def get_continent(self):
        db.execute("SELECT continentId FROM Countries WHERE id=?",
                   [self.country])
        continent = db.fetchone()[0]
        return(continent)

    def get_emoji(self):
        db.execute(f"SELECT iso2 FROM Countries WHERE id='{self.country}'")
        code = db.fetchone()[0].lower()
        return(emojize(f":flag_{code}:"))

    def get_singleresults(self):
        db.execute(
            "SELECT * FROM RanksSingle WHERE personid  = ?", [self.wcaid])
        results = db.fetchall()
        return(results)

    def get_averageresults(self):
        db.execute(
            "SELECT * FROM RanksAverage WHERE personid = ?", [self.wcaid])
        results = db.fetchall()
        return(results)

    def getevent(self, id):
        eventdict = {
            "222": "2x2",
            "333": "3x3",
            "444": "4x4",
            "555": "5x5",
            "666": "6x6",
            "777": "7x7",
            "333oh": "OH",
            "333bf": "3BLD",
            "333fm": "FMC",
            "333mbf": "MBLD",
            "clock": "Clock",
            "minx": "Mega",
            "pyram": "Pyra",
            "skewb": "Skewb",
            "sq1": "SQ1",
            "444bf": "4BLD",
            "555bf": "5BLD"
        }
        try:
            return eventdict[id]
        except:
            return(0)
        db.execute(f"SELECT name FROM Events where id='{id}'")
        return(db.fetchone()[0])

    def get_image_link(self):
        """ Scrapes wca website with given ID for profile photo
        """
        # My dad wrote a bash script for me, i have no idea how this shit works so
        # just trust the process...

        bashscript = (
            f'wget -O - https://www.worldcubeassociation.org/persons/{self.wcaid} 2>/dev/null | grep img | grep avatar | sed "s/.*src=\\"//" | sed "s/\\".*$//"')
        link = subprocess.getoutput(bashscript)
        if link == "":
            link = "https://www.worldcubeassociation.org/assets/missing_avatar_thumb-12654dd6f1aa6d458e80d02d6eed8b1fbea050a04beeb88047cb805a4bfe8ee0.png"
        return(link)

    def parse_single_results(self):
        parsed_single_results = {}
        for result in self.get_person_singleresults():
            event = self.getevent(result[1])
            time = ResultTime(result[2], result[1], "Single").ftime
            wr = result[3]
            cr = result[4]
            nr = result[5]
            parsed_single_results.update({event: [time, wr, cr, nr]})
        parsed_single_results.pop(0, None)
        return(parsed_single_results)

    def parse_average_results(self):
        parsed_average_results = {}
        for result in self.get_person_averageresults():
            event = self.getevent(result[1])
            time = ResultTime(result[2], result[1], "Average").ftime
            wr = result[3]
            cr = result[4]
            nr = result[5]
            parsed_average_results.update({event: [time, wr, cr, nr]})
        parsed_average_results.pop(0, None)
        return(parsed_average_results)

    def get_medals(self):
        medals = [0, 0, 0]
        for i in [1, 2, 3]:
            db.execute(
                "SELECT pos FROM Results WHERE roundTypeId='f' AND personId=? AND pos=?", [self.wcaid, i]
                )
            count = len(db.fetchall())
            medals[i - 1] = count
        
        return(medals)
        
    def get_competition_count(self):
        db.execute("SELECT DISTINCT competitionId FROM Results WHERE personId=?", [self.wcaid])
        bruh = len(db.fetchall())
        return bruh

class ResultTime:
    def __init__(self, time, event, solvetype):
        self.rawtime = time
        self.event = event
        self.solvetype = solvetype
        self.ftime = self.formatresult(
            self.rawtime, self.event, self.solvetype)

    # I realized i could have done some of this stuff in a way better way
    def mbldformat(self, n):
        # Taken from README of WCA export
        difference = 99 - int(f"{n[0]}{n[1]}")
        time = int(f"{n[2]}{n[3]}{n[4]}{n[5]}{n[6]}")
        seconds = time % 60
        minutes = int((time - seconds)/60)
        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"
        time = f"{minutes}:{seconds}"

        missed = int(f"{n[7]}{n[8]}")
        solved = difference + missed
        attempted = solved + missed

        return(f"{solved}/{attempted} {time}")

    def timeformat(self, time):
        """ Takes xxxx format and adjusts it
            to xx:xx.xx if necessary
        """
        solvetime = float('{0:.2f}'.format(int(time) / 100.0))
        if float(solvetime) < 60.00:
            return('{0:.2f}'.format(solvetime))

        # Format m:s.ms if more than a minute
        if float(solvetime) >= 60.00:
            solvetime_ms = int(round(solvetime - int(solvetime), 2) * 100)
            if solvetime_ms < 10:
                solvetime_ms = f"0{str(solvetime_ms)}"
            solvetime_s = int(solvetime) % 60
            if solvetime_s < 10:
                solvetime_s = f"0{solvetime_s}"
            solvetime_m = int(int(solvetime) / 60)
            return(f"{solvetime_m}:{solvetime_s}.{solvetime_ms}")

    def formatresult(self, time, eventid, solvetype):
        if eventid == "333fm":
            if solvetype == "Single":
                return(time)
            if solvetype == "Average":
                solvetime = float('{0:.2f}'.format(int(time) / 100.0))
                return('{0:.2f}'.format(solvetime))
        elif eventid == "333mbf":
            return(self.mbldformat(time))
        else:
            return(self.timeformat(time))


class Region:
    ''' Represents a given country, continent, or entire world
    '''

    def __init__(self, ranktype, country="world"):
        self.ranktype = ranktype
        self.regiontype = self.get_region_type(ranktype)
        self.region = self.get_region(self.ranktype, country)

    def get_region_type(self, ranktype):
        if ranktype == "WR":
            return("world")
        elif ranktype == "NR":
            return("country")
        elif ranktype in {"AFR", "NAR", "EUR", "ASR", "ER", "SAR", "OCR"}:
            return("continent")
        else:
            return(1)

    def get_region(self, ranktype, country=""):
        continentdict = {"AFR": "Africa", "NAR": "North America", "ASR": "Asia",
                         "ER": "Europe", "EUR": "Europe", "SAR": "South America",
                         "OCR": "Oceania"}
        if ranktype in continentdict:
            return(continentdict[string])
        elif ranktype == "NR":
            return(country)
        elif ranktype == "WR":
            return("world")


class ResultRequest:
    def __init__(self, message):
        self.ranktype = message[1].upper()
        self.rank = message[2]
        self.solvetype = self.single_or_avg(message[3])
        if len(message) > 5:
            self.country = self.get_country_id(message[4:-1])
        else:
            self.country = ''
        self.event = message[-1]
        self.region = Region(self.ranktype, self.country)

    def get_country_id(self, request):
        request = " ".join(request).lower().replace("'", "_")
        db.execute(f'''SELECT id FROM Countries WHERE id LIKE ?''',
                   [f'%{request}%'])
        return(db.fetchone()[0])

    def single_or_avg(self, msg):
        """ Determines whether a string is referring to single or avg"""
        if msg in {"single", "sg", "s"}:
            return("Single")
        elif msg in {"average", "mean", "mn", "a", "m", "avg"}:
            return("Average")
        else:
            return(1)
