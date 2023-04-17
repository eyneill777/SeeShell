from sqlalchemy import *
import json


class Tables():
    def __init__(self):
        with open("../Database/config.json", "r") as f:
            self.config = json.load(f)
        engine = create_engine('mysql+pymysql://'+self.config['username']+':'+self.config['password']+'@'+self.config['host'])
        metadata_obj = MetaData()
        self.User = Table(
            "User",
            metadata_obj,
            Column("Username", VARCHAR(50), primary_key=True),
            Column("Email_Address", VARCHAR(100), nullable=False),
            Column("Password", VARCHAR(100), nullable=False)
        )
        self.Shell = Table(
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
        self.Location = Table(
            "Location",
            metadata_obj,
            Column("Location", VARCHAR(100), primary_key=True),
            Column("Scientific_Name", VARCHAR(100), primary_key=True)
        )
        self.Family = Table(
            "Family",
            metadata_obj,
            Column("Family", VARCHAR(100), primary_key=True),
            Column("Wiki_Link", VARCHAR(100))
        )
        self.Message = Table(
            "Message",
            metadata_obj,
            Column("Id", INTEGER, primary_key=True),
            Column("Username", VARCHAR(50)),
            Column("Data", VARCHAR(1000))
        )
        metadata_obj.create_all(engine)


