# ⚡ Analisador de Reclamações de Clientes

**Sistema inteligente de análise de reclamações utilizando Python, FastAPI, NLTK e SQLite.**

Aplicação web desenvolvida para auxiliar equipes de **Qualidade, Atendimento ao Cliente (SAC) e Produto** na identificação dos principais pontos de atrito relatados pelos consumidores.

O sistema utiliza técnicas de Processamento de Linguagem Natural (NLP) para analisar reclamações em português, identificar as quatro palavras-chave mais relevantes de cada relato e armazenar os resultados em um banco de dados SQLite, permitindo consultas posteriores.

---

## 🎯 Funcionalidades

- **Processamento de Linguagem Natural (NLP):** utiliza a biblioteca NLTK para tokenização, normalização de textos, remoção de pontuações e eliminação de stopwords em português.
- **Extração das Top 4 palavras-chave:** identifica os quatro termos mais frequentes e calcula seu percentual de relevância em relação às palavras consideradas na análise.
- **Histórico persistente:** armazena automaticamente a data, o horário, o texto original da reclamação e as palavras-chave extraídas em um banco de dados SQLite.
- **Interface
