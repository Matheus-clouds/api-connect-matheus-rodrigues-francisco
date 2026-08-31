class UserRepository:
    """Repositorio temporario que persiste dados apenas enquanto a API esta ligada."""

    def __init__(self):
        self._users = [
            {"id": 1, "nome": "Ana Souza", "email": "ana.souza@exemplo.com", "idade": 28},
            {"id": 2, "nome": "Bruno Lima", "email": "bruno.lima@exemplo.com", "idade": 34},
        ]
        self._next_id = 3

    def list(self):
        return self._users.copy()

    def get_by_id(self, user_id):
        return next((user for user in self._users if user["id"] == user_id), None)

    def get_by_email(self, email):
        return next((user for user in self._users if user["email"].lower() == email.lower()), None)

    def create(self, attributes):
        user = {"id": self._next_id, **attributes}
        self._users.append(user)
        self._next_id += 1
        return user

    def update(self, user, attributes):
        user.update(attributes)
        return user

    def delete(self, user):
        self._users.remove(user)
