import mysql.connector

def create_table():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',   # ganti dengan password MySQL kamu
        database='crawler_db'       # pastikan database ini sudah dibuat
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawl_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            seed_url TEXT NOT NULL,
            keyword TEXT NOT NULL,
            visited_urls TEXT,
            found_urls TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    print("Table created successfully!")
