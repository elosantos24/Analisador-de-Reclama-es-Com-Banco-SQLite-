# ⚡ Analisador de Reclamações de Clientes (FastAPI + NLTK + SQLite)

Aplicação web corporativa desenvolvida para equipes de **Qualidade, Atendimento (SAC) e Produto** identificarem rapidamente os principais pontos de atrito relatados por clientes. O sistema processa textos de reclamações em linguagem natural, extrai os **4 termos mais relevantes** de cada análise e mantém um histórico persistente em banco de dados.

## 🎯 Funcionalidades Principais

- **Processamento de Linguagem Natural (NLP):** Utiliza a biblioteca **NLTK** para tokenização, limpeza de pontuações e remoção automática de *stopwords* em português (artigos, preposições e conectivos irrelevantes).
- **Extração de Top 4 Termos:** Calcula a frequência e o percentual de relevância das palavras-chave, destacando as **4 principais palavras** de cada relato.
- **Persistência em Banco de Dados (SQLite):** Armazena automaticamente a data/hora, o texto original da reclamação e as 4 palavras extraídas no arquivo `historico_reclamacoes.db`.
- **Interface Corporativa Interativa:** Painel responsivo desenvolvido com **Bootstrap 5** e **Fetch API**, permitindo análises instantâneas sem recarregamento de página e visualização em tempo real do histórico salvo.
- **Documentação Automática de API:** Endpoints documentados nativamente via Swagger UI (`/docs`).

## 🛠️ Stack Tecnológica

- **Backend:** Python 3, FastAPI, Uvicorn
- **Processamento de Texto:** NLTK (*Natural Language Toolkit*)
- **Banco de Dados:** SQLite3 (nativo)
- **Frontend:** HTML5, Bootstrap 5, JavaScript (Vanilla / Fetch API)
- **Deploy em Nuvem:** Render

## 📁 Estrutura do Projeto

```text
Analisador-de-Reclama-es-Com-Banco-SQLite-/
│
├── main.py                  # Aplicação FastAPI, lógica NLTK, SQLite e interface integrada
├── requirements.txt         # Dependências do projeto para instalação local e nuvem
├── .gitignore               # Arquivos ignorados pelo controle de versão (cache, banco local, venv)
├── README.md                # Documentação do projeto
└── historico_reclamacoes.db # Banco
