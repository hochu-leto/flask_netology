import requests

response = requests.get('http://127.0.0.1:6000/test/')
print(response.text)