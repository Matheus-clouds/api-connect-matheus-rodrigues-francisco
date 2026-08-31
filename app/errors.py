from flask import jsonify
from werkzeug.exceptions import HTTPException


def error_response(status, message, details=None):
    """Gera o contrato padrao para respostas de erro."""
    body = {"error": {"status": status, "message": message}}
    if details:
        body["error"]["details"] = details
    return jsonify(body), status


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return error_response(error.code, error.description)

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        app.logger.exception(error)
        return error_response(500, "Erro interno do servidor.")
