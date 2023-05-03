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
    def uploadImage(self, file, id):
        '''
        Attempts to upload the provided file to the server, with the specified id for later message retrieval
        '''
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
        '''
        Sends a user's username and password to the server for account validation
        '''
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
        '''
        Sends a new user's username, email and password to the server for account validation and creation
        '''
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
        '''
        Sends a request to the server to check for new messages and return them if any exist
        '''
        headers = {"Username": self.username}
        try:
            response = requests.get(self.url + "/getMessages/", headers=headers)
            return json.loads(response.text)
        except requests.exceptions.ConnectionError as e:
            print("Connection to server failed")

    def clean_data(self, shell_dict):
        '''
        Cleans stored shell data for cleaner presentation in blurb screen
        '''
        new_shell_dict = {}
        if shell_dict["AphiaID"] == 'None':
            new_shell_dict['Scientific Name'] = shell_dict["Scientific_Name"]
            return new_shell_dict
        new_shell_dict['Scientific Name'] = shell_dict["Accepted_SciName"]
        if shell_dict["Common_Name"] != 'None':
            new_shell_dict["Common Name"] = shell_dict["Common_Name"]
        if shell_dict["Habitat"] != '[]' or shell_dict["Habitat"] != 'None':
            new_shell_dict["Habitat"] = shell_dict["Habitat"]
        if shell_dict["Family"] != 'None':
            new_shell_dict["Family"] = shell_dict["Family"]
        new_shell_dict["Extinct"] = shell_dict["Extinct"]
        if "Family_Link" in shell_dict and shell_dict["Family_Link"] != "None":
            new_shell_dict["Family_Link"] = shell_dict["Family_Link"]
        return new_shell_dict