import psycopg2
import os
from typing import Optional
from contextlib import contextmanager

DB_USER = os.getenv('user')
DB_PASSWORD = os.getenv('password')
DB_HOST = os.getenv('host')
DB_PORT = os.getenv('port')
DB_NAME = os.getenv('dbname')

@contextmanager
def get_conn():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    language TEXT DEFAULT 'uk'
                )
            ''')
            conn.commit()

def upsert_user(user_id: int, username: Optional[str], language: Optional[str] = None):
    with get_conn() as conn:
        with conn.cursor() as c:
            if language:
                c.execute('''
                    INSERT INTO users (user_id, username, language) VALUES (%s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET username=EXCLUDED.username, language=EXCLUDED.language
                ''', (user_id, username, language))
            else:
                c.execute('''
                    INSERT INTO users (user_id, username) VALUES (%s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET username=EXCLUDED.username
                ''', (user_id, username))
            conn.commit()

def get_user_language(user_id: int) -> str:
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('SELECT language FROM users WHERE user_id=%s', (user_id,))
            row = c.fetchone()
            return row[0] if row else 'uk'

def set_user_language(user_id: int, language: str):
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE users SET language=%s WHERE user_id=%s', (language, user_id))
            conn.commit()
