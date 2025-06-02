import sqlite3
import json
import os

DB_PATH = os.path.abspath('crawler.db')

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawl_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seed_url TEXT NOT NULL,
            keyword TEXT NOT NULL,
            visited_urls TEXT,
            found_urls TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_crawl_result(seed_url, keyword, visited_urls, found_urls):
    conn = connect_db()
    cursor = conn.cursor()

    visited_json = json.dumps(list(visited_urls))
    found_json = json.dumps(list(found_urls)) if found_urls else json.dumps([])

    cursor.execute('''
        INSERT INTO crawl_results (seed_url, keyword, visited_urls, found_urls)
        VALUES (?, ?, ?, ?)
    ''', (seed_url, keyword, visited_json, found_json))

    conn.commit()
    conn.close()
