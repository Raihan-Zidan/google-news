from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def scrape_google_images(query, start=0):
    url = f"https://www.google.com/search?q={query}&tbm=isch&start={start}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for img in soup.select("img"):
        img_url = img["src"] if "src" in img.attrs else img.get("data-src", "")
        if img_url.startswith("http"):  # Hindari gambar yang bukan URL valid
            results.append({"image": img_url})

    return results

@app.route("/scrape", methods=["GET"])
def scrape():
    query = request.args.get("query", "random")
    start = request.args.get("start", 0, type=int)
    data = scrape_google_images(query, start)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
