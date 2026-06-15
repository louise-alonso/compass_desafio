import requests
import pytest
from faker import Faker

fake = Faker()
BASE_URL = "https://compassuol.serverest.dev"

def gerar_usuario_payload():
    return {
        "nome": fake.first_name(),
        "email": fake.unique.email(),
        "password": "senha_padrao_123",
        "administrador": "true"
    }

class TestLoginAPI:

    @pytest.fixture
    def usuario_valido(self):
        payload = gerar_usuario_payload()
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = response.json().get("_id")
        
        yield payload 
        
        if user_id:
            requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    # 1. Login com credenciais válidas
    def test_01_login_com_credenciais_validas_retorna_200_e_token(self, usuario_valido):
        payload_login = {
            "email": usuario_valido["email"],
            "password": usuario_valido["password"]
        }
        
        response = requests.post(f"{BASE_URL}/login", json=payload_login)
        body = response.json()
        
        assert response.status_code == 200
        assert body["message"] == "Login realizado com sucesso"
        assert "authorization" in body  

    # 2. Falha no login com senha incorreta
    def test_02_login_com_senha_invalida_retorna_401(self, usuario_valido):
        payload_login = {
            "email": usuario_valido["email"],
            "password": "senha_errada_propositalmente"
        }
        
        response = requests.post(f"{BASE_URL}/login", json=payload_login)
        
        assert response.status_code == 401
        assert response.json()["message"] == "Email e/ou senha inválidos"

    # 3. Falha no login com email não cadastrado
    def test_03_login_com_email_nao_cadastrado_retorna_401(self):
        payload_login = {
            "email": fake.unique.email(),  
            "password": "qualquer_senha"
        }
        
        response = requests.post(f"{BASE_URL}/login", json=payload_login)
        
        assert response.status_code == 401
        assert response.json()["message"] == "Email e/ou senha inválidos"

    # 4. Falha no login com campos ausentes (sem senha)
    def test_04_login_com_campos_ausentes_retorna_400(self):
        payload_login = {"email": "teste@exemplo.com"}
        
        response = requests.post(f"{BASE_URL}/login", json=payload_login)
        
        assert response.status_code == 400
        assert response.json()["password"] == "password é obrigatório"