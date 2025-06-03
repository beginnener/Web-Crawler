from flask import Flask, render_template, request
from crawler import dfs_search_for_keyword_and_save
import mysql.connector
import json

app = Flask(__name__)

def get_cached_result(seed_url, keyword, max_depth=None, max_pages=None):
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
    raw_results = cursor.fetchall()
    conn.close()

    filtered_results = []

    for r in raw_results:
        r['visited_urls'] = json.loads(r['visited_urls']) if r['visited_urls'] else []
        r['found_urls'] = json.loads(r['found_urls']) if r['found_urls'] else []

        # Hitung depth dari panjang rute
        current_depth = len(r['visited_urls'])

        # Cek apakah sesuai dengan kriteria filter
        if max_depth is not None and current_depth > max_depth:
            continue

        filtered_results.append(r)

        # Batasi jumlah hasil (jika max_pages di-set)
        if max_pages is not None and len(filtered_results) >= max_pages:
            break

    return filtered_results if filtered_results else None
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seed = request.form.get('seed')
        keyword = request.form.get('keyword')
        depth = int(request.form.get('depth'))
        max_result = int(request.form.get('max_result'))

        if seed and keyword:
            if not seed.startswith("http"):
                seed = "https://" + seed

            cached_results = get_cached_result(seed, keyword, depth, max_result)
            results = cached_results if cached_results else []

            # Kalau hasil masih kurang, lanjut crawling sisanya
            if len(results) < max_result:
                new_results = dfs_search_for_keyword_and_save(seed, keyword, max_result, depth)
                results = get_cached_result(seed, keyword, depth, len(results))

            return render_template('crawler.html', results=results)

    # GET request
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
