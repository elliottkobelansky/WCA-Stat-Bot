import sqlite3
from emoji import emojize
import utilityfunctions as uf

# Import WCA.db (sql database)
con = sqlite3.connect("../WCA.db")
db = con.cursor()


def getavgtimes(dict):

    # actual spaghetti code pepelaugh
    db.execute(f'''SELECT value1, value2, value3, value4, value5 FROM RESULTS WHERE
                eventID="{dict['eventid']}" AND personId="{dict['wcaid']}" AND average={dict['rawtime']}''')
    searchresults = db.fetchone()
    searchresults = [float(x) for x in searchresults]
    
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
        searchresults = [uf.timeformat(i) for i in searchresults if int(i) != 0 and int(i) != -1]
    else:
        searchresults = [i for i in searchresults if i != "0"]

    if len(searchresults) == 5:
        searchresults[maxvalue] = f'({searchresults[maxvalue]})'
        searchresults[minindex] = f'({searchresults[minindex]})'
                
    return(searchresults)


def getflagemoji(country):
    # This is actually pretty cool i am proud of this
    db.execute(f"SELECT iso2 FROM Countries WHERE id='{country}'")
    code = db.fetchone()[0].lower()
    return(emojize(f":flag_{code}:"))


def SQLgetResult(regiontype, rank, solvetype, region, event):

    """Selects: Name, WCAID, PR, Rank, Country, Event Name and EventID
       For a given region (country, continent, or world)
       Solvetype (Single or Mean), event, and country.
    """
    
    query = f'''SELECT Persons.name, Persons.id, best, {regiontype}Rank, 
                          countryid, Events.name, eventid 
                
                    FROM ((Ranks{solvetype} JOIN Persons ON
                          Ranks{solvetype}.personId=Persons.id)
                    JOIN Events ON Ranks{solvetype}.eventID=Events.id)
                    JOIN Countries ON countryid = Countries.id
                    
                    WHERE eventid LIKE ? 
                    AND {regiontype}Rank=? '''
    args = [f'%{event}%', rank]

    if regiontype in ['continent', 'country']: 
        query += f'AND {regiontype}id LIKE ?'   
        args.append(f'%{region}%')
    
    db.execute(query, args)
    return(db.fetchone())


def getresult(message):
    """Returns a dict of results e.g. !wca nr 3 s canada bf will return
       A dict of different aspects of that result.  
    """
    # Parses the message into different variables using parsemessage function
    ranktype, rank, solvetype, regiontype, region, event = uf.parsemessage(message)
    ranktype = ranktype.upper()

    # Gets more variables using SQLgetResult function
    name, wcaid, best, rank, country, event, eventid = \
    SQLgetResult(regiontype, rank, solvetype, region, event)

    # Formats time accord to event (e.g. 333mbf needs to be formatted different)
    f_time = uf.formatresult(best, eventid)

    # MBLD means dont exist... (yet????)
    if eventid == "333mbf": solvetype = "" 

    resultdict = {'name': name, 'wcaid': wcaid, 'time': f_time, 'rank': rank,
                  'event': event, 'ranktype': ranktype, 'solvetype': solvetype,
                  'country': country, 'eventid': eventid, 'rawtime': best}

    print(resultdict)

    return(resultdict)


def getworstresult(solvetype, eventid):
    pass


