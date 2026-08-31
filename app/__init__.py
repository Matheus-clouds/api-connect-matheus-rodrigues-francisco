from flask import Flask

from app.errors import register_error_handlers
from app.routes.users import users_bp


def create_app(test_config=None):
    """Cria e configura a aplicacao Flask."""
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(users_bp)
    register_error_handlers(app)

    @app.get("/health")
    def health_check():
        return {"status": "ok", "message": "API Connect em execucao."}, 200

    return app
