import requests

response = requests.post(
    'http://127.0.0.1:6000/users/',
    json={'email': "test222@nmmu.ru", 'password': 'tghRY45#$'}
)

print(response.text)