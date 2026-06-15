import requests
import pytest
from faker import Faker

fake = Faker()
BASE_URL = "https://compassuol.serverest.dev"

def gerar_usuario_payload(admin="true"):
    return {
        "nome": fake.first_name(),
        "email": fake.unique.email(),
        "password": "senha",
        "administrador": admin
    }

def gerar_produto_payload():
    return {
        "nome": f"{fake.unique.company()} - Produto",
        "preco": fake.random_int(min=10, max=5000),
        "descricao": fake.sentence(),
        "quantidade": fake.random_int(min=1, max=100)
    }

class TestProdutosAPI:

    @pytest.fixture
    def token_admin(self):
        user = gerar_usuario_payload(admin="true")
        res_user = requests.post(f"{BASE_URL}/usuarios", json=user)
        user_id = res_user.json().get("_id")
        
        res_login = requests.post(f"{BASE_URL}/login", json={"email": user["email"], "password": user["password"]})
        token = res_login.json().get("authorization")
        
        yield token
        
        if user_id:
            requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    @pytest.fixture
    def token_comum(self):
        user = gerar_usuario_payload(admin="false")
        res_user = requests.post(f"{BASE_URL}/usuarios", json=user)
        user_id = res_user.json().get("_id")
        
        res_login = requests.post(f"{BASE_URL}/login", json={"email": user["email"], "password": user["password"]})
        token = res_login.json().get("authorization")
        
        yield token
        
        if user_id:
            requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    @pytest.fixture
    def produto_cadastrado(self, token_admin):
        payload = gerar_produto_payload()
        headers = {"Authorization": token_admin}
        
        res_prod = requests.post(f"{BASE_URL}/produtos", json=payload, headers=headers)
        prod_id = res_prod.json().get("_id")
        
        yield {"id": prod_id, "payload": payload, "token": token_admin}
        
        if prod_id:
            requests.delete(f"{BASE_URL}/produtos/{prod_id}", headers=headers)

    # 1. Listar produtos com sucesso
    def test_1_listar_produtos_com_sucesso(self):
        response = requests.get(f"{BASE_URL}/produtos")
        
        assert response.status_code == 200
        assert "produtos" in response.json()

    # 2. Cadastrar produto válido como Administrador
    def test_2_cadastrar_produto_como_admin_retorna_201(self, token_admin):
        payload = gerar_produto_payload()
        headers = {"Authorization": token_admin}
        
        response = requests.post(f"{BASE_URL}/produtos", json=payload, headers=headers)
        body = response.json()
        
        assert response.status_code == 201
        assert body["message"] == "Cadastro realizado com sucesso"
        
        requests.delete(f"{BASE_URL}/produtos/{body['_id']}", headers=headers)

    # 3. Erro ao cadastrar produto com usuário comum
    def test_3_cadastrar_produto_com_usuario_comum_retorna_403(self, token_comum):
        payload = gerar_produto_payload()
        headers = {"Authorization": token_comum}
        
        response = requests.post(f"{BASE_URL}/produtos", json=payload, headers=headers)
        
        assert response.status_code == 403
        assert response.json()["message"] == "Rota exclusiva para administradores"

    # 4. Erro ao cadastrar produto sem token de autenticação
    def test_4_cadastrar_produto_sem_token_retorna_401(self):
        payload = gerar_produto_payload()
        
        response = requests.post(f"{BASE_URL}/produtos", json=payload)
        
        assert response.status_code == 401
        assert response.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

    # 5. Buscar produto por ID válido
    def test_5_buscar_produto_por_id_valido(self, produto_cadastrado):
        prod_id = produto_cadastrado["id"]
        
        response = requests.get(f"{BASE_URL}/produtos/{prod_id}")
        
        assert response.status_code == 200
        assert response.json()["nome"] == produto_cadastrado["payload"]["nome"]

    # 6. Atualizar produto existente como Administrador
    def test_6_atualizar_produto_como_admin_retorna_200(self, produto_cadastrado):
        prod_id = produto_cadastrado["id"]
        headers = {"Authorization": produto_cadastrado["token"]}
        
        payload_atualizado = gerar_produto_payload()
        payload_atualizado["nome"] = produto_cadastrado["payload"]["nome"]
        
        response = requests.put(f"{BASE_URL}/produtos/{prod_id}", json=payload_atualizado, headers=headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Registro alterado com sucesso"

    # 7. Excluir produto existente como Administrador
     def test_7_excluir_produto_como_admin_retorna_200(self, token_admin):
        """
        Versão refatorada: usa a fixture token_admin e o padrão de teardown correto.
        """
        # 1. Criar um produto usando o token_admin da fixture
        payload = gerar_produto_payload()
        headers = {"Authorization": token_admin}
        
        res_criar = requests.post(
            f"{BASE_URL}/produtos", 
            json=payload, 
            headers=headers
        )
        prod_id = res_criar.json()["_id"]
        
        # 2. Excluir o produto criado
        response = requests.delete(
            f"{BASE_URL}/produtos/{prod_id}", 
            headers=headers
        )
        
        # 3. Asserts
        assert response.status_code == 200
        assert "excluído" in response.json()["message"].lower() or \
               "excluido" in response.json()["message"].lower()