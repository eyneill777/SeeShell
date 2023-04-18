import requests
import uuid

class SeeShellAPIClient():
    def __init__(self, url):
        self.url = url
       
    # Upload Image to Server
    def uploadImage(self, file, username):
        returnText = "Image Upload Failed - Generic Error"
        files = {"file": file}
        headers = {'id': str(uuid.uuid4()), "userName": username, "apiKey": "1234"}
        try:
            response = requests.post(self.url+"/upload/", files=files, headers=headers)
            returnText = response.text
        except requests.exceptions.ConnectionError as e:
            returnText = "Connection to server failed"
        return returnText

    
    # Authenticate
    def checkPass(self, username, password):
        returnText = "Password Check Failed - Generic Error"
        headers = {"username": username, "password": password}
        try:
            response = requests.post(self.url+"/checkPass/", headers=headers)
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
            response = requests.post(self.url+"/createAccount/", headers=headers)
            if response.text == 'Username taken':
                returnText = 'Username taken, please try another'
            elif response.text == 'Success':
                returnText = 'Success'
        except requests.exceptions.ConnectionError as e:
            returnText = "Connection to server failed"
        return returnText