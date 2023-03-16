import mysql.connector
from mysql.connector import Error

def dbconnection():
    try:
        conn = mysql.connector.connect(host='localhost', database='SeeShell',user='root',password='root')

    except Error as e:
        print('Connection Error')

    if conn.is_connected():
        print('Connected to database')

    return conn