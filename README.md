## Это учебный сервер Flask для сайта объявлений

### Уствновка пакетов
```pip install -r requirements.txt```

### Запуск БД
```docker-compose up```

### Запуск сервера
```python server.py```

### Создание пользователя 
```requests.post('http://127.0.0.1:6000/users/',json={'email': "test13@nmmu.ru", 'password': 'tghRYdf45#$'})```

### Создание объявления

```requests.post('http://127.0.0.1:6000/ads/', json={"token": "71a96721-f157-485c-aa33-66590c469442", 'header': "Fourth commit", 'description': 'Lorem ipsum caecat cupidatat non proid'})```

### Получение объявления

```requests.get('http://127.0.0.1:6000/ads/', json={"ad_id": "3"})```

### Удаление объявления

```requests.get('http://127.0.0.1:6000/ads/', json={"ad_id": "3", 'user_id': '8'})```

