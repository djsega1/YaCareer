# YaCareer
![flake8 test]( https://github.com/DJsega1/YaCareer/actions/workflows/django.yml/badge.svg) 

## Клонируем репозиторий
```commandline 
git clone https://github.com/DJsega1/YaCareer.git
```

## Переходим в папку YaCareer
```commandline 
cd YaCareer
```

## Устанавливаем виртуальное окружение и все зависимости
| Windows | MacOs + Linux                            |Обозначение|
| :--------------- | :------------------------------ |:--------------- |
|`python -m venv venv`|`python3 -m venv venv`|Добавлем вирутальное окружение|
|`.\venv\Scripts\activate`|`source venv/bin/activate`| Активируем вирутальное окружение|
|`pip install -r requirements.txt`|`pip3 install -r requirements.txt`| Устанавливаем все зависимости в вирутальное окружение|

## Переходим в папку yacareer
```commandline 
cd yacareer
```

## Запускаем сайт
| Windows | MacOs + Linux                            |
| :--------------- | :------------------------------ |
|`python manage.py runserver`|`python3 manage.py runserver`|


## Настройка .env:
##### Примечание: это необязательно
### Создаем файл .env в корневой директории, прописываем туда секретные данные (пример - .env_example):
```commandline
SECRET_KEY=secret_key_1234567890
DEBUG=boolean_value
```

## Структура базы данных