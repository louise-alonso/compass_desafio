# Plano de Testes - API ServeRest

## Objetivo
Garantir a confiabilidade das operações de CRUD e dos mecanismos de autenticação da API ServeRest, validando regras de negócio e prevenindo falhas sistêmicas.

## Estratégia
- **Camada:** Backend (API REST).
- **Ferramentas:** Python 3, Pytest, Requests e Faker.
- **Tipo de Teste:** Testes Funcionais de API.

## Escopo
- **Entra:** Endpoints `/usuarios`, `/login` e `/produtos`.
- **Fica de fora:** Endpoint `/carrinhos`, testes de interface (UI) e testes de performance.

## Cenários a Implementar

### `/usuarios` (Concluído)
| # | Método | Cenário | Status Esperado |
|---|--------|---------|-----------------|
| 1 | GET | Listar usuários com sucesso | 200 |
| 2 | POST | Cadastrar usuário com sucesso | 201 |
| 3 | POST | Erro ao cadastrar com email duplicado | 400 |
| 4 | POST | Erro ao cadastrar sem o campo "nome" | 400 |
| 5 | POST | Erro ao cadastrar sem o campo "email" | 400 |
| 6 | POST | Erro ao cadastrar sem o campo "password" | 400 |
| 7 | GET | Buscar usuário por ID válido | 200 |
| 8 | GET | Erro ao buscar usuário com ID inexistente | 400 |
| 9 | PUT | Atualizar usuário existente com sucesso | 200 |
| 10 | DELETE | Excluir usuário existente com sucesso | 200 |

### `/login` (Pendente)
| # | Método | Cenário | Status Esperado |
|---|--------|---------|-----------------|
| 8 | POST | Login com credenciais válidas | 200 |
| 9 | POST | Erro de login com senha inválida | 401 |
| 10 | POST | Erro de login com email não cadastrado | 401 |
| 11 | POST | Erro de login com campos ausentes | 400 |

### `/produtos` (Pendente)
| # | Método | Cenário | Status Esperado |
|---|--------|---------|-----------------|
| 12 | GET | Listar produtos com sucesso | 200 |
| 13 | POST | Cadastrar produto usando token de Administrador | 201 |
| 14 | POST | Erro ao cadastrar usando token de usuário comum | 403 |
| 15 | POST | Erro ao cadastrar sem enviar token | 401 |
| 16 | GET | Buscar produto por ID válido | 200 |
| 17 | PUT | Atualizar produto como Administrador | 200 |
| 18 | DELETE | Excluir produto como Administrador | 200 |

## Critérios de Qualidade (Definition of Done)
Um teste só é considerado finalizado se cumprir:
1. **Independência:** Roda sozinho e não depende do resultado de nenhum outro teste.
2. **Teardown Seguro:** Limpa a própria bagunça, apagando do banco tudo o que criou ao final do teste (via `yield`).
3. **Assertividade Dupla:** Valida o Status Code e se o JSON voltou com os campos e estruturas certas.
4. **Massa Dinâmica:** Usa `Faker` para gerar dados novos a cada rodada, evitando conflitos de e-mails duplicados.
