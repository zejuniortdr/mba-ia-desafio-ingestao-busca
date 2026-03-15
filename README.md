# Desafio MBA Engenharia de Software com IA - Full Cycle

> **Trabalho de MBA em Engenharia de Software com IA**
> Sistema de busca semântica e chat conversacional sobre documentos PDF, implementado com arquitetura RAG (Retrieval-Augmented Generation) usando LangChain, pgVector (PostgreSQL) e suporte a múltiplos provedores de LLM (OpenAI / Google Gemini).

---

## Visão Geral da Arquitetura

O sistema implementa o padrão **RAG (Retrieval-Augmented Generation)**, que combina busca semântica vetorial com geração de linguagem natural:

```mermaid
flowchart TB
    subgraph INGESTAO["Pipeline de Ingestão"]
        direction LR
        PDF["📄 PDF"]
        CHUNK["✂️ Chunking"]
        EMBED1["🔢 Embeddings"]
        STORE[("🗄️ pgVector\nArmazenamento")]

        PDF --> CHUNK --> EMBED1 --> STORE
    end

    subgraph CONSULTA["Pipeline de Consulta"]
        direction LR
        USER["🙋 Pergunta do  Usuário"]
        EMBED2["🔢 Embedding"]
        SEARCH["🔍 Busca por\nSimilaridade"]
        CTX["📋 Contexto"]
        LLM["🤖 LLM"]
        RESP["💡 Resposta"]

        USER --> EMBED2 --> SEARCH --> CTX --> LLM --> RESP
    end

    STORE -->|"vetores relevantes"| SEARCH
```

| Componente       | Tecnologia                        | Responsabilidade                        |
|------------------|-----------------------------------|-----------------------------------------|
| Ingestão         | LangChain + PyPDFLoader           | Leitura, chunking e vetorização do PDF  |
| Vetorial Store   | pgVector (PostgreSQL)             | Armazenamento e busca por similaridade  |
| Embeddings       | OpenAI `text-embedding-ada-002`   | Geração de vetores semânticos           |
| LLM              | OpenAI GPT / Google Gemini        | Geração de respostas contextualizadas   |
| Orquestração     | LangChain                         | Pipeline RAG end-to-end                 |

---

## Pré-requisitos

Antes de iniciar, certifique-se de que os itens abaixo estão instalados e configurados:

| Ferramenta     | Versão mínima | Verificação                  |
|----------------|---------------|------------------------------|
| Python         | 3.14+         | `python3 --version`          |
| Docker         | 24+           | `docker --version`           |
| Docker Compose | 2.x           | `docker compose version`     |
| Git            | qualquer      | `git --version`              |
| Make           | qualquer      | `make --version`             |

Você também precisará de **ao menos uma** das seguintes API Keys:
- **OpenAI API Key** — [platform.openai.com](https://platform.openai.com)
- **Google Gemini API Key** — [aistudio.google.com](https://aistudio.google.com)

---

## Passo a Passo — Setup Completo

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### 2. Configurar as variáveis de ambiente

```bash
# Copiar o arquivo de exemplo
cp .env.example .env
```

Abra o arquivo `.env` e preencha **todas** as variáveis obrigatórias:

```bash
# Editor de sua preferência
nano .env
# ou
code .env
```

> ⚠️ **Atenção:** Os comandos `ingest` e `chat` verificam automaticamente se o `.env`
> está corretamente preenchido antes de executar. Nenhuma variável pode estar vazia.

### 3. Adicionar o documento PDF

```bash
# Copie seu PDF para a raiz do projeto com o nome esperado
cp /caminho/para/seu/arquivo.pdf ./document.pdf
```

> O arquivo deve se chamar `document.pdf` e estar na raiz do projeto.

### 4. Criar o ambiente virtual e instalar dependências

```bash
# Ambiente de produção
make setup

# — ou — ambiente de desenvolvimento (inclui ferramentas de lint e testes)
make setup/dev
```

Isso irá:
- Criar o `venv/` com Python 3
- Atualizar o `pip`
- Instalar todas as dependências do `requirements.txt` (ou `requirements-dev.txt`)

### 5. Subir o banco de dados (pgVector)

```bash
make up
```

Isso iniciará o container PostgreSQL com a extensão `pgvector` habilitada via Docker Compose em modo detached (background).

Verifique se está rodando:

```bash
docker compose ps
```

> Aguarde o status `healthy` antes de prosseguir.

### 6. Executar a ingestão do PDF

```bash
make ingest
```

Este comando irá:
1. Verificar se todas as variáveis do `.env` estão preenchidas
2. Carregar e fazer o chunking do `document.pdf`
3. Gerar embeddings via API (OpenAI ou Gemini)
4. Persistir os vetores no pgVector

> A ingestão precisa ser executada **apenas uma vez** por documento.
> Para trocar o documento, remova os dados do banco e ingeste novamente.

### 7. Iniciar o chat

```bash
make chat
```

Este comando irá:
1. Verificar se todas as variáveis do `.env` estão preenchidas
2. Iniciar a interface de chat no terminal
3. Aguardar suas perguntas sobre o conteúdo do PDF

Para encerrar o chat, pressione `Ctrl+C` ou `Ctrl+D`.

---

## Configuração do `.env`

Descrição de cada variável disponível no `.env.example`:

| Variável           | Obrigatória | Descrição                                              |
|--------------------|-------------|--------------------------------------------------------|
| `LLM_PROVIDER`     | ✅ Sim       | Provedor do LLM: `openai` ou `gemini`                  |
| `OPENAI_API_KEY`   | Condicional | Obrigatória se `LLM_PROVIDER=openai`                   |
| `GOOGLE_API_KEY`   | Condicional | Obrigatória se `LLM_PROVIDER=gemini`                   |
| `DATABASE_URL`     | ✅ Sim       | URL de conexão com o PostgreSQL (ex: `postgresql://...`)|

### Usando Google Gemini (padrão)

```dotenv
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIza...
DATABASE_URL=postgresql://user:password@localhost:5432/ragdb

### Usando OpenAI

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@localhost:5432/ragdb
```
```

---

## Testes

```bash
# Apenas testes unitários
make test

# Apenas testes de integração (requer banco de dados rodando)
make test-integration

# Toda a suite de testes
make test-all
```

> Para testes de integração, certifique-se de executar `make up` antes.

---

## 🗂️ Estrutura do Projeto

```
.
├── docker-compose.yml        # Configuração do PostgreSQL + pgVector
├── requirements.txt          # Dependências de produção
├── requirements-dev.txt      # Dependências de desenvolvimento (lint, testes)
├── pyproject.toml            # Configuração do projeto e ferramentas (ruff)
├── Makefile                  # Automação de tarefas
├── .env.example              # Template das variáveis de ambiente
├── .env                      # Variáveis de ambiente (NÃO commitar)
├── document.pdf              # PDF para ingestão (NÃO commitar)
├── src/
│   ├── config.py             # Settings via pydantic-settings e factories de LLM
│   ├── ingest.py             # Pipeline de ingestão: load → chunk → embed → store
│   ├── search.py             # Busca semântica direta (sem geração)
│   └── chat.py               # Interface CLI do chat RAG
└── tests/
    ├── unit/                 # Testes unitários (sem dependências externas)
    └── integration/          # Testes de integração (requerem DB e API)
```

---

## 💬 Exemplo de Uso

```
$ make chat

✅ Todas as variáveis estão preenchidas!
🚀 Iniciando chat... (Ctrl+C para sair)

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Qual é a capital da França?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

> O sistema responde **apenas** com base no conteúdo do PDF ingerido,
> evitando alucinações ao declarar explicitamente quando não há contexto suficiente.

---

## Ferramentas de Desenvolvimento

O projeto utiliza o **ruff** para linting e formatação de código:

```bash
# Verificar estilo e erros
venv/bin/ruff check src/

# Formatar código automaticamente
venv/bin/ruff format src/
```

Configurações definidas no `pyproject.toml`: linha de 88 caracteres, aspas duplas, regras E, W, F, I, C, B habilitadas.

---

## Checklist de Entrega — MBA

Antes de submeter o trabalho, verifique:

- [x] Arquivo `.env.example` presente e com todas as variáveis documentadas
- [x] Arquivo `.env` **não** versionado (presente no `.gitignore`)
- [x] Arquivo `document.pdf` **não** versionado (presente no `.gitignore`)
- [x] `make setup` executado com sucesso em ambiente limpo
- [x] `make up` inicia o banco sem erros
- [x] `make ingest` conclui sem erros
- [x] `make chat` responde perguntas corretamente
- [x] `make test-all` passa sem falhas
- [x] README revisado e coerente com o projeto entregue

---

## Licença

Este projeto foi desenvolvido como trabalho acadêmico para o MBA em Engenharia de Software com IA.
