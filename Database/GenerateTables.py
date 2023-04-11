from sqlalchemy import *
from API import tables
import json
import csv
import sys
sys.path.append('..')

with open("config.json", "r") as f:
    config = json.load(f)

engine = create_engine('mysql+pymysql://'+config['username']+':'+config['password']+'@'+config['host'])
table = tables.Tables()

familyLinks = []
with open('familyInfo.csv', 'r') as f:
    freader = csv.reader(f)
    for row in freader:
        familyLinks.append(row)
    f.close()

shells = []
with open('finalShellInfo.csv', 'r') as f:
    freader = csv.reader(f)
    for row in freader:
        shells.append(row)
    f.close()

stmtlist = []
for i in range(1,len(familyLinks)):
    stmt = insert(table.Family).values(Family=familyLinks[i][0], Wiki_Link=familyLinks[i][1])
    stmtlist.append(stmt)

for i in range(1,len(shells)-1):
    if shells[i][1] == 'NA':
        stmt = insert(table.Shell).values(Scientific_Name = shells[i][0])
        stmtlist.append(stmt)
        continue
    stmt = insert(table.Shell).values(Scientific_Name = shells[i][0], Common_Name = shells[i][4], AphiaID = shells[i][1], Accepted_SciName = shells[i][2], Accepted_AphiaID = shells[i][3], Family = shells[i][0], Habitat = shells[i][6], Extinct = eval(shells[i][7]))
    stmtlist.append(stmt)
    if shells[i][8] != 'None' and shells[i][8] != '[]':
        locstring = shells[i][8]
        l = list(locstring)
        j = 0
        while j < len(l):
            if l[j] == '[':
                l.insert(j + 1, '\"')
                j += 1
            if l[j] == ',':
                l.insert(j, '\"')
                l.insert(j + 3, '\"')
                j += 3
            if l[j] == ']':
                l.insert(j, '\"')
                break
            j += 1
        locstring = ''.join(l)
        locations = json.loads(locstring)
        for location in locations:
            stmt = insert(table.Location).values(Location = location, Scientific_Name = shells[i][0])
            stmtlist.append(stmt)

with engine.connect() as conn:
    for stmt in stmtlist:
        conn.execute(stmt)
    conn.commit()
    conn.close()