import requests
import base64



#Upload an image using the API
data = open("/Users/eron/Downloads/im.jpeg", "rb")
data_read = data.read()
data_64_encode = base64.b64encode(data_read) 
data_64_string = data_64_encode.decode('utf-8')
payload = {'id': 'test', 'file': {'base64': data_64_string, 'extension': '.jpeg'}}
response = requests.post("http://localhost:5000/upload/", json = payload)
print(response)
print(response.text)