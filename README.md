🤖 FLOW — Agente de Inteligência Artificial

O **FLOW** é um agente virtual oficial da **Flowcore_IA**, desenvolvido em Python e integrado à API do Google Gemini utilizando o SDK mais recente (`google-genai`). O agente opera via terminal com uma persona customizada, profissional, direta e suporte a histórico de conversas (memória de sessão).

---

## 🚀 Funcionalidades

- **Persona Customizada**: Atendimento alinhado à identidade da Flowcore_IA.
- **Memória de Sessão**: Mantém o contexto da conversa ativo durante a execução.
- **Interface Colorida**: Feedback visual dinâmico no terminal utilizando a biblioteca `colorama`.
- **SDK Atualizado**: Construído sobre o modelo **Gemini 2.5 Flash** usando a nova estrutura do Google GenAI.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Google GenAI SDK** (Integração com Gemini 2.5 Flash)
- **Python Dotenv** (Gerenciamento seguro de variáveis de ambiente)
- **Colorama** (Estilização de cores no terminal)

---

## 📦 Pré-requisitos & Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com
cd NOME_DO_REPOSITORIO
```

### 2. Configurar o Ambiente Virtual (venv)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração da API Key

O projeto utiliza variáveis de ambiente para proteger suas credenciais. 
1. Crie um arquivo chamado **`.env`** na raiz do projeto.
2. Adicione sua chave da API do Gemini seguindo o modelo abaixo:

```env
GEMINI_API_KEY=seu_token_aqui_da_api_gemini
```

> **Nota:** Certifique-se de que o arquivo `.env` está listado no seu `.gitignore` para evitar enviar sua chave privada para o GitHub.

---

## 🖥️ Como Executar

Com o ambiente virtual ativado e a chave configurada no `.env`, execute o script principal do agente:

```bash
python agente_flowcore.py
```

---

## 📞 Contato

Desenvolvido por **Flowcore_IA**.
- **Instagram:** [@Flowcore_IA]
