import requests




#Upload an image using the API
file = open("/Users/eron/Downloads/im.jpeg", "rb")

files = {"file": file}
headers = {'id': 'test', "userName": "test user", "apiKey": "1234"}

response = requests.post("http://localhost:5000/upload/", files=files, headers=headers)
print(response)
print(response.text)