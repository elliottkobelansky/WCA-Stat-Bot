import sqlite3
import subprocess
import re
from emoji import emojize
import wcautils as wu

con = sqlite3.connect("WCA.db")
db = con.cursor()

class WcaPerson:
    ''' A person in the WCA database.
    '''
    
    def __init__(self, wcaid):
        self.wcaid = wcaid
        
    def name(self):
        db.execute("Select name from Persons where id=?", [self.wcaid])
        return db.fetchone()[0]
    
    def country(self):
        db.execute(
            "Select countryid from persons where id=? and subid=1", 
            [self.wcaid]
            )    
        return db.fetchone()[0]
    
    def emoji(self):
        db.execute(f"Select iso2 from Countries where id='{self.country()}'")
        code = db.fetchone()[0].lower()
        return emojize(f":flag_{code}:")
    
    def wca_link(self):
        return f"https://www.worldcubeassociation.org/persons/{self.wcaid}"
    
    def image_link(self):
        bashscript = (
            f'wget -O - https://www.worldcubeassociation.org/persons/{self.wcaid} 2>/dev/null | grep img | grep avatar | sed "s/.*src=\\"//" | sed "s/\\".*$//"')
        link = subprocess.getoutput(bashscript)
        if link == "":
            link = "https://www.worldcubeassociation.org/assets/missing_avatar_thumb-12654dd6f1aa6d458e80d02d6eed8b1fbea050a04beeb88047cb805a4bfe8ee0.png"
        return link
    
    def results(self):
        ''' Returns a dictionary in the form of 
            {
            "Single": {event: [time, wr, cr, nr], 
            "Average": {event [time, wr, cr, nr]
            }
        '''
        fresults = {"Single": {}, "Average": {}}
        results = []
        
        for solvetype in {"Single", "Average"}:
            db.execute(
                f"SELECT * FROM Ranks{solvetype} WHERE personid=?", 
                [self.wcaid]
            )
            results.append(db.fetchall())
            
        # Results: [[(wcaid, eventid, best, wr, cr, nr), ...], [...]]
        for resulttype, solvetype in zip(results, {"Single", "Average"}):
            for result in resulttype:
                event, time, wr, cr, nr = result[1:6]
                fresults[solvetype].update({event: [time, wr, cr, nr]})
            fresults[solvetype].pop(None, None)
        return fresults
    
    def get_pr(self, eventid, solvetype):
        ''' Gets a persons PR Average 
        '''
        
        db.execute(
                   f'''Select best from Ranks{solvetype} where eventId=?
                       and PersonId=?''', [eventid, self.wcaid]
                   )
        praverage = db.fetchone()
        if praverage:
            return praverage[0]
        else:
            return None
    
    def get_avgtimes(self, eventid):
        ''' Gets all 5 or 3 solves of a person's PR average, as a tuple
        '''
        
        pr = self.get_pr(eventid, "Average")
        db.execute(
            f'''Select value1, value2, value3, value4, value5 from Results
                where eventId=? and personId=? and average=?''',
                [eventid, self.wcaid, pr]
        )
        searchresults = db.fetchone()
        if searchresults:
            return wu.formataverage(searchresults, eventid)
        else:
            return None
        
        
        
        
        
        
        
            
                        
class Region:
    ''' Represents a country, continent, or the world
        Input: list of words e.g. ["Sri", "Lanka"]
    '''            

    def __init__(self, region="world"):
        self.region = region

        if self.region == "world":
            self.regiontype = "world"
        elif wu.get_country(self.region):
            self.regiontype = "country"
        else:
            self.regiontype = "continent"
        
        
    def top_25(self, solvetype, eventid):
        ''' Returns list of tuples in (rank, name, best) format
        ''' 
        request = (
            f"Select persons.id, best from Ranks{solvetype} order by best limit 25")
        pass
    
    def country_id(self):
        self.region


class ResultRequest:
    ''' Request for a WCA result based on certain factor.
        IMPORTANT: Region input must be a list bc i am dumbass.
    '''
    
    def __init__(self, solvetype, eventid, region, rank=1):
        self.solvetype = solvetype
        self.eventid = wu.get_eventid(eventid)
        self.region = Region(region).region
        self.regiontype = Region(region).regiontype
        self.rank = rank
        
        
    def get_result(self):
        ''' Selects WcaId and Best Time based on Result object 
        '''
         
        query = f'''Select Persons.id, best, {self.regiontype}Rank
        
                from ((Ranks{self.solvetype} join Persons on
                      Ranks{self.solvetype}.personId=Persons.id)
                join countries on persons.countryId = Countries.id)
                      
                where eventid = ? and 
                cast({self.regiontype}Rank as integer) <= ?
                '''
        args = [self.eventid, self.rank]
        
        if self.regiontype in {'continent', 'country'}:
            query += f'and {self.regiontype}Id like ?'
            args.append(f'%{self.region}%')
            
        query += (f"order by cast({self.regiontype}Rank as integer) desc ")

        query += ("limit 10")
        
        db.execute(query, args)
        
        result = db.fetchone()
        
        if result:
            return result
        else:
            return None

        
    



        
    
    
    