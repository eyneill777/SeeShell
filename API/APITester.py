import requests




#Upload an image using the API
file = open("/home/thomassmith/Downloads/shell.jpeg", "rb")

files = {"file": file}
headers = {'id': 'test', "userName": "test user", "apiKey": "1234"}
response = requests.post("http://localhost:5000/upload/", files=files, headers=headers)
print(response)
print(response.text)

# headers = {"username": 'username8', "password": 'pass'}
# passIsValid = requests.post("http://localhost:5000/checkPass/", headers=headers)
# print(passIsValid)
# print(passIsValid.text)