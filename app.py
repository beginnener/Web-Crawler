from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        seed = request.form["seed"]
        keyword = request.form["keyword"]

        try:
            response = requests.get(seed, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            found = keyword.lower() in page_text
            result = {
                "url": seed,
                "keyword": keyword,
                "found": found
            }
        except Exception as e:
            result = {
                "error": str(e)
            }

    return render_template("index.html", result=result)
    
if __name__ == "__main__":
    app.run(debug=True)