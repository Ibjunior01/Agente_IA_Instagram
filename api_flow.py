# api_flow.py — API da FLOW para receber chamadas do Make.com

from flask import Flask, request, jsonify
from agente_flowcore import agente_flowcore
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Chave de segurança para proteger sua API
API_KEY = os.getenv("API_KEY", "flowcore_chave_secreta")

@app.route("/flow", methods=["POST"])
def receber_mensagem():
    chave = request.headers.get("X-API-Key")
    if chave != API_KEY:
        return jsonify({"erro": "Não autorizado"}), 401

    dados = request.json
    mensagem = dados.get("mensagem", "")

    if not mensagem:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = agente_flowcore(mensagem)
    return jsonify({"resposta": resposta}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "FLOW online"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)