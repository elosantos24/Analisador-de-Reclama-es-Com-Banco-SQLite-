import os
import re
import sqlite3
from datetime import datetime
from collections import Counter
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import nltk
from nltk.corpus import stopwords

app = FastAPI(title="Analisador de Reclamações com Banco de Dados | FastAPI")

# Configuração e inicialização do Banco de Dados SQLite
DB_FILE = "historico_reclamacoes.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buscas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            texto_original TEXT,
            top_palavras TEXT
        )
    """)
    conn.commit()
    conn.close()

# Inicializa o banco ao iniciar a aplicação
init_db()

# Configuração do NLTK
nltk_data_dir = os.path.join(os.path.dirname(__file__), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

try:
    stopwords.words("portuguese")
except LookupError:
    try:
        nltk.download("stopwords", download_dir=nltk_data_dir, quiet=True)
    except Exception as e:
        print(f"Aviso NLTK: {e}")


def processar_texto(texto: str, top_n: int = 4):
    """Processa o texto, limpa stopwords e retorna as palavras mais frequentes."""
    try:
        palavras = re.findall(r"\b[a-záàâãéèêíïóôõöúçñ]+\b", texto.lower())
        
        try:
            stop_words = set(stopwords.words("portuguese"))
        except:
            stop_words = set()
            
        stop_words.update(["pra", "pro", "tá", "né", "pois", "assim", "sobre", "ainda", "muito", "bem"])
        
        palavras_filtradas = [
            p for p in palavras 
            if p not in stop_words and len(p) > 2
        ]
        
        total_validas = len(palavras_filtradas)
        contagem = Counter(palavras_filtradas).most_common(top_n)
        
        resultados = []
        for palavra, frequencia in contagem:
            percentual = round((frequencia / total_validas) * 100, 1) if total_validas > 0 else 0
            resultados.append({
                "palavra": palavra,
                "frequencia": frequencia,
                "percentual": percentual
            })
            
        return resultados, total_validas
    except Exception as e:
        print(f"Erro no processamento: {e}")
        return [], 0


def salvar_busca_db(texto: str, resultados: list):
    """Salva no SQLite o texto e as 4 palavras mais relevantes da busca."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Pega apenas as palavras do resultado para armazenar em formato de texto/csv
        palavras_str = ", ".join([item["palavra"] for item in resultados])
        
        cursor.execute(
            "INSERT INTO buscas (data_hora, texto_original, top_palavras) VALUES (?, ?, ?)",
            (data_hora, texto, palavras_str)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")


# Interface HTML corporativa integrada com visualização do histórico do banco
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Reclamações com Banco de Dados | FastAPI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar-brand { font-weight: 600; letter-spacing: 0.5px; }
        .card { border: none; border-radius: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); }
        .progress { height: 10px; border-radius: 5px; }
    </style>
</head>
<body>

<nav class="navbar navbar-dark bg-dark mb-4">
    <div class="container">
        <span class="navbar-brand mb-0 h1">⚡ Analisador de Reclamações (Com Banco SQLite)</span>
        <span class="text-light small">Portal Corporativo • Qualidade & Produto</span>
    </div>
</nav>

<div class="container">
    <div class="row g-4">
        <!-- Coluna de Entrada -->
        <div class="col-lg-6">
            <div class="card p-4 h-100">
                <h5 class="card-title mb-3 text-dark">Inserir Relatos de Clientes</h5>
                <p class="text-muted small">
                    O sistema extrairá automaticamente as <strong>4 palavras com maior relevância</strong> e as salvará no banco de dados.
                </p>
                
                <form id="formReclamacao">
                    <div class="mb-3">
                        <label for="texto_reclamacao" class="form-label fw-semibold">Texto das Reclamações</label>
                        <textarea 
                            class="form-control" 
                            id="texto_reclamacao" 
                            rows="9" 
                            placeholder="Ex: O aplicativo trava toda vez que tento finalizar o pagamento..."
                            required></textarea>
                    </div>

                    <button type="submit" id="btnProcessar" class="btn btn-success w-100 fw-semibold">
                        Processar e Salvar no Banco
                    </button>
                </form>
            </div>
        </div>

        <!-- Coluna de Resultados da Busca Atual -->
        <div class="col-lg-6">
            <div class="card p-4 h-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="card-title mb-0 text-dark">Top 4 Palavras Mais Relevantes</h5>
                    <span id="badgeTotal" class="badge bg-secondary d-none">0 relevantes</span>
                </div>

                <div id="containerResultados">
                    <div class="text-center text-muted my-auto py-5">
                        <p class="mb-1 fs-5">Nenhum dado processado ainda.</p>
                        <small>Insira o texto ao lado e clique em processar.</small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Histórico Salvo no Banco de Dados -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card p-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="card-title mb-0 text-dark">📂 Histórico de Buscas Salvas no Banco de Dados</h5>
                    <button class="btn btn-sm btn-outline-secondary" onclick="carregarHistorico()">Atualizar Histórico</button>
                </div>
                <div class="table-responsive">
                    <table class="table table-striped table-hover align-middle mb-0">
                        <thead class="table-dark">
                            <tr>
                                <th style="width: 15%;">Data / Hora</th>
                                <th style="width: 50%;">Trecho do Texto Analisado</th>
                                <th style="width: 35%;">Top 4 Palavras Salvas</th>
                            </tr>
                        </thead>
                        <tbody id="tabelaHistorico">
                            <tr>
                                <td colspan="3" class="text-center text-muted py-3">Carregando histórico...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    async function carregarHistorico() {
        try {
            const response = await fetch('/api/historico');
            const data = await response.json();
            const tbody = document.getElementById('tabelaHistorico');
            
            if (data.historico.length > 0) {
                let html = '';
                data.historico.forEach(item => {
                    html += `
                        <tr>
                            <td><small class="text-muted">${item.data_hora}</small></td>
                            <td><div class="text-truncate" style="max-width: 450px;" title="${item.texto}">${item.texto}</div></td>
                            <td><span class="badge bg-primary text-wrap">${item.top_palavras}</span></td>
                        </tr>
                    `;
                });
                tbody.innerHTML = html;
            } else {
                tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted py-3">Nenhum registro encontrado no banco de dados.</td></tr>`;
            }
        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
        }
    }

    document.getElementById('formReclamacao').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const texto = document.getElementById('texto_reclamacao').value;
        const btn = document.getElementById('btnProcessar');
        const container = document.getElementById('containerResultados');
        const badge = document.getElementById('badgeTotal');

        btn.disabled = true;
        btn.textContent = 'Processando e Gravando...';

        try {
            // Solicita top_n fixo em 4 conforme regra de negócio solicitada
            const response = await fetch('/api/analisar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texto, top_n: 4 })
            });

            if (!response.ok) throw new Error('Erro no servidor');

            const data = await response.json();
            
            if (data.resultados.length > 0) {
                badge.textContent = `${data.total_validas} palavras relevantes`;
                badge.classList.remove('d-none');

                let html = `
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>#</th>
                                    <th>Termo Relevante</th>
                                    <th class="text-center">Ocorrências</th>
                                    <th>Relevância</th>
                                </tr>
                            </thead>
                            <tbody>
                `;

                data.resultados.forEach((item, index) => {
                    html += `
                        <tr>
                            <td class="text-muted fw-bold">${index + 1}</td>
                            <td class="fw-semibold text-capitalize">${item.palavra}</td>
                            <td class="text-center"><span class="badge bg-success rounded-pill">${item.frequencia}</span></td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="progress flex-grow-1 me-2">
                                        <div class="progress-bar bg-success" role="progressbar" style="width: ${item.percentual}%;"></div>
                                    </div>
                                    <small class="text-muted">${item.percentual}%</small>
                                </div>
                            </td>
                        </tr>
                    `;
                });

                html += `</tbody></table></div>`;
                container.innerHTML = html;
                
                // Atualiza a tabela do histórico automaticamente após salvar
                carregarHistorico();
            } else {
                badge.classList.add('d-none');
                container.innerHTML = `<div class="text-center text-muted my-auto py-5"><p>Nenhuma palavra relevante encontrada.</p></div>`;
            }
        } catch (error) {
            alert('Ocorreu um erro ao processar a requisição.');
        } finally {
            btn.disabled = false;
            btn.textContent = 'Processar e Salvar no Banco';
        }
    });

    // Carrega o histórico ao abrir a página
    carregarHistorico();
</script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=HTML_TEMPLATE)


@app.post("/api/analisar")
async def analisar_api(data: dict):
    """Processa o texto, extrai as 4 palavras principais, salva no banco e retorna JSON."""
    try:
        texto = data.get("texto", "").strip()
        top_n = 4  # Fixado em 4 conforme solicitado

        if not texto:
            return JSONResponse({"resultados": [], "total_validas": 0})

        resultados, total_validas = processar_texto(texto, top_n)
        
        if resultados:
            salvar_busca_db(texto, resultados)

        return JSONResponse({
            "resultados": resultados,
            "total_validas": total_validas
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/historico")
async def obter_historico():
    """Retorna todas as buscas armazenadas no banco de dados SQLite."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT data_hora, texto_original, top_palavras FROM buscas ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()

        historico = []
        for row in rows:
            historico.append({
                "data_hora": row[0],
                "texto": row[1],
                "top_palavras": row[2]
            })

        return JSONResponse({"historico": historico})
    except Exception as e:
        return JSONResponse({"historico": []})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)