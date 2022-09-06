import requests

# response = requests.post(
#     'http://127.0.0.1:6000/users/',
#     json={'email': "test12@nmmu.ru", 'password': 'tghRYdf45#$'}
# )
# #

# response = requests.post(
#     'http://127.0.0.1:6000/ads/',
#     json={"token": "71a96721-f157-485c-aa33-66590c469442", 'header': "Fourth commit", 'description': 'Lorem ipsum '
#                                                                                                     'caecat '
#                                                                                                     'cupidatat non '
#                                                                                                     'proid'}
# )
# response = requests.get(
#     'http://127.0.0.1:6000/ads/',
#     json={"ad_id": "3"}
# )
#
# response = requests.delete(
#     'http://127.0.0.1:6000/ads/',
#     json={"ad_id": "3", 'user_id': '8'}
# )
response = requests.get(
    'http://127.0.0.1:6000/ads/'
    # json={"ad_id": "3"}
)


print(response.text)
