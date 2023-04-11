from flask import Flask, make_response, request
from tables import Tables
import json
import uuid
from sqlalchemy import *
import bcrypt

with open("config.json", "r") as f:
    config = json.load(f)

engine = create_engine('mysql+pymysql://'+config['username']+':'+config['password']+'@'+config['host'])


app = Flask(__name__)

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


#Check user credentials
@app.route('/checkPass/', methods=['POST'])
def checkPass():
    response = make_response("<h1>Bad Request</h1>")
    response.status_code = 400

    if request.method == 'POST':
        username = request.headers["username"]
        password = request.headers["password"]
        stmt = select(Tables().User.c.Password).where(Tables().User.c.Username == username)
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

#Create a new user account
@app.route('/createAccount/', methods=['POST'])
def createAccount():
    response = make_response("<h1>Bad Request</h1>")
    response.status_code = 400

    if request.method == 'POST':
        username, email, password = request.headers["username"], request.headers["email"], request.headers["password"]
        stmt = select(Tables().User.c.Username).where(Tables().User.c.Username == username)
        with engine.connect() as conn:
            result = conn.execute(exists(stmt).select())
            if result.first()[0]:
                response = make_response('Username taken')
                response.status_code = 200
                return response
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        with engine.connect() as conn:
            conn.execute(insert(Tables().User).values(Username=username, Email_Address=email, Password=password))
            conn.commit()
            conn.close()
        response = make_response('Success')
        response.status_code = 200
    return response
