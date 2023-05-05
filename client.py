import requests
import json

url = "http://localhost:8000/login"
data = {"username":"csaglili", "password":"1234"}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
