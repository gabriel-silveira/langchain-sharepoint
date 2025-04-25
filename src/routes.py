from flask import Blueprint, request, jsonify
from src.crawler import WebCrawler

crawler_routes = Blueprint(
    'simple_page',
    __name__,
    template_folder='templates',
)


@crawler_routes.route("/api/crawl", methods=["POST"])
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
