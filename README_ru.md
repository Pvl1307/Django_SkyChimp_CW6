# Mailing list management, administration and statistics collection service


## Описание
Чтобы удержать текущих клиентов, часто используют вспомогательные, или «прогревающие», рассылки для информирования и привлечения клиентов.
В связи с этим был разработан сервис управления рассылками, администрирования и получения статистики.

## Установка
1. Скачайте проект в домашнюю директорию.
2. Активируйте виртуальное окружение командой: poetry shell.
3. Установите зависимости командой: poetry install.

## Перед первым запуском программы:
1. Создайте Базу данных (в данной работе используется PostgreSQL) и перейдите в файл .env.sample и пропишите переменные окружения в формате(все данные после "=" в виде примера):

```ini
SECRET_KEY='django-secret-key'
DEBUG=True/False

DATABASE_NAME='name_of_db'
DATABASE_USER='db_user'
DATABASE_PASSWORD='your_password'
DATABASE_HOST='127.0.0.1'
DATABASE_PORT=5432

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=email.host.com
EMAIL_PORT=465
EMAIL_HOST_USER=ur_mail@gmail.com/ru
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True/False
EMAIL_USE_SSL=True/False

CACHE_ENABLED=True/False
CACHE_LOCATION=cashe_location://127.0.0.0:6477
```

2. Установите Redis

3. В терминале выполните следующие команды:

   - `python manage.py migrate`
   - `python manage.py loaddata group_data.json`
   - `python manage.py loaddata users_data.json`

   (Пароль и логин для суперпользователя и менеджера можно найти в файлах **cm.py** и **csu.py** в `users/management/commands`).

   Команда для запуска сервера: `python manage.py runserver`

   Команда для запуска apscheduler: `python manage.py runapscheduler`


## Работа кода

**Для обычного пользователя:**

При запуске сервера будет открыта гланая страница со статиской сайта, а также статьями, связаные с данным сервисом. Перед использованием возможностей сервиса, придется зарегестрироваться, а также пройти верификацию почты.
После верификации почты будут доступны такие возможности как создание/просмотр/редактирование/удаление своих клиентов, сообщений и рассылок, и также просмотр логгов по отправке рассылки.


**Для суперюзера/менеджера(группа-**managers**):**

Та же главная страница, также возможность управлять активность пользователя сервера(**is_active**) и статусом рассылки (**Created/Started/Done**)

##Для завершения работы

В терминале, где запущен сервер, прожать **Ctrl + C**








