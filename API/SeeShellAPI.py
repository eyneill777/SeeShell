from flask import Flask, make_response, request
import json
import uuid
import os
from sqlalchemy import *
import pandas as pd
import bcrypt

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)

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

engine = create_engine('mysql://' + config['username'] + ':' + config['password'] + '@' + config['host'])


@app.route("/")
def hello_world():
    return "<p>Welcome to the SeeShell API</p>"





#Upload an image
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    response = make_response("<h1>Bad Request</h1>")
    response.status_code = 400
    
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = uploaded_file.filename
        if filename != '':
            tmp = filename.split('.')
            fileExt = tmp[len(tmp)-1]
            if fileExt not in config['uploadExtensions']:
                response = make_response("<h1>Unsupported Media Type</h1>")
                response.status_code = 415
                return response
            uploaded_file.save(config["dropFolder"]+str(uuid.uuid4())+"."+fileExt)
            response = make_response("<h1>Success</h1>")
            response.status_code = 200
            
    return response


@app.route('/checkPass/', methods=['POST'])
def checkPass():
    response = make_response("<h1>Bad Request</h1>")
    response.status_code = 400

    if request.method == 'POST':
        username = request.headers["username"]
        password = request.headers["password"]
        stmt = select(User.c.Password).where(User.c.Username == username)
        with engine.connect() as conn:
            for rows in conn.execute(stmt):
                row = rows
            conn.close()
        if bcrypt.checkpw(password.encode('utf-8'), str(row[0]).encode('utf-8')):
            response = make_response('good')
            response.status_code = 200
        else:
            response = make_response('bad')
            response.status_code = 200
    return response

@app.route('/createAccount/', methods=['POST'])
def createAccount():
    response = make_response("<h1>Bad Request</h1>")
    response.status_code = 400

    if request.method == 'POST':
        username, email, password = request.headers["username"], request.headers["email"], request.headers["password"]
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        with engine.connect() as conn:
            conn.execute(insert(User).values(Username=username, Email_Address=email, Password=password))
            conn.commit()
            conn.close()
        response = make_response('Success')
        response.status_code = 200
    return response