# Messanger


# Инструменты
Язык: Python 3.10

Фреймворк: FastApi

База данных: Postgres 16

# Как запустить
### С Docker-compose
1. Перейти в директорию с файлом
```commandline
cd wb_chat
``` 
2. Собрать Docker-compose образ
```commandline
docker-compose build
```
3. Запустить Docker-compose образ
```commandline
docker-compose up
```

# Это должен помнить каждый
Чтобы подключиться к вебсокету используется адрес: ws://localhost:8000/ws?token={token}.

Он ВСЕ отдает в виде json и принимает только json.