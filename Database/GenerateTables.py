from sqlalchemy import *
import json

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
    Column("Family", ForeignKey("Family.Family"),VARCHAR(100)),
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
    Column("Scientific_Name", ForeignKey("Shell.Scientific_Name"), VARCHAR(100))
)


metadata_obj.create_all(engine)
