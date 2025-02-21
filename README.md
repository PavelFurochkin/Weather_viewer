# Погода
- - -
Веб-приложение для просмотра текущей погоды. 
Пользователь может зарегистрироваться и добавить в коллекцию одну или несколько локаций (городов, сёл, других пунктов), 
после чего главная страница приложения начинает отображать список локаций с их текущей погодой

## Запуск проекта
- - -
1. Скачайте проект на локальную машину
2. Установите Docker
3. Создайте файл .env в корне проекта
4. выполните команду ` docker compose up -d`

### Файл .env

- POSTGRES_ENGINE=Используемый драйвер для работы с БД
- POSTGRES_DB=Имя БД
- POSTGRES_USER=Имя пользователя от БД
- POSTGRES_PASSWORD=Пароль от БД
- POSTGRES_HOST=Имя контейнера, в котором запущен PostgreSQL
- POSTGRES_PORT=Порт БД
- WEATHER_API_KEY=Уникальный ключ [OpenWeatherAPI](https://home.openweathermap.org/api_keys)
- SECRET_KEY= секретный ключ Django
- NGINX_EXTERNAL_PORT=80(Порт БД)

## Доступные страницы
- - - 

- `/` главная страница
- ` users/login` авторизация
- ` search/` страница результатов пойска

## Стек
- - -
- Python 3.11
- Django 5.1.2
- PostgreSQL
- docker
- unittest
- requests
- HTML/CSS(Bootstrap5)

