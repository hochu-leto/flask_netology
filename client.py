import requests

response = requests.post(
    'http://127.0.0.1:6000/users/',
    json={'email': "test", 'password': 'test1'}
)

print(response.text)