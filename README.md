# Desafio Semana 3

Testes automatizados em **Python + Pytest** para o endpoint `/usuarios` da API [ServeRest](https://compassuol.serverest.dev/).

---

## 📁 Estrutura

```
compass_desafio/
├── tests/test_usuarios.py   # Todos os testes
├── requirements.txt         # Dependências
└── README.md                # Este arquivo
```

---

## 🚀 Como rodar

```bash
1. Clonar o repositório
Abra o terminal onde deseja salvar o projeto e execute:

Bash
git clone [https://github.com/louise-alonso/compass_desafio.git](https://github.com/louise-alonso/compass_desafio.git)
2. Acessar a pasta do projeto

Bash
cd compass_desafio
3. Criar o ambiente virtual

Bash
py -m venv .venv
4. Ativar o ambiente virtual (Windows)

Bash
.venv\Scripts\activate
5. Instalar as dependências

Bash
py -m pip install -r requirements.txt
6. Executar os testes

Bash
py -m pytest tests/test_usuarios.py -v
```

---

## 📋 Cenários testados (15 testes)

| # | Método | Endpoint | Cenário |
|---|--------|----------|----------|
| 1 | GET | `/usuarios` | Listar usuários → 200 |
| 2 | GET | `/usuarios` | Validar estrutura (quantidade + usuarios) |
| 3 | GET | `/usuarios` | Quantidade = tamanho da lista |
| 4 | POST | `/usuarios` | Cadastro válido → 201 |
| 5 | POST | `/usuarios` | Email duplicado → 400 |
| 6 | POST | `/usuarios` | Sem campo "nome" → 400 |
| 7 | POST | `/usuarios` | Sem campo "email" → 400 |
| 8 | POST | `/usuarios` | Sem campo "password" → 400 |
| 9 | GET | `/usuarios/{id}` | ID válido → 200 + dados corretos |
| 10 | GET | `/usuarios/{id}` | ID inexistente → 400 |
| 11 | PUT | `/usuarios/{id}` | Atualizar usuário existente → 200 |
| 12 | PUT | `/usuarios/{id}` | Atualização parcial → 400 |
| 13 | DELETE | `/usuarios/{id}` | Excluir usuário existente → 200 |
| 14 | DELETE | `/usuarios/{id}` | Excluir mesmo usuário duas vezes → idempotente |
| 15 | DELETE | `/usuarios/{id}` | ID inexistente → 200 + "Nenhum registro excluído" |

---

## 📦 Dependências

```txt
pytest==9.0.3
requests==2.34.2
faker==40.23.0
pytest-html==4.2.0
```

---

## 🧠 Decisões técnicas

- **Emails dinâmicos** com `Faker` para evitar conflitos
- **Limpeza automática** após cada teste (`requests.delete`)
- **Verificação dupla**: status code + conteúdo da resposta
- **Testes independentes** (cada um cria e limpa seus dados)
- **Asserts flexíveis** para lidar com acentos da API

---

## 🔗 Links

- [ServeRest API](https://compassuol.serverest.dev/)
- [Pytest Docs](https://docs.pytest.org/)
- [Requests Docs](https://requests.readthedocs.io/)

---
