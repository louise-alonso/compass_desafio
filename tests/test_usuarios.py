import requests
import pytest
from faker import Faker

fake = Faker()
BASE_URL = "https://compassuol.serverest.dev"

def gerar_email_unico():
    return fake.unique.email()

def gerar_usuario_payload(nome=None, email=None, administrador="true"):
    return {
        "nome": nome or fake.first_name(),
        "email": email or gerar_email_unico(),
        "password": "teste123",
        "administrador": administrador
    }

class TestUsuariosAPI:
    """Suite de testes para o endpoint /usuarios da ServeRest"""

    @pytest.fixture
    def usuario_criado(self):
        """Fixture para criar um usuário antes do teste e excluí-lo depois (teardown)."""
        payload = gerar_usuario_payload()
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = response.json().get("_id")
        
        yield {"id": user_id, "payload": payload}
        
        if user_id:
            requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    # 1. Listagem de Usuários com Sucesso
    def test_01_listar_usuarios_com_sucesso(self):
        response = requests.get(f"{BASE_URL}/usuarios")
        body = response.json()
        
        assert response.status_code == 200
        assert "quantidade" in body
        assert isinstance(body["usuarios"], list)

    # 2. Cadastro Válido
    def test_02_cadastrar_usuario_valido_retorna_201(self):
        payload = gerar_usuario_payload()
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        body = response.json()
        
        assert response.status_code == 201
        assert body["message"] == "Cadastro realizado com sucesso"
        assert "_id" in body
        
        requests.delete(f"{BASE_URL}/usuarios/{body['_id']}")

    # 3. Cadastro Inválido: Email Duplicado
    def test_03_cadastrar_usuario_email_duplicado_deve_falhar(self, usuario_criado):
        email_existente = usuario_criado["payload"]["email"]
        payload_duplicado = gerar_usuario_payload(email=email_existente)
        
        response = requests.post(f"{BASE_URL}/usuarios", json=payload_duplicado)
        assert response.status_code == 400
        assert response.json()["message"] == "Este email já está sendo usado"

    # 4. Cadastro Inválido: Sem campo Nome
    def test_04_cadastrar_usuario_sem_campo_nome_retorna_400(self):
        payload = gerar_usuario_payload()
        del payload["nome"]
        
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert response.status_code == 400
        assert response.json()["nome"] == "nome é obrigatório"

    # 5. Cadastro Inválido: Sem campo Email
    def test_05_cadastrar_usuario_sem_campo_email_retorna_400(self):
        payload = gerar_usuario_payload()
        del payload["email"]
        
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert response.status_code == 400
        assert response.json()["email"] == "email é obrigatório"

    # 6. Cadastro Inválido: Sem campo Password
    def test_06_cadastrar_usuario_sem_campo_password_retorna_400(self):
        payload = gerar_usuario_payload()
        del payload["password"]
        
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert response.status_code == 400
        assert response.json()["password"] == "password é obrigatório"

    # 7. Busca Válida por ID
    def test_07_buscar_usuario_por_id_valido(self, usuario_criado):
        user_id = usuario_criado["id"]
        payload_original = usuario_criado["payload"]
        
        response = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        body = response.json()
        
        assert response.status_code == 200
        assert body["nome"] == payload_original["nome"]
        assert body["email"] == payload_original["email"]

    # 8. Busca Inválida (ID Inexistente)
    def test_08_buscar_usuario_id_inexistente_retorna_400(self):
        response = requests.get(f"{BASE_URL}/usuarios/9999999999999999")
        assert response.status_code == 400

    # 9. Atualização com Sucesso
    def test_09_atualizar_usuario_existente_retorna_200(self, usuario_criado):
        user_id = usuario_criado["id"]
        payload_atualizado = gerar_usuario_payload(nome="Nome Atualizado via PUT")
        
        response = requests.put(f"{BASE_URL}/usuarios/{user_id}", json=payload_atualizado)
        assert response.status_code == 200
        assert response.json()["message"] == "Registro alterado com sucesso"

    # 10. Exclusão com Sucesso
    def test_10_excluir_usuario_existente_retorna_200(self):
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        
        response = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        assert response.status_code == 200
        
        mensagem = response.json()["message"]
        assert "excluído" in mensagem or "excluido" in mensagem