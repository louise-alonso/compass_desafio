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
        
        # O yield pausa a fixture, entrega os dados para o teste usar, e retoma depois do teste
        yield {"id": user_id, "payload": payload}
        
        # Limpeza GARANTIDA, independentemente de o teste passar ou falhar
        if user_id:
            requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    def test_01_listar_usuarios_deve_retornar_status_200(self):
        response = requests.get(f"{BASE_URL}/usuarios")
        assert response.status_code == 200

    def test_02_listar_usuarios_deve_conter_estrutura_valida(self):
        response = requests.get(f"{BASE_URL}/usuarios")
        body = response.json()
        assert "quantidade" in body
        assert "usuarios" in body
        assert isinstance(body["usuarios"], list)
        assert isinstance(body["quantidade"], int)

    def test_03_listar_usuarios_quantidade_deve_corresponder_ao_tamanho_da_lista(self):
        response = requests.get(f"{BASE_URL}/usuarios")
        body = response.json()
        assert body["quantidade"] == len(body["usuarios"])

    def test_04_cadastrar_usuario_com_dados_validos_retorna_201(self):
        payload = gerar_usuario_payload()
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        
        assert response.status_code == 201
        body = response.json()
        assert body["message"] == "Cadastro realizado com sucesso"
        assert "_id" in body
        
        # Limpeza limpa e segura (aspas simples dentro da f-string)
        requests.delete(f"{BASE_URL}/usuarios/{body['_id']}")

    def test_05_cadastrar_usuario_com_email_duplicado_deve_falhar(self, usuario_criado):
        # Utiliza o email que acabou de ser criado pela fixture
        email_existente = usuario_criado["payload"]["email"]
        
        payload_duplicado = gerar_usuario_payload(email=email_existente)
        response = requests.post(f"{BASE_URL}/usuarios", json=payload_duplicado)
        
        assert response.status_code == 400

    def test_06_cadastrar_usuario_sem_campo_nome_deve_retornar_400(self):
        payload = {"email": gerar_email_unico(), "password": "teste123", "administrador": "true"}
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert response.status_code == 400

    def test_07_cadastrar_usuario_sem_campo_email_deve_retornar_400(self):
        payload = {"nome": "Usuario Sem Email", "password": "teste123", "administrador": "true"}
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert response.status_code == 400

    def test_08_cadastrar_usuario_sem_campo_password_deve_retornar_400(self):
        payload = {"nome": fake.first_name(), "email": gerar_email_unico(), "administrador": "true"}
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert response.status_code == 400

    def test_09_buscar_usuario_por_id_valido_deve_retornar_dados_corretos(self, usuario_criado):
        user_id = usuario_criado["id"]
        payload_original = usuario_criado["payload"]
        
        response = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        
        assert response.status_code == 200
        body = response.json()
        assert body["_id"] == user_id
        assert body["nome"] == payload_original["nome"]
        assert body["email"] == payload_original["email"]

    def test_10_buscar_usuario_com_id_inexistente_deve_retornar_400(self):
        response = requests.get(f"{BASE_URL}/usuarios/9999999999999999")
        assert response.status_code == 400

    def test_11_atualizar_usuario_existente_deve_retornar_200(self, usuario_criado):
        user_id = usuario_criado["id"]
        payload_atualizado = {
            "nome": "Nome Atualizado via PUT",
            "email": gerar_email_unico(),
            "password": "novaSenha@123",
            "administrador": "false"
        }
        
        response = requests.put(f"{BASE_URL}/usuarios/{user_id}", json=payload_atualizado)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Registro alterado com sucesso"

    def test_12_atualizar_apenas_um_campo_deve_ser_rejeitado(self, usuario_criado):
        user_id = usuario_criado["id"]
        response = requests.put(f"{BASE_URL}/usuarios/{user_id}", json={"nome": "Apenas Nome Mudou"})
        assert response.status_code == 400

    def test_13_excluir_usuario_existente_deve_retornar_200(self):
        # Neste teste criamos manualmente pois o objetivo primário dele é testar o DELETE
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        
        response = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        assert response.status_code == 200
        
        mensagem = response.json()["message"]
        assert "excluído" in mensagem or "excluido" in mensagem
        
        verificar = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        assert verificar.status_code == 400

    def test_14_excluir_usuario_ja_excluido_deve_ser_idempotente(self):
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        
        requests.delete(f"{BASE_URL}/usuarios/{user_id}") # Primeiro delete
        
        response2 = requests.delete(f"{BASE_URL}/usuarios/{user_id}") # Segundo delete
        assert response2.status_code == 200
        assert "Nenhum" in response2.json()["message"]

    def test_15_excluir_usuario_com_id_inexistente_deve_retornar_200(self):
        response = requests.delete(f"{BASE_URL}/usuarios/8888888888888888")
        assert response.status_code == 200
        assert "Nenhum" in response.json()["message"]