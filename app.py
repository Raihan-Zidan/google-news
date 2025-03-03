from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)

def scrape_google_news(query):
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for article in soup.select(".SoaBEf"):
        title_elem = article.select_one("div.MBeuO")
        title = title_elem.text if title_elem else "No Title"
        link = article.select_one("a")["href"] if article.select_one("a") else "#"
        
        source_elem = article.select_one(".MgUUmf span")
        source = source_elem.text if source_elem else "Unknown Source"

        time_elem = article.select_one(".LfVVr")
        time = time_elem.text if time_elem else "Unknown Time"

        # Ambil gambar thumbnail
        img_elem = article.select_one("img")
        thumbnail = img_elem["src"] if img_elem else "https://via.placeholder.com/150"

        results.append({
            "title": title,
            "link": link,
            "source": source,
            "time": time,
            "thumbnail": thumbnail
        })

    return results

@app.route("/scrape", methods=["GET"])
def scrape():
    query = request.args.get("query", "berita terbaru")
    data = scrape_google_news(query)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
