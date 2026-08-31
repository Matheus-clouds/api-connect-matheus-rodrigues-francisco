from flask import Blueprint

from app.controllers import users_controller

users_bp = Blueprint("users", __name__, url_prefix="/api/usuarios")


@users_bp.get("")
def list_users():
    return users_controller.list_users()


@users_bp.get("/<int:user_id>")
def get_user(user_id):
    return users_controller.get_user(user_id)


@users_bp.post("")
def create_user():
    return users_controller.create_user()


@users_bp.patch("/<int:user_id>")
@users_bp.put("/<int:user_id>")
def update_user(user_id):
    return users_controller.update_user(user_id)


@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    return users_controller.delete_user(user_id)
