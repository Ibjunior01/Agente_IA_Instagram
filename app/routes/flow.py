from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.config import (
    API_KEY,
    MAX_MESSAGE_LENGTH,
    MAX_USER_ID_LENGTH,
)
from app.services.agent_service import processar_mensagem

flow_bp = Blueprint(
    "flow",
    __name__,
)


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
)


def obter_chave_rate_limit_usuario():
    """
    Usa user_id como identificador principal do rate limit.

    Quando o payload não possui um user_id válido,
    utiliza o endereço IP como fallback.
    """
    dados = request.get_json(silent=True)

    if isinstance(dados, dict):
        user_id = dados.get("user_id")

        if isinstance(user_id, str) and user_id.strip():
            return f"user:{user_id.strip()}"

    return f"ip:{get_remote_address()}"


@flow_bp.route("/flow", methods=["POST"])
@limiter.limit(
    "10 per minute",
    key_func=obter_chave_rate_limit_usuario,
)
@limiter.limit(
    "120 per minute",
    key_func=get_remote_address,
)
def receber_mensagem():
    chave = request.headers.get("X-API-Key")

    if chave != API_KEY:
        return jsonify(
            {
                "erro": "Não autorizado"
            }
        ), 401

    if not request.is_json:
        return jsonify(
            {
                "erro": "Content-Type deve ser application/json"
            }
        ), 415

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify(
            {
                "erro": "JSON inválido ou ausente"
            }
        ), 400

    user_id = dados.get("user_id")
    mensagem = dados.get("mensagem")

    if user_id is None:
        return jsonify(
            {
                "erro": "user_id é obrigatório"
            }
        ), 400

    if not isinstance(user_id, str):
        return jsonify(
            {
                "erro": "user_id deve ser uma string"
            }
        ), 400

    user_id = user_id.strip()

    if not user_id:
        return jsonify(
            {
                "erro": "user_id é obrigatório"
            }
        ), 400

    if len(user_id) > MAX_USER_ID_LENGTH:
        return jsonify(
            {
                "erro": (
                    "user_id deve possuir no máximo "
                    f"{MAX_USER_ID_LENGTH} caracteres"
                )
            }
        ), 400

    if mensagem is None:
        return jsonify(
            {
                "erro": "mensagem é obrigatória"
            }
        ), 400

    if not isinstance(mensagem, str):
        return jsonify(
            {
                "erro": "mensagem deve ser uma string"
            }
        ), 400

    mensagem = mensagem.strip()

    if not mensagem:
        return jsonify(
            {
                "erro": "mensagem não pode ser vazia"
            }
        ), 400

    if len(mensagem) > MAX_MESSAGE_LENGTH:
        return jsonify(
            {
                "erro": (
                    "mensagem deve possuir no máximo "
                    f"{MAX_MESSAGE_LENGTH} caracteres"
                )
            }
        ), 400

    resposta = processar_mensagem(
        user_id=user_id,
        mensagem_usuario=mensagem,
    )

    return jsonify(
        {
            "resposta": resposta
        }
    ), 200


@flow_bp.route("/health", methods=["GET"])
@limiter.exempt
def health():
    return jsonify(
        {
            "status": "FLOW online"
        }
    ), 200