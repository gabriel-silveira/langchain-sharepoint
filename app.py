from flask import Flask, request, jsonify
from flask_cors import CORS
from src.sharepoint_rag_chain import SharePointRAG

app = Flask(__name__)
CORS(app)

rag_chain = SharePointRAG().get_chain()


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    # Validação de campos obrigatórios
    if not data:
        return jsonify({"error": "Requisição inválida. Corpo JSON ausente."}), 400

    question = data.get("question")
    session_id = data.get("session_id", "default_user")

    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "O campo 'question' é obrigatório."}), 400

    if not isinstance(session_id, str) or not session_id.strip():
        return jsonify({"error": "O campo 'session_id' é obrigatório."}), 400

    try:
        response = rag_chain.invoke(
            {"question": question},
            config={"configurable": {"session_id": session_id}}
        )

        return jsonify({"answer": response["answer"]})
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a pergunta: {str(e)}"}), 500


@app.route("/", methods=["GET"])
def index():
    return "🚀 API RAG está rodando!"


if __name__ == "__main__":
    app.run(debug=True)
