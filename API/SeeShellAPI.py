from flask import Flask, make_response, request
import json
import uuid
import os

with open("config.json", "r") as f:
    config = json.load(f)

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