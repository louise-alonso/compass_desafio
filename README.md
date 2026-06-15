
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

## Cobertura de Testes

- **Método:** Operator Coverage (Cobertura de Operações)
- **Cobertura total:** 68,75% (11/16 operações)
- **Cenários fora do escopo:** Endpoint `/carrinhos` e testes de performance
- **Bugs encontrados:** 2 bugs reportados (ver Issues #1, #2 e #3)

### O que ficou de fora e por quê?

Como já foi definido e delimitado no arquivo **PLANO-DE-TESTES.md**, deixei alguns cenários fora do escopo desta etapa:

1. **Endpoint de Carrinhos (`/carrinhos`):** Priorizei as regras de negócio base da aplicação (gestão de usuários, login e o catálogo de produtos com trava de admin). O fluxo transacional de carrinhos ficou para uma próxima iteração.
2. **Combinações exaustivas de parâmetros (Parameter Value Coverage):** Validei os cenários críticos e a ausência de campos obrigatórios. Não testei todas as combinações possíveis de dados inválidos ou limites de caracteres para manter a suíte rodando rápido e focada no que é essencial no momento.

---

## JSON Schema (Extra 1)

Validação da estrutura das respostas da API usando JSON Schema.

### Schemas implementados

| Endpoint | Schema | O que valida |
|----------|--------|--------------|
| `GET /usuarios` | `SCHEMA_LISTAR_USUARIOS` | Estrutura da listagem: `quantidade` (int) + array `usuarios` com campos obrigatórios |
| `POST /login` | `SCHEMA_LOGIN_SUCESSO` | Resposta de login: `message` (string) + `authorization` (string ≥ 10 caracteres) |
| `GET /produtos` | `SCHEMA_LISTAR_PRODUTOS` | Estrutura da listagem: `quantidade` (int) + array `produtos` com campos obrigatórios |

### Tecnologia
- Biblioteca: `jsonschema`
- Validação: `validate(instance=resposta, schema=SCHEMA)`
- Tratamento de erros: `pytest.fail()` com mensagem descritiva

---

## Links

- [ServeRest API](https://compassuol.serverest.dev/)
- [Pytest Docs](https://docs.pytest.org/)
- [Requests Docs](https://requests.readthedocs.io/)
- [Repositório no GitHub](https://github.com/louise-alonso/compass_desafio)
