from sqlalchemy import *
import json
import csv

with open("config.json", "r") as f:
    config = json.load(f)

engine = create_engine('mysql://'+config['username']+':'+config['password']+'@'+config['host'])

metadata_obj = MetaData()
User = Table(
    "User",
    metadata_obj,
    Column("Username", VARCHAR(50), primary_key=True),
    Column("Email_Address", VARCHAR(100), nullable=False),
    Column("Password", VARCHAR(100), nullable=False)
)

Shell = Table(
    "Shell",
    metadata_obj,
    Column("Scientific_Name", VARCHAR(100), primary_key=True),
    Column("Common_Name", VARCHAR(100)),
    Column("AphiaID", INTEGER),
    Column("Accepted_SciName", VARCHAR(100)),
    Column("Accepted_AphiaID", INTEGER),
    Column("Family", VARCHAR(100)),
    Column("Habitat", VARCHAR(20)),
    Column("Extinct", BOOLEAN)
)

Family = Table(
    "Family",
    metadata_obj,
    Column("Family", VARCHAR(100), primary_key=True),
    Column("Wiki_Link", VARCHAR(100))
)

Location = Table(
    "Location",
    metadata_obj,
    Column("Location", VARCHAR(100), primary_key=True),
    Column("Scientific_Name", VARCHAR(100), primary_key=True)
)


metadata_obj.create_all(engine)





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
    stmt = insert(Family).values(Family=familyLinks[i][0], Wiki_Link=familyLinks[i][1])
    stmtlist.append(stmt)

for i in range(1,len(shells)-1):
    if shells[i][1] == 'NA':
        stmt = insert(Shell).values(Scientific_Name = shells[i][0])
        stmtlist.append(stmt)
        continue
    stmt = insert(Shell).values(Scientific_Name = shells[i][0], Common_Name = shells[i][4], AphiaID = shells[i][1], Accepted_SciName = shells[i][2], Accepted_AphiaID = shells[i][3],Family = shells[i][0], Habitat = shells[i][6], Extinct = eval(shells[i][7]))
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
            stmt = insert(Location).values(Location = location, Scientific_Name = shells[i][0])
            stmtlist.append(stmt)

with engine.connect() as conn:
    for stmt in stmtlist:
        conn.execute(stmt)
    conn.commit()
    conn.close()