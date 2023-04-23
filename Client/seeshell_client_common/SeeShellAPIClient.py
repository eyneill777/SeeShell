from apscheduler.schedulers.background import BackgroundScheduler
import random
import requests
import uuid
import json

class SeeShellAPIClient():
    def __init__(self, url):
        self.url = url
        self.username = None
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    # Upload Image to Server
    def uploadImage(self, id, file):
        returnText = "Image Upload Failed - Generic Error"
        files = {"file": file}
        headers = {'id': id, "userName": self.username, "apiKey": "1234"}
        try:
            response = requests.post(self.url + "/upload/", files=files, headers=headers)
            returnText = response.text
        except requests.exceptions.ConnectionError as e:
            returnText = "Connection to server failed"
        return returnText

    # Authenticate
    def checkPass(self, username, password):
        returnText = "Password Check Failed - Generic Error"
        headers = {"username": username, "password": password}
        try:
            response = requests.post(self.url + "/checkPass/", headers=headers)
            if response.text == 'good':
                returnText = "Success"
            else:
                returnText = "Invalid username or password"
        except requests.exceptions.ConnectionError as e:
            returnText = "Connection to server failed"
        return returnText

    # Create New Account
    def createAccount(self, username, email, password):
        returnText = "Account Creation Failed - Generic Error"
        try:
            headers = {"username": username, "email": email, "password": password}
            response = requests.post(self.url + "/createAccount/", headers=headers)
            if response.text == 'Username taken':
                returnText = 'Username taken, please try another'
            elif response.text == 'Success':
                returnText = 'Success'
        except requests.exceptions.ConnectionError as e:
            returnText = "Connection to server failed"
        return returnText

    def getMessages(self):
        headers = {"Username": self.username}
        try:
            response = requests.get(self.url + "/getMessages/", headers=headers)
            return json.loads(response.text)
        except requests.exceptions.ConnectionError as e:
            print("Connection to server failed")

    def makeBlurb(self, species):
        if species["AphiaID"] is None:
            return 'This shell is a/an ' + species[0]

        blurb = 'This shell is a/an ' + species["Accepted_SciName"]

        if species["Common_Name"] != 'None' and species["Habitat"] != 'None':
            blurb += ', commonly known as ' + species["Common_Name"] + ', and lives in a ' + species["Habitat"] + ' environment.'
        elif species["Common_Name"] != 'None':
            blurb += ' and is commonly known as ' + species["Common_Name"] + '.'
        elif species["Habitat"] != '[]' or species["Habitat"] != 'None':
            blurb += ' and can be found in a ' + species["Habitat"].lower() + ' environment. '

        if species["Family"] != 'None':
            blurb += 'It is a member of the family ' + species["Family"] + '.'
        if species["Extinct"]:
            blurb += 'This species is thought to be extinct.'
        return blurb