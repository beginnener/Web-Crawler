from flask import Flask, render_template, request
from crawler import dfs_search_for_keyword_and_save
import mysql.connector
import json

app = Flask(__name__)

def get_cached_result(seed_url, keyword):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='crawler_db'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT * FROM crawl_results
        WHERE seed_url = %s AND keyword = %s
        ORDER BY created_at DESC
    ''', (seed_url, keyword))
    result = cursor.fetchall()
    conn.close()

    if result:
        for r in result:
            r['visited_urls'] = json.loads(r['visited_urls']) if r['visited_urls'] else []
            r['found_urls'] = json.loads(r['found_urls']) if r['found_urls'] else []
        return result
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        seed = request.form.get('seed')
        keyword = request.form.get('keyword')
        mode = request.form.get('mode', 'cached')

        if seed and keyword:
            if not seed.startswith("http"):
                seed = "https://" + seed

            if mode == 'fresh':
                # Hapus entri lama dengan seed dan keyword yang sama
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='crawler_db'
                )
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM crawl_results WHERE seed_url = %s AND keyword = %s",
                    (seed, keyword)
                )
                conn.commit()
                conn.close()

                # Lakukan crawling ulang
                result = dfs_search_for_keyword_and_save(seed, keyword)

            result = get_cached_result(seed, keyword)
            if not result:
                result = dfs_search_for_keyword_and_save(seed, keyword)
        return render_template('crawler.html', results=result)
    else:
        return render_template('index.html')

@app.route('/history')
def history():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='', 
        database='crawler_db'
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM crawl_results ORDER BY created_at DESC")
    records = cursor.fetchall()

    # Decode JSON ke Python list
    for r in records:
        r['visited_urls'] = json.loads(r['visited_urls']) if r['visited_urls'] else []
        r['found_urls'] = json.loads(r['found_urls']) if r['found_urls'] else []

    conn.close()
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
