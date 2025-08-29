# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ---> ДОБАВЛЯЕМ НОВЫЕ СТРОКИ <---
# Копируем скрипт и делаем его исполняемым
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 5000

# Указываем наш скрипт как точку входа
ENTRYPOINT ["./entrypoint.sh"]

# Команда по умолчанию, которая будет передана в entrypoint.sh
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]