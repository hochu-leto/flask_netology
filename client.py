import requests

# response = requests.post(
#     'http://127.0.0.1:6000/users/',
#     json={'email': "test12@nmmu.ru", 'password': 'tghRYdf45#$'}
# )
#
# response = requests.get(
#     'http://127.0.0.1:6000/users/'
# )

response = requests.post(
    'http://127.0.0.1:6000/ads/',
    json={"token": "71a96721-f157-485c-aa33-66590c469442", 'header': "Fourth commit", 'description': 'Lorem ipsum '
                                                                                                    'caecat '
                                                                                                    'cupidatat non '
                                                                                                    'proid'}
)

print(response.text)
