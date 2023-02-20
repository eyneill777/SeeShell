from sqlalchemy import *
import json

with open("config.json", "r") as f:
    config = json.load(f)

engine = create_engine('mysql://'+config['username']+':'+config['password']+'@'+config['host'])

metadata_obj = MetaData()
User = Table(
    "User",
    metadata_obj,
    Column("Username", VARCHAR(60), primary_key=True),
    Column("Email_Address", VARCHAR(60), nullable=False),
    Column("Password", VARCHAR(60), nullable=False),
    Column("Image_Library", VARCHAR(60))
)

Shell = Table(
    "Shell",
    metadata_obj,
    Column("Scientific_Name", VARCHAR(100), primary_key=True),
    Column("Common_Name", VARCHAR(60)),
    Column("AphiaID", INTEGER),
    Column("Accepted_SciName", VARCHAR(100)),
    Column("Habitat", VARCHAR(60)),
    Column("Blurb", TEXT)
)

UserHasSeen = Table(
    "UserHasSeen",
    metadata_obj,
    Column("Username", VARCHAR(60), ForeignKey("User.Username"), primary_key=True),
    Column("Scientific_Name", VARCHAR(100), ForeignKey("Shell.Scientific_Name"), primary_key=True)
)


metadata_obj.create_all(engine)
