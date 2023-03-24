import mysql.connector
from mysql.connector import Error
import json

def dbconnection():

    with open("config.json", "r") as f:
        config = json.load(f)

    try:
        conn = mysql.connector.connect(host=config['host'], database=config['database'], user=config['username'],password=config['password'])

    except Error as e:
        print('Connection Error')

    if conn.is_connected():
        print('Connected to database')

    return conn