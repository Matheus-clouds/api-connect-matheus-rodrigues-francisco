from app.repositories.user_repository import UserRepository


class ValidationError(Exception):
    def __init__(self, details):
        self.details = details
        super().__init__("Dados de entrada invalidos.")


class ConflictError(Exception):
    def __init__(self, details):
        self.details = details
        super().__init__("Conflito de dados.")


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def list_users(self):
        return self.repository.list()

    def get_user(self, user_id):
        return self.repository.get_by_id(user_id)

    def create_user(self, payload):
        attributes = self._validate(payload, partial=False)
        if self.repository.get_by_email(attributes["email"]):
            raise ConflictError({"email": "Ja existe um usuario cadastrado com este e-mail."})
        return self.repository.create(attributes)

    def update_user(self, user_id, payload, partial):
        user = self.get_user(user_id)
        if not user:
            return None

        attributes = self._validate(payload, partial=partial)
        if "email" in attributes:
            same_email_user = self.repository.get_by_email(attributes["email"])
            if same_email_user and same_email_user["id"] != user_id:
                raise ConflictError({"email": "Ja existe um usuario cadastrado com este e-mail."})
        return self.repository.update(user, attributes)

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False
        self.repository.delete(user)
        return True

    @staticmethod
    def _validate(payload, partial):
        if not isinstance(payload, dict):
            raise ValidationError({"body": "O corpo da requisicao deve ser um objeto JSON."})

        allowed_fields = {"nome", "email", "idade"}
        errors = {}
        extra_fields = set(payload) - allowed_fields
        if extra_fields:
            errors["body"] = f"Campos nao permitidos: {', '.join(sorted(extra_fields))}."

        if not partial:
            for field in ("nome", "email"):
                if field not in payload:
                    errors[field] = "Este campo e obrigatorio."
        elif not payload:
            errors["body"] = "Envie ao menos um campo para atualizacao."

        attributes = {}
        if "nome" in payload:
            nome = payload["nome"]
            if not isinstance(nome, str) or not nome.strip():
                errors["nome"] = "Informe um nome nao vazio."
            elif len(nome.strip()) > 100:
                errors["nome"] = "O nome deve ter no maximo 100 caracteres."
            else:
                attributes["nome"] = nome.strip()

        if "email" in payload:
            email = payload["email"]
            if not isinstance(email, str) or "@" not in email or email.startswith("@"):
                errors["email"] = "Informe um e-mail valido."
            elif len(email.strip()) > 254:
                errors["email"] = "O e-mail deve ter no maximo 254 caracteres."
            else:
                attributes["email"] = email.strip().lower()

        if "idade" in payload:
            idade = payload["idade"]
            if isinstance(idade, bool) or not isinstance(idade, int) or not 0 <= idade <= 130:
                errors["idade"] = "A idade deve ser um numero inteiro entre 0 e 130."
            else:
                attributes["idade"] = idade

        if errors:
            raise ValidationError(errors)
        return attributes


user_service = UserService()
