import sqlite3
from config import DB_NAME


def create_database():
    """Создает таблицу requests, если она не существует"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            contact TEXT NOT NULL,
            issue TEXT NOT NULL,
            preferred_time TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def save_request(username, contact, issue, preferred_time):
    """Сохраняет заявку в базу данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO requests (username, contact, issue, preferred_time)
        VALUES (?, ?, ?, ?)
    ''', (username, contact, issue, preferred_time))

    conn.commit()
    conn.close()
