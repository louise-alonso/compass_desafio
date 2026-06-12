import requests
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
        requests.delete(f"{BASE_URL}/usuarios/{body["_id"]}")

    def test_05_cadastrar_usuario_com_email_duplicado_deve_falhar(self):
        payload1 = gerar_usuario_payload()
        response1 = requests.post(f"{BASE_URL}/usuarios", json=payload1)
        assert response1.status_code == 201
        email_existente = payload1["email"]
        user_id = response1.json()["_id"]
        payload2 = gerar_usuario_payload(email=email_existente)
        response2 = requests.post(f"{BASE_URL}/usuarios", json=payload2)
        assert response2.status_code == 400
        requests.delete(f"{BASE_URL}/usuarios/{user_id}")

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

    def test_09_buscar_usuario_por_id_valido_deve_retornar_dados_corretos(self):
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        response = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["_id"] == user_id
        assert body["nome"] == payload["nome"]
        assert body["email"] == payload["email"]
        requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    def test_10_buscar_usuario_com_id_inexistente_deve_retornar_400(self):
        response = requests.get(f"{BASE_URL}/usuarios/9999999999999999")
        assert response.status_code == 400

    def test_11_atualizar_usuario_existente_deve_retornar_200(self):
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        novo_email = gerar_email_unico()
        payload_atualizado = {
            "nome": "Nome Atualizado via PUT",
            "email": novo_email,
            "password": "novaSenha@123",
            "administrador": "false"
        }
        response = requests.put(f"{BASE_URL}/usuarios/{user_id}", json=payload_atualizado)
        assert response.status_code == 200
        assert response.json()["message"] == "Registro alterado com sucesso"
        requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    def test_12_atualizar_apenas_um_campo_deve_ser_rejeitado(self):
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        response = requests.put(f"{BASE_URL}/usuarios/{user_id}", json={"nome": "Apenas Nome Mudou"})
        assert response.status_code == 400
        requests.delete(f"{BASE_URL}/usuarios/{user_id}")

    def test_13_excluir_usuario_existente_deve_retornar_200(self):
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        response = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        assert response.status_code == 200
        assert "excluído" in response.json()["message"] or "excluido" in response.json()["message"]
        verificar = requests.get(f"{BASE_URL}/usuarios/{user_id}")
        assert verificar.status_code == 400

    def test_14_excluir_usuario_ja_excluido_deve_ser_idempotente(self):
        payload = gerar_usuario_payload()
        criacao = requests.post(f"{BASE_URL}/usuarios", json=payload)
        user_id = criacao.json()["_id"]
        response1 = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        assert response1.status_code == 200
        response2 = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
        assert response2.status_code == 200
        assert "Nenhum" in response2.json()["message"]

    def test_15_excluir_usuario_com_id_inexistente_deve_retornar_200(self):
        response = requests.delete(f"{BASE_URL}/usuarios/8888888888888888")
        assert response.status_code == 200
        assert "Nenhum" in response.json()["message"]
