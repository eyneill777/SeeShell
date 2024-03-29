import base64
from sqlalchemy import *

def Blurb(Scientific_Name, engine, table):
    """
    Returns a text \"Blurb\" containing factual information about a species based on Molluscabase data stored in the SeeShell database
    """
    stmt = select(table.Shell).where(table.Shell.c.Scientific_Name == Scientific_Name)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        for species in result:
            #only if shell never matched with molluscabase
            if species[2] is None:
                return 'This shell is a/an '+species[0]


            blurb = 'This shell is a/an '+ species[3]

            if species[1] != 'None' and species[6] != 'None':
                blurb += ', commonly known as '+species[1]+', and lives in a '+species[6]+' environment.'
            elif species[1] != 'None':
                blurb += ' and is commonly known as '+species[1]+'.'
            elif species[6] != '[]' or species[6] != 'None':
                blurb += ' and can be found in a '+species[6].lower()+' environment. '


            if species[5] != 'None':
                blurb += 'It is a member of the family '+species[5]+'.'
            if species[7]:
                blurb += 'This species is thought to be extinct.'
            return blurb

def getLink(Scientific_Name, engine, table):
    """
    Returns information about family linkages between species
    """
    stmt = select(table.Shell).where(table.Shell.c.Scientific_Name == Scientific_Name)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        for species in result:
            stmt = select(table.Family).where(table.Family.c.Family == species[5])
            familyResult = conn.execute(stmt)
        for family in familyResult:
            return family[1]

def getMap(Scientific_Name, path_to_shellMaps):
    """
    Returns a pre-generated map of the species geographical distribution
    """
    try:
        target_file = path_to_shellMaps+'/'+Scientific_Name + '.png'
        with open(target_file, 'rb') as f:
            return base64.b64encode(f)
    except FileNotFoundError:
        return None
