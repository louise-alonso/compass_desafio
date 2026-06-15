# ServeRest API Tests — Desafio Compass

Testes automatizados em **Python + Pytest** para a API [ServeRest](https://compassuol.serverest.dev/).

![Testes](https://github.com/louise-alonso/compass_desafio/actions/workflows/test.yml/badge.svg)

---

## Estrutura

```
compass_desafio/
├── .github/
│   └── workflows/
│       └── test.yml              # GitHub Actions (Extra 2)
├── tests/
│   ├── test_usuarios.py          # CRUD /usuarios (10 testes)
│   ├── test_login.py             # Autenticação /login (4 testes)
│   ├── test_produtos.py          # CRUD /produtos (7 testes)
│   └── test_json_schema.py       # Validação de schema (Extra 1)
├── reports/
│   └── report.html               # Relatório gerado automaticamente
├── PLANO-DE-TESTES.md            # Planejamento da suíte
├── README.md                     # Este arquivo
├── requirements.txt              # Dependências
└── .gitignore                    # Arquivos ignorados
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
python -m venv .venv
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
pip install -r requirements.txt
```

### 5. Executar testes

```bash
# Todos os testes
pytest tests/ -v

# Com relatório HTML
pytest tests/ -v --html=reports/report.html --self-contained-html

# Módulo específico
pytest tests/test_usuarios.py -v
```

---

## Cenários testados (24 testes)

### /usuarios (10 testes)

| # | Método | Cenário | Status |
|---|--------|---------|--------|
| 1 | GET | Listar usuários | 200 |
| 2 | POST | Cadastro válido | 201 |
| 3 | POST | Email duplicado | 400 |
| 4 | POST | Sem campo "nome" | 400 |
| 5 | POST | Sem campo "email" | 400 |
| 6 | POST | Sem campo "password" | 400 |
| 7 | GET | Buscar por ID válido | 200 |
| 8 | GET | Buscar por ID inexistente | 400 |
| 9 | PUT | Atualizar usuário | 200 |
| 10 | DELETE | Excluir usuário | 200 |

### /login (4 testes)

| # | Método | Cenário | Status |
|---|--------|---------|--------|
| 1 | POST | Credenciais válidas | 200 |
| 2 | POST | Senha incorreta | 401 |
| 3 | POST | Email não cadastrado | 401 |
| 4 | POST | Campos ausentes | 400 |

### /produtos (7 testes)

| # | Método | Cenário | Status |
|---|--------|---------|--------|
| 1 | GET | Listar produtos | 200 |
| 2 | POST | Cadastrar como admin | 201 |
| 3 | POST | Cadastrar como usuário comum | 403 |
| 4 | POST | Cadastrar sem token | 401 |
| 5 | GET | Buscar por ID válido | 200 |
| 6 | PUT | Atualizar produto | 200 |
| 7 | DELETE | Excluir produto | 200 |

### JSON Schema (3 testes)

| # | Endpoint | Schema validado |
|---|----------|-----------------|
| 1 | GET /usuarios | Estrutura da listagem |
| 2 | POST /login | Resposta de autenticação |
| 3 | GET /produtos | Estrutura da listagem |

---

## Dependências

```txt
pytest==9.0.3
requests==2.34.2
faker==40.23.0
pytest-html==4.2.0
jsonschema==4.23.0
```

---

## Decisões técnicas

- **Dados dinâmicos** com `Faker` para evitar conflitos entre execuções
- **Limpeza automática** via fixtures com `yield` (teardown após cada teste)
- **Verificação dupla**: status code + conteúdo do JSON
- **Testes independentes**: cada teste cria e limpa seus próprios dados
- **JSON Schema**: valida estrutura das respostas em 3 endpoints (Extra 1)
- **CI/CD**: GitHub Actions executa os testes a cada push (Extra 2)

---

## Cobertura de Testes

- **Método:** Operator Coverage (Cobertura de Operações)
- **Cobertura total:** 68,75% (11/16 operações)
- **Cenários fora do escopo:** Endpoint `/carrinhos` e testes de performance

### O que ficou de fora

1. **Endpoint /carrinhos:** Prioridade para regras de negócio base (usuários, autenticação e catálogo de produtos)
2. **Combinações exaustivas:** Foco em cenários críticos para manter a suíte rápida e objetiva

---

## Bugs Reportados

| # | Título | Severidade |
|---|--------|-----------|
| 1 | DELETE em produto já excluído retorna 200 ao invés de 404 | Média |
| 2 | API aceita cadastro de produto com nome contendo apenas espaços | Alta |
| 3 | GET /usuarios/ com ID vazio retorna listagem completa | Baixa |

---

## GitHub Actions (Extra 2)

Os testes são executados automaticamente a cada push. O relatório HTML fica disponível como artefato para download.

[Ver histórico de execuções](https://github.com/louise-alonso/compass_desafio/actions)

---

## Links

- [ServeRest API](https://compassuol.serverest.dev/)
- [Documentação do Pytest](https://docs.pytest.org/)
- [Documentação do Requests](https://requests.readthedocs.io/)
- [Repositório no GitHub](https://github.com/louise-alonso/compass_desafio)
