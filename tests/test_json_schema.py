import requests
import pytest
from faker import Faker
from jsonschema import validate, ValidationError

fake = Faker()
BASE_URL = "https://compassuol.serverest.dev"


# ─── Schemas ────────────────────────────────────────────────────────────────

SCHEMA_LISTAR_USUARIOS = {
    "type": "object",
    "required": ["quantidade", "usuarios"],
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["nome", "email", "password", "administrador", "_id"],
                "properties": {
                    "nome":          {"type": "string"},
                    "email":         {"type": "string", "format": "email"},
                    "password":      {"type": "string"},
                    "administrador": {"type": "string", "enum": ["true", "false"]},
                    "_id":           {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}

SCHEMA_LOGIN_SUCESSO = {
    "type": "object",
    "required": ["message", "authorization"],
    "properties": {
        "message":       {"type": "string"},
        "authorization": {"type": "string", "minLength": 10},
    },
    "additionalProperties": False,
}

SCHEMA_LISTAR_PRODUTOS = {
    "type": "object",
    "required": ["quantidade", "produtos"],
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["nome", "preco", "descricao", "quantidade", "_id"],
                "properties": {
                    "nome":        {"type": "string"},
                    "preco":       {"type": "integer"},
                    "descricao":   {"type": "string"},
                    "quantidade":  {"type": "integer"},
                    "_id":         {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}


# ─── Helpers ────────────────────────────────────────────────────────────────

def _criar_admin():
    """Cria um usuário admin e retorna (email, password, user_id, token)."""
    user = {
        "nome": fake.first_name(),
        "email": fake.unique.email(),
        "password": "senha123",
        "administrador": "true",
    }
    res_user = requests.post(f"{BASE_URL}/usuarios", json=user)
    user_id = res_user.json().get("_id")

    res_login = requests.post(
        f"{BASE_URL}/login",
        json={"email": user["email"], "password": user["password"]},
    )
    token = res_login.json().get("authorization")
    return user["email"], user["password"], user_id, token


# ─── Testes de Schema ────────────────────────────────────────────────────────

class TestJsonSchema:
    """Extra 1 — Valida a estrutura das respostas via JSON Schema."""

    # ── Schema 1: GET /usuarios ──────────────────────────────────────────────
    def test_schema_listar_usuarios(self):
        """
        Verifica que GET /usuarios retorna o envelope correto:
        { quantidade: int, usuarios: [ { nome, email, password, administrador, _id } ] }
        """
        response = requests.get(f"{BASE_URL}/usuarios")

        assert response.status_code == 200, (
            f"Status inesperado: {response.status_code}"
        )

        try:
            validate(instance=response.json(), schema=SCHEMA_LISTAR_USUARIOS)
        except ValidationError as e:
            pytest.fail(f"Schema inválido em GET /usuarios: {e.message}")

    # ── Schema 2: POST /login ────────────────────────────────────────────────
    def test_schema_login_com_sucesso(self):
        """
        Verifica que POST /login (credenciais válidas) retorna:
        { message: str, authorization: str (≥10 chars) }
        """
        email, password, user_id, _ = _criar_admin()

        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"email": email, "password": password},
            )

            assert response.status_code == 200, (
                f"Status inesperado: {response.status_code}"
            )

            try:
                validate(instance=response.json(), schema=SCHEMA_LOGIN_SUCESSO)
            except ValidationError as e:
                pytest.fail(f"Schema inválido em POST /login: {e.message}")

        finally:
            if user_id:
                requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    # ── Schema 3: GET /produtos ──────────────────────────────────────────────
    def test_schema_listar_produtos(self):
        """
        Verifica que GET /produtos retorna o envelope correto:
        { quantidade: int, produtos: [ { nome, preco, descricao, quantidade, _id } ] }
        """
        response = requests.get(f"{BASE_URL}/produtos")

        assert response.status_code == 200, (
            f"Status inesperado: {response.status_code}"
        )

        try:
            validate(instance=response.json(), schema=SCHEMA_LISTAR_PRODUTOS)
        except ValidationError as e:
            pytest.fail(f"Schema inválido em GET /produtos: {e.message}")