from apscheduler.schedulers.background import BackgroundScheduler
import random
import requests
import uuid
import json

class SeeShellAPIClient():
    def __init__(self, url):
        self.url = url
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    # Upload Image to Server
    def uploadImage(self, id, file, username):
        returnText = "Image Upload Failed - Generic Error"
        files = {"file": file}
        headers = {'id': id, "userName": username, "apiKey": "1234"}
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

    def checkMessages(self,username):
        headers = {"username": username}
        try:
            response = requests.get(self.url + "/checkMessages/", headers=headers)
            if response.text == 'There is a message':
                return True
            elif response.text == 'There is no message':
                return False
        except requests.exceptions.ConnectionError as e:
            return False

    def getMessages(self, username):
        headers = {"username": username}
        try:
            response = requests.get(self.url + "/getMessages/", headers=headers)
            print(response.text)
        except requests.exceptions.ConnectionError as e:
            print('nope')