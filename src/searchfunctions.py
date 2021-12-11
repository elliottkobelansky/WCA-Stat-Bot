import sqlite3
import subprocess
import re
from emoji import emojize


# Import WCA.db (sql database)
con = sqlite3.connect("WCA.db")
db = con.cursor()




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

def get_top_x(x, solvetype, region, event):
    query = f"SELECT * FROM Ranks{solvetype} WHERE eventid = ? ORDER BY cast(worldRank as INTEGER) LIMIT ?"
    args = [event, x]
    db.execute(query, args)
    return db.fetchall()


