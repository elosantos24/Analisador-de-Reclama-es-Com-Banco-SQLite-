⚡ Analisador de Reclamações de Clientes (FastAPI + NLTK + SQLite)
Aplicação web corporativa desenvolvida para equipes de Qualidade, Atendimento (SAC) e Produto identificarem rapidamente os principais pontos de atrito relatados por clientes. O sistema processa textos de reclamações em linguagem natural, extrai os 4 termos mais relevantes de cada análise e mantém um histórico persistente em banco de dados.
🎯 Funcionalidades Principais
Processamento de Linguagem Natural (NLP): Utiliza a biblioteca NLTK para tokenização, limpeza de pontuações e remoção automática de stopwords em português (artigos, preposições e conectivos irrelevantes).
Extração de Top 4 Termos: Calcula a frequência e o percentual de relevância das palavras-chave, destacando as 4 principais palavras de cada relato.
Persistência em Banco de Dados (SQLite): Armazena automaticamente a data/hora, o texto original da reclamação e as 4 palavras extraídas no arquivo historico_reclamacoes.db.
Interface Corporativa Interativa: Painel responsivo desenvolvido com Bootstrap 5 e Fetch API, permitindo análises instantâneas sem recarregamento de página e visualização em tempo real do histórico salvo.
Documentação Automática de API: Endpoints documentados nativamente via Swagger UI (/docs).
🛠️ Stack Tecnológica
Backend: Python 3, FastAPI, Uvicorn
Processamento de Texto: NLTK (Natural Language Toolkit)
Banco de Dados: SQLite3 (nativo)
Frontend: HTML5, Bootstrap 5, JavaScript (Vanilla / Fetch API)
Deploy em Nuvem: Render
📁 Estrutura do Projeto
Analisador-de-Reclama-es-Com-Banco-SQLite-/
├── main.py                     # Aplicação FastAPI, lógica NLTK, SQLite e interface integrada
├── requirements.txt            # Dependências do projeto para instalação local e nuvem
├── .gitignore                  # Arquivos ignorados pelo controle de versão (cache, banco local, venv)
├── README.md                   # Documentação do projeto
└── historico_reclamacoes.db    # Banco de dados SQLite (gerado automaticamente na primeira execução)


🚀 Como Executar Localmente
Pré-requisitos
Python 3.9 ou superior instalado.
Passo a Passo
Clone o repositório:
git clone https://github.com/SEU_USUARIO/Analisador-de-Reclama-es-Com-Banco-SQLite-.git
cd Analisador-de-Reclama-es-Com-Banco-SQLite-


(Opcional) Crie e ative um ambiente virtual:
python -m venv venv
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux/Mac:
source venv/bin/activate


Instale as dependências:
pip install -r requirements.txt


Inicie o servidor:
python main.py


(Na primeira execução, o sistema baixará automaticamente o pacote de stopwords em português do NLTK e criará o banco de dados SQLite).
Acesse a aplicação no navegador:
Painel Principal: http://127.0.0.1:8000
Documentação da API (Swagger): http://127.0.0.1:8000/docs
☁️ Deploy em Produção (Render)
Este projeto está configurado para implantação contínua no Render:
Crie um novo Web Service no painel do Render conectado ao seu repositório do GitHub.
Utilize as seguintes configurações:
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Clique em Create Web Service.
Nota sobre Banco de Dados em Nuvem: No plano gratuito (Free Tier) do Render, o sistema de arquivos é efêmero (reiniciado a cada novo deploy ou inatividade). Para persistência permanente em produção de grande escala, recomenda-se anexar um Persistent Disk no Render ou migrar a conexão sqlite3 para PostgreSQL.
🔌 Endpoints da API
Método
Rota
Descrição
GET
/
Renderiza a interface web principal do analisador.
POST
/api/analisar
Recebe {"texto": "..."}, extrai as Top 4 palavras, grava no SQLite e retorna o ranking em JSON.
GET
/api/historico
Retorna as últimas 20 análises registradas no banco de dados SQLite.
