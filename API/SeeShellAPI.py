from flask import Flask
from flask import request
import json
import base64

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        data = request.json
        b = base64.b64decode(data["file"]["base64"]) 
        with open(config["dropFolder"]+data["id"]+data["file"]["extension"], "wb") as file:
            file.write(b)
        return "Done"