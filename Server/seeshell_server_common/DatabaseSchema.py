from sqlalchemy import *
import json


class Tables():
    def __init__(self):
        """
        Common library of ORM objects which defines each of the data models in the SeeShell database.  Intended for server side use only, and database transactions should only be done through these ORM models.
        """
        with open("../Database/config.json", "r") as f:
            self.config = json.load(f)
        self.metadata_obj = MetaData()
        self.User = Table(
            "User",
            self.metadata_obj,
            Column("Username", VARCHAR(50), primary_key=True),
            Column("Email_Address", VARCHAR(100), nullable=False),
            Column("Password", VARCHAR(100), nullable=False)
        )
        self.Shell = Table(
            "Shell",
            self.metadata_obj,
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
            self.metadata_obj,
            Column("Location", VARCHAR(100), primary_key=True),
            Column("Scientific_Name", VARCHAR(100), primary_key=True)
        )
        self.Family = Table(
            "Family",
            self.metadata_obj,
            Column("Family", VARCHAR(100), primary_key=True),
            Column("Wiki_Link", VARCHAR(100))
        )
        self.Message = Table(
            "Message",
            self.metadata_obj,
            Column("Id", VARCHAR(100), primary_key=True),
            Column("Username", VARCHAR(50)),
            Column("Data", VARCHAR(10000))
        )


