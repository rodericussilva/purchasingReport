# 📦 Purchasing Report System

Sistema web de gestão e análise de compras, desenvolvido com **Flask** no backend e **HTML/CSS/JavaScript** no frontend. Oferece dashboards, relatórios e ferramentas de suporte à decisão para equipes de compras e vendas.

---

## 🚀 Funcionalidades

| Módulo | Descrição |
|---|---|
| **Painel Geral** | Dashboard com indicadores consolidados de compras |
| **Sugestões de Compra** | Lista produtos com sugestão de reposição baseada em histórico |
| **Risco de Ruptura** | Identifica itens com risco de falta de estoque em N dias |
| **Itens Próximos ao Vencimento** | Monitora produtos com validade próxima |
| **Produtos Parados** | Lista itens sem movimentação por período configurável |
| **Comissões** | Calcula comissões de vendedores por período (mês/ano), com suporte a múltiplos vendedores simultâneos e exportação em Excel |
| **Detalhe por Política** | Exibe detalhamento de vendas por política comercial por vendedor, com exportação em Excel |

---

## 🛠️ Tecnologias

**Backend**
- Python 3.x
- Flask + Flask-CORS
- pyodbc (SQL Server)
- ReportLab (geração de PDF)
- python-dotenv

**Frontend**
- HTML5 + Bootstrap 5
- JavaScript (ES6+)
- SheetJS / xlsx (exportação de planilhas Excel)
- Bootstrap Icons

---

## 📁 Estrutura do Projeto

```
project/
├── backend/
│   ├── app.py               # Entrypoint Flask, definição de rotas
│   ├── database.py          # Conexão com banco de dados
│   ├── models.py            # Queries e regras de negócio
│   ├── routes/
│   │   └── reports.py       # Rotas de geração de relatórios (PDF, Excel, CSV)
│   ├── utils/
│   │   └── reports_utils.py # Funções utilitárias de geração de arquivos
│   ├── static/              # Arquivos estáticos servidos pelo Flask
│   └── .env                 # Variáveis de ambiente (não versionado)
│
└── frontend/
    ├── index.html
    ├── commissions.html
    ├── political-detail.html
    ├── purchase-suggestions.html
    ├── rupture-risk.html
    ├── close-to-expiration.html
    ├── stopped-products.html
    └── assets/
        ├── css/
        ├── js/
        │   ├── config.js            # URL base da API
        │   ├── commissions.js       # Lógica de comissões + exportação Excel
        │   ├── political_detail.js  # Lógica de detalhe por política + exportação Excel
        │   ├── rupture.js
        │   ├── suggestions.js
        │   ├── closeToExpiration.js
        │   └── stoppedProducts.js
        └── vendor/
            └── bootstrap/
```

---

## ⚙️ Configuração e Instalação

### Pré-requisitos

- Python 3.10+
- SQL Server com driver ODBC instalado (`ODBC Driver for SQL Server`)
- Node.js (opcional, apenas se utilizar o build do frontend)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/purchasing-report.git
cd purchasing-report
```

### 2. Configure o ambiente Python

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie o arquivo `backend/.env` com base no exemplo abaixo:

```env
DB_SERVER=seu_servidor
DB_DATABASE=seu_banco
DB_UID=seu_usuario
DB_PWD=sua_senha

FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

### 4. Inicie o servidor

```bash
cd backend
python app.py
```

O servidor estará disponível em `http://127.0.0.1:5000`.

### 5. Acesse o frontend

Abra o navegador e acesse:

```
http://127.0.0.1:5000/frontend/index.html
```

---

## 📊 Exportação de Relatórios Excel

As páginas **Comissões** e **Detalhe por Política** possuem botão de exportação direta para `.xlsx`, gerado no navegador via [SheetJS](https://sheetjs.com/). Cada vendedor selecionado é exportado em uma aba separada, com o conteúdo exatamente como exibido na tela.

- O arquivo é nomeado automaticamente com o mês e ano selecionados
- Suporta exportação de um ou múltiplos vendedores simultaneamente
- Não requer interação com o servidor para gerar o Excel

---

## 🔌 Principais Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/suppliers` | Lista fornecedores |
| GET | `/api/sellers` | Lista vendedores |
| GET | `/api/products` | Produtos por fornecedor |
| GET | `/api/rupture-risk` | Risco de ruptura por fornecedor e prazo |
| GET | `/api/items-close-expiration` | Itens próximos ao vencimento |
| GET | `/api/stagnant-items` | Itens parados por fornecedor |
| GET | `/api/commissions` | Comissões por vendedor e período |
| GET | `/api/political-detail` | Detalhe por política comercial |
| GET | `/api/sellers/periods` | Períodos disponíveis por vendedor |
| POST | `/api/generate_report` | Gera relatório PDF/Excel/CSV |

---

## 🗃️ Banco de Dados

O sistema conecta-se a um banco **SQL Server** via `pyodbc`. As configurações de conexão são lidas do arquivo `.env` e nunca expostas no código-fonte.

---

## 📝 Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `DB_SERVER` | Endereço do servidor SQL Server |
| `DB_DATABASE` | Nome do banco de dados |
| `DB_UID` | Usuário do banco |
| `DB_PWD` | Senha do banco |
| `FLASK_HOST` | Host do servidor Flask (padrão: `127.0.0.1`) |
| `FLASK_PORT` | Porta do servidor Flask (padrão: `5000`) |

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Commit suas alterações (`git commit -m 'feat: adiciona minha feature'`)
4. Push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
