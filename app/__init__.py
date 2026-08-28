from flask import Flask, jsonify

from app.routes.flow import flow_bp, limiter


def create_app():
    """
    Cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    limiter.init_app(app)

    app.register_blueprint(flow_bp)

    @app.errorhandler(429)
    def rate_limit_excedido(_erro):
        return jsonify(
            {
                "erro": (
                    "Muitas requisições. "
                    "Tente novamente em alguns instantes."
                )
            }
        ), 429

    return app