from flask import Flask, render_template, request
from crawler import bfs_search_for_keyword
from crawler import bfs_search_for_keyword_and_save

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
            result = bfs_search_for_keyword(seed, keyword)
            # Panggil fungsi crawling sekaligus simpan ke DB
            result = bfs_search_for_keyword_and_save(seed, keyword)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)