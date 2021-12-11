import sqlite3, re, zipfile, os
from urllib.request import urlopen, urlretrieve

EXPORT_FILES = {
    "WCA_export_Competitions.tsv",
    "WCA_export_RanksAverage.tsv",
    "WCA_export_RanksSingle.tsv",
    "WCA_export_Results.tsv",
    "WCA_export_Events.tsv",
    "WCA_export_Persons.tsv",
    "WCA_export_Countries.tsv"
}

INDEXES = [
    "create index resultspersonididx on results (personid)",
    "create index resultseventididx on results (eventid)",
    "create index resultsbestidx on results (best)",
    "create index resultsaverageidx on results (average)",
    
    "create index rankssinglepersonididx on rankssingle (personid)",
    "create index rankssingleeventididx on rankssingle (eventid)",
    "create index rankssinglebestidx on rankssingle (best)",
    "create unique index bruhx on rankssingle (personid, eventid)",
    
    "create index ranksaveragepersonididx on ranksaverage (personid)",
    "create index ranksaverageeventididx on ranksaverage (eventid)",
    "create index ranksaveragebestidx on ranksaverage (best)",
    "create unique index bruh2x on ranksaverage (personid, eventid)",
    
    "create unique index personspersonididx on persons (id, subid)",
    "create unique index competitionsididx on competitions (id)" 
]
    

# From pochmann github with some modifications

filenames = []
tablenames = []

print("Reading HTML...")
html = str(urlopen('https://www.worldcubeassociation.org/results/misc/export.html').read())
filename = re.search(r"WCA_export\w+.tsv.zip", html).group(0)

os.system("mkdir export")

print("Downloading Latest TSV Export...")
urlretrieve('https://www.worldcubeassociation.org/results/misc/' + filename, "export/" + filename)

with zipfile.ZipFile("export/" + filename) as zf:
    for name in EXPORT_FILES:
        print(f"Extracting {name}...")
        filenames.append(name)
        zf.extract(name, "export/")
        
for name in filenames:
    name = re.search(r"[A-Z][a-z]+[A-Za-z]+[^\.]", name).group(0)
    tablenames.append(name)
    

os.system("rm WCA.db && touch WCA.db")

for filename, tablename in zip(filenames, tablenames):
    print(f"Creating table \"{tablename}\"")
    os.system(f"bash src/import/import_table.sh export/{filename} {tablename}")
    
con = sqlite3.connect('WCA.db')
db = con.cursor()

print("Creating indexes...")
for index in INDEXES:
    db.execute(index)
    
os.system("rm -r export")
print("Successfully imported latest WCA database.")