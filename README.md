
# ServeRest API Tests — Desafio Compass

Testes automatizados em **Python + Pytest** para o endpoint `/usuarios` da API [ServeRest](https://compassuol.serverest.dev/).

---

## Estrutura

```
compass_desafio/
├── tests/
│   └── test_usuarios.py   # Todos os testes
├── requirements.txt       # Dependências
├── README.md              # Este arquivo
└── .gitignore             # Arquivos ignorados
```

---

## Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/louise-alonso/compass_desafio.git
cd compass_desafio
```

### 2. Criar ambiente virtual

```bash
py -m venv .venv
```

### 3. Ativar ambiente virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependências

```bash
py -m pip install -r requirements.txt
```

### 5. Executar testes

```bash
# Todos os testes
py -m pytest tests/test_usuarios.py -v

# Com relatório HTML
py -m pytest tests/test_usuarios.py -v --html=reports/report.html

# Apenas testes específicos
py -m pytest tests/test_usuarios.py -v -k "cadastrar"
```

---

## Cenários testados (10 testes)

| # | Método | Endpoint | Cenário |
| --- | --- | --- | --- |
| 1 | GET | `/usuarios` | Listar usuários com sucesso (Status 200 + estrutura) |
| 2 | POST | `/usuarios` | Cadastro válido → 201 |
| 3 | POST | `/usuarios` | Email duplicado → 400 |
| 4 | POST | `/usuarios` | Sem campo "nome" → 400 |
| 5 | POST | `/usuarios` | Sem campo "email" → 400 |
| 6 | POST | `/usuarios` | Sem campo "password" → 400 |
| 7 | GET | `/usuarios/{id}` | Buscar por ID válido → 200 + validação de dados |
| 8 | GET | `/usuarios/{id}` | Buscar por ID inexistente → 400 |
| 9 | PUT | `/usuarios/{id}` | Atualizar usuário existente → 200 |
| 10 | DELETE | `/usuarios/{id}` | Excluir usuário existente → 200 |

---

## Dependências

```txt
pytest==9.0.3
requests==2.34.2
faker==40.23.0
pytest-html==4.2.0
```

---

## Decisões técnicas

- **Emails dinâmicos** com `Faker` para evitar conflitos
- **Limpeza automática** após cada teste (`requests.delete`)
- **Verificação dupla**: status code + conteúdo da resposta
- **Testes independentes** (cada um cria e limpa seus dados)
- **Asserts flexíveis** para lidar com acentos da API

---

## Links

- [ServeRest API](https://compassuol.serverest.dev/)
- [Pytest Docs](https://docs.pytest.org/)
- [Requests Docs](https://requests.readthedocs.io/)
- [Repositório no GitHub](https://github.com/louise-alonso/compass_desafio)
