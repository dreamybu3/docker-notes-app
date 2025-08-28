# -*- coding: utf-8 -*-
from app.main import app

def test_index_route():
    """Тест проверяет, что главная страница открывается успешно."""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    # Вот ИСПРАВЛЕННАЯ строка
    assert "Мои заметки".encode('utf-8') in response.data