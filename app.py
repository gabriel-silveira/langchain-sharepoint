from flask import Flask, request, jsonify
from src.sharepoint_rag_chain import SharePointRAG

app = Flask(__name__)

rag_chain = SharePointRAG().get_chain()


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    question = data.get("question")

    if not question:
        return jsonify({"error": "Pergunta não fornecida"}), 400

    try:
        response = rag_chain.invoke({"question": question})

        return jsonify({"answer": response["answer"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    return "🚀 API RAG está rodando!"


if __name__ == "__main__":
    app.run(debug=True)
