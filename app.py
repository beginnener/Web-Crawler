from flask import Flask, render_template, request
from crawler import dfs_search_for_keyword_and_save
import mysql.connector
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        seed = request.form.get('seed')
        keyword = request.form.get('keyword')
        if seed and keyword:
            if not seed.startswith("http"):
                seed = "https://" + seed
            result = dfs_search_for_keyword_and_save(seed, keyword)
    return render_template('index.html', result=result)

@app.route('/history')
def history():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # sesuaikan jika pakai password
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
