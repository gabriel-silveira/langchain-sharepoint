from flask import Flask, request, jsonify
from src.crawler import WebCrawler

app = Flask(__name__)


@app.route("/api/crawl", methods=["POST"])
def chat():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Requisição inválida. Corpo JSON ausente."}), 400

    url = data.get("url")
    limit = data.get("limit")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "O campo 'url' é obrigatório."}), 400

    crawler = WebCrawler(url=url, limit=limit)

    result = crawler.start()

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
