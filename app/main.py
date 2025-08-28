import os
import time
import psycopg2
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST"),
                database=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print("Не удалось подключиться к БД. Попытка через 5 секунд...")
            time.sleep(5)
    raise Exception("Не удалось подключиться к базе данных после нескольких попыток.")

# Инициализация таблицы при первом запуске
conn = get_db_connection()
with conn.cursor() as cur:
    cur.execute("CREATE TABLE IF NOT EXISTS notes (id serial PRIMARY KEY, content TEXT);")
    conn.commit()
conn.close()


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
    # Эта секция используется только для локального запуска без Docker
    app.run(host='0.0.0.0', port=5000)