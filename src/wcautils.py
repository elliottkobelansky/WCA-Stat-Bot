# Utility functions related to the WCA.


import sqlite3
import re

con = sqlite3.connect("WCA.db")
db = con.cursor()

EVENTSDICT = {
    "222": "2x2",
    "333": "3x3",
    "444": "4x4",
    "555": "5x5",
    "666": "6x6",
    "777": "7x7",
    "333bf": "3BLD",
    "333fm": "FMC",
    "333oh": "OH",
    "clock": "Clock",
    "minx": "Mega",
    "pyram": "Pyra",
    "skewb": "Skewb",
    "sq1": "SQ1",
    "444bf": "4BLD",
    "555bf": "5BLD",
    "333mbf": "MBLD",
    }
  

def is_wca_id_form(potential_id):
    ''' Determines if WCA id in the proper form ddddDDdd. Returns boolean.
    '''
    if not re.search(r"^\d{4}\D{4}\d{2}$", potential_id):
        return False
    else:
        return True


def get_wcaid(wcaid):
    ''' Gets a wcaid if it is in the WCA db. If not, returns None.
    '''
    
    potential_id = potential_id.upper()
    db.query("Select id from Persons where id=?", [wcaid])
    # This will either be None or a valid ID
    wcaid = db.fetchone()[0]
    return(wcaid)

def get_eventid(string):
    ''' Finds the eventid that best matches the string (sorta???)
    ''' 
    
    db.execute("Select id from Events where id like ?", 
               [f"%{string}%"])
    return db.fetchone()[0]
    
    
def get_event_name(eventid):
    ''' Gets an event's name given its eventid. If it's not a valid
        id, returns None.
    '''
    try:
        return EVENTSDICT[eventid]
    except:
        return None
   
   
def sort_events(event):
    ''' Returns value corresponding to order in which events are ordered
    ''' 
    # I had to account for this weird thing so just trust me on this one
    if event == "Event":
        return 0
    for i, eventid in enumerate(EVENTSDICT):
        if EVENTSDICT[eventid] == event:
            return i + 1
        
def get_country(string):
    ''' Returns countryid if it is a country, None if it isn't.
    '''
    
    db.execute("Select id from Countries where id like ? order by id desc", [f'%{string}%'])
    try:
        return db.fetchone()[0]
    except:
        return None

def get_CR_region(ranktype):
    ''' Given a continental ranktype (NR, WR, OCR, ER, etc.),
        returns the region.
    '''
    
    continentdict = {
        "AFR": "Africa", "NAR": "North America", "ASR": "Asia",
        "ER": "Europe", "SAR": "South America", "OCR": "Oceania", 
        "EUR": "Europe"
    }
    
    try:
        return continentdict[ranktype]
    except:
        return None
    
def is_valid_ranktype(ranktype):
    ''' Checks if the input is a valid ranktype (nr, wr, nar, ...)
        Case insensitive. 
    '''
    if ranktype.lower() in { \
        "wr", "nr", "ocr", "nar", "er", "eur", "afr", "asr", "sar" \
        }:
        return True
    else:
        return False
    
def single_or_avg(solvetype):
    # This is sorta weird. Checks if starts with an s
    if re.search("^[sS]", solvetype):
        return "Single"
    
    if re.search("^[aA]", solvetype):
        return "Average"
    
    else:
        return None
    
def get_wcaid_from_name(name):
    ''' Gets a person's ID based on their name (input in list form)
    '''
    
    query = "Select id from persons where subid=1" \
            + " and name like ?" * len(name)
    
    for i in range(len(name)):
        name[i] = f"%{name[i]}%"
        
    db.execute(query, name)
    
    results = db.fetchall()
    # This would return everyone with similar names. For now i only return one
    if results: 
        results = [x[0] for x in results]
        return(results[0])
    
    else: 
        return None