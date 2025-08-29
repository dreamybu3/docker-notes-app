# app/main.py (НОВАЯ, ИСПРАВЛЕННАЯ ВЕРСИЯ)

import os
import time
import psycopg2
import click # <-- Добавляем импорт
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    # Уменьшим время ожидания для быстрого падения в случае проблем
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        connect_timeout=3
    )
    return conn

# --- УДАЛЯЕМ СТАРЫЙ БЛОК ИНИЦИАЛИЗАЦИИ ОТСЮДА ---

# Создаем функцию для инициализации БД
def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS notes (id serial PRIMARY KEY, content TEXT);")
                conn.commit()
            conn.close()
            print("Database initialized successfully.")
            return
        except psycopg2.OperationalError as e:
            retries -= 1
            print(f"DB connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Could not initialize database.")

# Регистрируем функцию как CLI команду Flask
@app.cli.command("init-db")
def init_db_command():
    """Создает таблицы базы данных."""
    init_db()
    click.echo("Initialized the database.")

@app.route('/')
def index():
    """Отображает все заметки."""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM notes ORDER BY id DESC;')
        notes = cur.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=('POST',))
def add_note():
    """Добавляет новую заметку."""
    content = request.form['content']
    if content:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('INSERT INTO notes (content) VALUES (%s)', (content,))
            conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)