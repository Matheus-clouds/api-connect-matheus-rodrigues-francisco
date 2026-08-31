import unittest

from app import create_app
from app.services.user_service import user_service


class UsersApiTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app({"TESTING": True})
        self.client = app.test_client()
        user_service.repository._users = [
            {"id": 1, "nome": "Ana Souza", "email": "ana.souza@exemplo.com", "idade": 28}
        ]
        user_service.repository._next_id = 2

    def test_list_users_returns_json(self):
        response = self.client.get("/api/usuarios")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["total"], 1)

    def test_create_user(self):
        response = self.client.post(
            "/api/usuarios",
            json={"nome": "Carlos Silva", "email": "carlos@exemplo.com", "idade": 25},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["id"], 2)

    def test_rejects_invalid_user(self):
        response = self.client.post("/api/usuarios", json={"nome": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json["error"]["details"])

    def test_update_and_get_user(self):
        update_response = self.client.patch("/api/usuarios/1", json={"idade": 29})
        get_response = self.client.get("/api/usuarios/1")
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(get_response.json["data"]["idade"], 29)

    def test_put_requires_complete_representation(self):
        response = self.client.put("/api/usuarios/1", json={"nome": "Ana Maria"})
        self.assertEqual(response.status_code, 400)

    def test_rejects_duplicate_email(self):
        response = self.client.post(
            "/api/usuarios", json={"nome": "Outra Ana", "email": "ana.souza@exemplo.com"}
        )
        self.assertEqual(response.status_code, 409)

    def test_delete_user(self):
        response = self.client.delete("/api/usuarios/1")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
