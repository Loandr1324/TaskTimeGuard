# TaskTimeGuard

### Описание

------------
Скрипт для контроля запуска модулей(скриптов).

Данный скрипт получает информацию из Google таблицы.

Проверяет интервал времени с последнего запуска модуля(скрипта) на соответствие разрешённому интервалу времени 
указанному в Google таблице.
Для работы с google таблицей требуется создать сервисный аккаунт google. 

При обнаружении нарушений, отправляет сообщение о тревоге в телеграм.

### Доступы

------------

Данные для доступа размещаем в файл config.py в виде словаря:    
```python
TOKEN_BOT: str = 'токен вашего бота'
AUTH_GOOGLE: dict = {
    'GOOGLE_CLIENT_ID': 'ваш google клиент id',
    'GOOGLE_CLIENT_SECRET': 'ваш google ',
    'KEY_WORKBOOK': 'id вашей google таблицы'
}
FILE_NAME_LOG: str = 'имя вашего лог файла'
```
Так же в папке проекта должен [services/google_table](services/google_table) необходимо расположить файл 
`credentials.json` с параметрами подключения к Google таблице
```python
{
  "type": "service_account",
  "project_id": "ваше наименование проeкта",
  "private_key_id": "ваш id",
  "private_key": "ваш ключ",
  "client_email": "email вашего сервис, который добавляется как редактор к гугл таблице",
  "client_id": "id вашего сервиса",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "url сертификата вашего сервиса",
  "universe_domain": "googleapis.com"
}
```

### Примечание 

------------
Для логирования используется библиотека [logguru](https://loguru.readthedocs.io/en/stable/overview.html)
Наименование лог файла прописывается в файле config.py в переменную `FILE_NAME_CONFIG`