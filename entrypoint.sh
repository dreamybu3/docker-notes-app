#!/bin/sh

# Этот скрипт будет ждать, пока база данных не станет доступна,
# затем выполнит инициализацию и запустит gunicorn.

# Ждем, пока PostgreSQL не будет готов принимать соединения
# Мы используем встроенную утилиту pg_isready
while ! pg_isready -h $DB_HOST -p 5432 -q -U $DB_USER; do
  echo "$(date) - waiting for database to start"
  sleep 2
done

# Запускаем инициализацию базы данных
# FLASK_APP должен быть установлен
export FLASK_APP=app/main.py
flask init-db

# Запускаем основной процесс приложения (gunicorn)
# exec "$@" означает "выполнить команду, переданную этому скрипту"
exec "$@"