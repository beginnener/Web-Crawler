import mysql.connector

def create_database_and_table():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''  
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS crawler_db")
    conn.commit()
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='crawler_db'
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
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_database_and_table()
    print("Database and table created successfully!")
