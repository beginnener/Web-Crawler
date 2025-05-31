# app.py
from flask import Flask, render_template, request
from crawler import bfs_crawl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        seed = request.form.get('seed')
        if seed:
            if not seed.startswith("http"):
                seed = "https://" + seed
            result = bfs_crawl(seed)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
