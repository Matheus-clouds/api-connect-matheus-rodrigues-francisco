from flask import jsonify, request
from werkzeug.exceptions import BadRequest

from app.errors import error_response
from app.services.user_service import ConflictError, ValidationError, user_service


def _json_body():
    """Obtém e valida o corpo JSON de uma requisição de escrita."""
    if not request.is_json:
        return None, error_response(415, "Content-Type deve ser application/json.")
    try:
        return request.get_json(), None
    except BadRequest:
        return None, error_response(400, "JSON invalido no corpo da requisicao.")


def list_users():
    users = user_service.list_users()
    return jsonify({"data": users, "total": len(users)}), 200


def get_user(user_id):
    user = user_service.get_user(user_id)
    if not user:
        return error_response(404, "Usuario nao encontrado.")
    return jsonify({"data": user}), 200


def create_user():
    payload, response = _json_body()
    if response:
        return response
    try:
        user = user_service.create_user(payload)
    except ValidationError as error:
        return error_response(400, "Dados de entrada invalidos.", error.details)
    except ConflictError as error:
        return error_response(409, "E-mail ja esta em uso.", error.details)
    return jsonify({"data": user, "message": "Usuario criado com sucesso."}), 201


def update_user(user_id):
    payload, response = _json_body()
    if response:
        return response
    try:
        user = user_service.update_user(user_id, payload, partial=request.method == "PATCH")
    except ValidationError as error:
        return error_response(400, "Dados de entrada invalidos.", error.details)
    except ConflictError as error:
        return error_response(409, "E-mail ja esta em uso.", error.details)
    if not user:
        return error_response(404, "Usuario nao encontrado.")
    return jsonify({"data": user, "message": "Usuario atualizado com sucesso."}), 200


def delete_user(user_id):
    if not user_service.delete_user(user_id):
        return error_response(404, "Usuario nao encontrado.")
    return "", 204
