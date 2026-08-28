# Agente de IA para Instagram

API REST desenvolvida em Python e Flask para atendimento automatizado de leads provenientes do Instagram, utilizando Google Gemini como modelo de linguagem e Make.com como camada de automação e orquestração.

O projeto foi desenvolvido inicialmente como MVP e posteriormente evoluído para uma arquitetura mais segura, testável e organizada, adequada para demonstração técnica, portfólio e evolução para uso real.

---

## Visão geral

Empresas que recebem contatos pelas redes sociais podem perder oportunidades quando não conseguem responder rapidamente, manter o contexto das conversas ou qualificar leads de forma consistente.

Este projeto implementa um agente virtual capaz de:

- receber mensagens por API REST;
- identificar cada conversa por `user_id`;
- manter memória isolada entre usuários;
- gerar respostas utilizando Google Gemini;
- conduzir conversas de qualificação;
- integrar-se a fluxos externos utilizando Make.com;
- proteger a API por chave de acesso;
- limitar abuso por rate limiting;
- tratar falhas do provedor de IA sem expor informações internas.

---

## Arquitetura

```text
Instagram
    ↓
Make.com
    ↓
Flask REST API
    ↓
Routes
    ↓
Agent Service
    ├── Prompt
    ├── Session Store
    └── Google Gemini
    ↓
Resposta
```

### Fluxo de uma mensagem

```text
1. Lead envia mensagem no Instagram

2. Make.com recebe o evento

3. Make.com envia:
   user_id + mensagem
   para POST /flow

4. Flask:
   - valida autenticação
   - valida payload
   - aplica rate limit

5. Agent Service:
   - recupera o histórico daquele usuário
   - envia contexto + mensagem ao Gemini
   - recebe a resposta
   - atualiza o histórico

6. A resposta retorna ao fluxo de automação
```

---

## Tecnologias

- Python
- Flask
- Google Gemini
- Google Gen AI SDK
- REST API
- Make.com
- Prompt Engineering
- Pytest
- Flask-Limiter
- Ruff
- Gunicorn
- Docker
- GitHub Actions

> Redis ainda não faz parte da implementação atual. Está previsto no roadmap para substituir a memória local em cenários de produção distribuída.

---

## Estrutura do projeto

```text
Agente_IA_Instagram/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   └── session_store.py
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── flow_prompt.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── flow.py
│   │
│   └── services/
│       ├── __init__.py
│       └── agent_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_agente_flowcore.py
│   └── test_flow_api.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── agente_flowcore.py
├── api_flow.py
├── run.py
└── README.md
```

---

## Memória conversacional

Cada conversa é identificada por um `user_id`.

Exemplo:

```json
{
  "user_id": "instagram_123456",
  "mensagem": "Quero automatizar meu atendimento"
}
```

O histórico é armazenado separadamente:

```text
instagram_123456
└── histórico A

instagram_987654
└── histórico B
```

Isso evita compartilhamento acidental de contexto entre leads.

O histórico também possui limite de mensagens para impedir crescimento indefinido.

### Limitação atual

A implementação utiliza memória local do processo Python.

Portanto:

- o histórico é perdido quando a aplicação reinicia;
- múltiplos processos não compartilham memória;
- múltiplos containers não compartilham memória.

Para produção distribuída, a evolução prevista é utilizar Redis com TTL.

---

## Segurança

A aplicação possui:

- autenticação via `X-API-Key`;
- chave obrigatória por variável de ambiente;
- ausência de segredo padrão no código;
- validação do `Content-Type`;
- validação rigorosa do JSON;
- validação de tipos;
- limite de tamanho para `user_id`;
- limite de tamanho das mensagens;
- rate limiting;
- tratamento seguro de exceções;
- proteção contra exposição de detalhes internos;
- `.env` excluído do Git;
- `.env` excluído da imagem Docker.

Credenciais reais nunca devem ser adicionadas ao repositório.

---

## Configuração

Crie o arquivo `.env` a partir do exemplo:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux/macOS

```bash
cp .env.example .env
```

Depois configure:

```env
API_KEY=sua_chave_privada

GEMINI_API_KEY=sua_chave_do_google_ai_studio

GEMINI_MODEL=gemini-2.5-flash
GEMINI_TIMEOUT_MS=60000
GEMINI_TEMPERATURE=0.75
GEMINI_MAX_OUTPUT_TOKENS=600

PORT=5000
```

A `API_KEY` pode ser gerada com Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Instalação local

Recomenda-se utilizar ambiente virtual.

### Criar ambiente

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

### Instalar dependências

Para executar a aplicação:

```bash
python -m pip install -r requirements.txt
```

Para desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

---

## Executar localmente

```bash
python run.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

---

## Endpoints

### `GET /health`

Verifica se a aplicação está disponível.

Exemplo:

```bash
curl http://127.0.0.1:5000/health
```

Resposta:

```json
{
  "status": "FLOW online"
}
```

---

### `POST /flow`

Processa uma mensagem do usuário.

Header obrigatório:

```text
X-API-Key: SUA_API_KEY
```

Payload:

```json
{
  "user_id": "instagram_123456",
  "mensagem": "Quero automatizar meu atendimento"
}
```

Resposta:

```json
{
  "resposta": "Resposta gerada pelo agente"
}
```

---

## Exemplo com curl

```bash
curl -X POST http://127.0.0.1:5000/flow \
  -H "Content-Type: application/json" \
  -H "X-API-Key: SUA_API_KEY" \
  -d '{
    "user_id": "instagram_123456",
    "mensagem": "Quero automatizar meu atendimento"
  }'
```

---

## Integração com Make.com

O Make.com pode atuar como camada intermediária entre Instagram e a API.

Fluxo conceitual:

```text
Instagram
    ↓
Trigger / automação
    ↓
Make.com
    ↓
HTTP POST
    ↓
/flow
```

A requisição enviada pelo Make.com deve conter:

### Header

```text
X-API-Key: SUA_API_KEY
```

### JSON

```json
{
  "user_id": "identificador_estavel_do_lead",
  "mensagem": "mensagem_recebida"
}
```

O `user_id` deve permanecer estável durante toda a conversa.

Não deve ser criado um identificador novo para cada mensagem.

---

## Testes

O projeto utiliza Pytest.

Execute:

```bash
python -m pytest -q
```

A suíte cobre atualmente, entre outros cenários:

- health check;
- ausência de API Key;
- API Key incorreta;
- JSON ausente;
- JSON malformado;
- `user_id` ausente;
- tipo inválido de `user_id`;
- limite de tamanho do `user_id`;
- mensagem vazia;
- tipo inválido de mensagem;
- limite de tamanho da mensagem;
- request válido;
- isolamento de histórico entre usuários;
- falha simulada do Gemini;
- fallback seguro;
- rate limiting.

As chamadas ao Gemini são mockadas durante os testes.

Isso evita:

- consumo de API;
- dependência de internet;
- resultados não determinísticos.

---

## Qualidade de código

O projeto utiliza Ruff para análise estática e organização dos imports.

Execute:

```bash
python -m ruff check .
```

Resultado esperado:

```text
All checks passed!
```

---

## Docker

O projeto possui um `Dockerfile` preparado para execução com Gunicorn.

Build:

```bash
docker build -t agente-ia-instagram .
```

Execução:

```bash
docker run \
  -p 5000:5000 \
  -e API_KEY="sua_api_key" \
  -e GEMINI_API_KEY="sua_gemini_api_key" \
  agente-ia-instagram
```

A configuração atual utiliza um único worker do Gunicorn porque a memória conversacional ainda é mantida no processo local.

Após migração para Redis, a aplicação poderá utilizar múltiplos workers ou containers mantendo contexto compartilhado.

---

## CI/CD

O projeto possui GitHub Actions.

A cada `push` ou `pull request` para a branch principal, o CI executa:

```text
Checkout
   ↓
Python 3.12
   ↓
Instalação das dependências
   ↓
Ruff
   ↓
Pytest
   ↓
Docker Build
   ↓
Container
   ↓
Smoke Test /health
```

Nenhuma chave real do Gemini é utilizada durante o CI.

---

## Tratamento de falhas da IA

A chamada ao Gemini possui timeout configurável.

Caso o provedor apresente falha, timeout ou indisponibilidade, informações internas não são enviadas ao usuário.

O agente retorna um fallback seguro:

```text
Não consegui processar sua mensagem agora.
Tente novamente em alguns instantes.
```

Mensagens que não obtêm uma resposta válida também são removidas do histórico para evitar contaminar a conversa.

---

## Transparência

O agente é apresentado como assistente virtual da empresa.

Ele não precisa repetir constantemente que utiliza inteligência artificial, mas deve responder com transparência caso o usuário pergunte diretamente.

---

## Limitações atuais

A versão atual ainda possui algumas limitações importantes:

- memória armazenada somente em RAM;
- perda de histórico após reinicialização;
- execução com apenas um worker para preservar a memória;
- ausência de armazenamento persistente de leads;
- ausência de painel administrativo;
- integração com Instagram depende da camada externa de automação;
- rate limiting utiliza armazenamento local;
- não há observabilidade centralizada.

Esses pontos são tratados como limitações conhecidas, e não como funcionalidades já implementadas.

---

## Roadmap

Evoluções previstas:

- Redis para memória conversacional;
- TTL por conversa;
- Redis como backend do rate limiting;
- múltiplos workers;
- observabilidade estruturada;
- métricas de atendimento;
- persistência de leads qualificados;
- testes adicionais de integração;
- deploy em ambiente cloud;
- versionamento da API;
- aprimoramento contínuo do prompt.

---

## Objetivo do projeto

Este projeto demonstra conhecimentos aplicados em:

- desenvolvimento backend com Python;
- APIs REST;
- integração com LLMs;
- automação de processos;
- engenharia de prompt;
- segurança de APIs;
- gerenciamento de contexto conversacional;
- testes automatizados;
- arquitetura modular;
- Docker;
- integração contínua.

### Classificação

**Automação & Inteligência Artificial**