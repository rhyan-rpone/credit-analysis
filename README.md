# Credit Analysis Team

Projeto de analise de credito com uma arquitetura multiagente. A ideia central e simular uma equipe de especialistas trabalhando em conjunto para receber documentos, extrair informacoes, avaliar capacidade de pagamento, aplicar politicas de credito, consolidar riscos e gerar um parecer final auditavel.

## Visao Geral

O `credit-analysis` foi pensado como uma plataforma modular para analise de propostas de credito. O backend exposto por FastAPI deve funcionar como a porta de entrada para casos de analise, enquanto os modulos internos organizam agentes, regras, extracao documental, calculos financeiros, persistencia e geracao de relatorios.

Em termos praticos, o sistema deve apoiar um fluxo como:

1. Receber uma proposta de credito e seus documentos.
2. Processar documentos com extracao de texto, tabelas e dados financeiros.
3. Acionar agentes especializados para revisar partes diferentes do caso.
4. Cruzar informacoes extraidas com politicas internas de credito.
5. Produzir uma recomendacao final com justificativas, alertas e evidencias.
6. Registrar o resultado para auditoria, acompanhamento e melhoria continua.

## Objetivos do Projeto

- Automatizar etapas repetitivas da analise de credito.
- Reduzir perda de contexto entre documentos, indicadores financeiros e politicas.
- Permitir que agentes especializados trabalhem de forma coordenada.
- Gerar pareceres explicaveis, rastreaveis e consistentes.
- Separar bem as responsabilidades entre API, agentes, regras, banco, documentos e relatorios.

## Estado Atual

O repositorio esta em fase inicial de estrutura. Hoje ele contem:

- Uma API FastAPI inicial em `apps/api/app/main.py`.
- Um endpoint de healthcheck em `GET /health`.
- Arquivo `requirements.txt` com dependencias previstas para API, banco, jobs, OCR, relatorios, IA, testes e qualidade de codigo.
- Pastas preparadas para agentes, documentos, politicas, financeiro, relatorios, workers, frontend, infraestrutura, amostras e documentacao.
- `docker-compose.yml`, `apps/api/app/core/config.py` e `apps/api/app/db/session.py` ainda estao como esqueletos.

> Observacao: a aplicacao importa `get_settings` de `apps/api/app/core/config.py`. Como esse arquivo ainda esta vazio no estado atual, a configuracao precisa ser implementada antes de subir a API sem erro.

## Arquitetura Conceitual

```mermaid
flowchart TD
    A[Cliente ou Analista] --> B[API FastAPI]
    B --> C[Orquestrador Multiagente]
    C --> D[Agente de Documentos]
    C --> E[Agente Financeiro]
    C --> F[Agente de Politicas]
    C --> G[Agente de Risco]
    C --> H[Agente de Relatorio]
    D --> I[Extracoes e Evidencias]
    E --> J[Indicadores Financeiros]
    F --> K[Regras e Enquadramento]
    G --> L[Alertas e Recomendacao]
    H --> M[Parecer Final]
    B --> N[(Banco de Dados)]
    C --> O[(Fila e Cache)]
```

## Time de Agentes

A estrutura foi preparada para comportar agentes especializados. Uma divisao esperada e:

- `Agente Coordenador`: controla o fluxo da analise, define proximos passos e consolida as respostas dos demais agentes.
- `Agente de Documentos`: le documentos enviados, executa OCR quando necessario, extrai campos relevantes e aponta inconsistencias.
- `Agente Financeiro`: calcula indicadores como renda, faturamento, margem, endividamento, liquidez, alavancagem e capacidade de pagamento.
- `Agente de Politicas`: compara a proposta com regras internas, limites de credito, criterios de elegibilidade e restricoes.
- `Agente de Risco`: avalia sinais de alerta, divergencias, fragilidades e fatores mitigantes.
- `Agente de Relatorio`: transforma a analise em parecer final estruturado, com recomendacao, justificativas e evidencias.

## Stack Tecnica

- `Python`: linguagem principal do backend.
- `FastAPI`: API HTTP.
- `Pydantic` e `pydantic-settings`: validacao de dados e configuracoes.
- `SQLAlchemy` e `Alembic`: acesso a banco e migracoes.
- `PostgreSQL`: banco relacional previsto.
- `Redis` e `Celery`: cache, filas e processamento assincrono.
- `PyMuPDF`, `pdfplumber`, `pytesseract`, `Pillow`: leitura, OCR e extracao de documentos.
- `pandas` e `openpyxl`: manipulacao de dados tabulares e planilhas.
- `Jinja2` e `Markdown`: geracao de relatorios.
- `OpenAI`, `LangGraph` e `langchain-core`: IA e orquestracao multiagente.
- `pytest`, `ruff` e `mypy`: testes, lint e checagem estatica.

## Estrutura de Pastas

```text
credit-analysis/
+-- apps/
|   +-- api/
|   |   +-- app/
|   |   |   +-- agents/
|   |   |   +-- api/
|   |   |   +-- core/
|   |   |   |   +-- config.py
|   |   |   +-- db/
|   |   |   |   +-- session.py
|   |   |   +-- documents/
|   |   |   +-- finance/
|   |   |   +-- policies/
|   |   |   +-- reports/
|   |   |   +-- tests/
|   |   |   +-- workers/
|   |   |   +-- main.py
|   |   +-- scripts/
|   +-- web/
+-- docs/
+-- infra/
+-- samples/
|   +-- documents/
|   +-- expected-results/
+-- docker-compose.yml
+-- README.md
+-- requirements.txt
```

### Raiz do Projeto

- `README.md`: documentacao principal do projeto.
- `requirements.txt`: dependencias Python do backend e ferramentas de desenvolvimento.
- `docker-compose.yml`: reservado para subir dependencias locais, como banco, Redis e possivelmente servicos da aplicacao.
- `.gitignore`: regras para ignorar ambiente virtual, caches, artefatos de build, arquivos temporarios e saidas de ferramentas.

### `apps/api`

Contem o backend principal do sistema. A API deve concentrar endpoints HTTP, configuracao, acesso a banco, orquestracao dos agentes, processamento de documentos, calculos e relatorios.

- `app/main.py`: ponto de entrada da aplicacao FastAPI. Hoje define o titulo da API, versao e o endpoint `GET /health`.
- `app/core/`: configuracoes globais, carregamento de variaveis de ambiente, logging e constantes compartilhadas.
- `app/db/`: conexao com banco, sessoes SQLAlchemy, modelos e utilitarios de persistencia.
- `app/api/`: roteadores HTTP, schemas de entrada/saida e controllers da API.
- `app/agents/`: definicoes dos agentes, prompts, estados, ferramentas e grafo de orquestracao.
- `app/documents/`: upload, leitura, OCR, parsing de PDFs, planilhas e documentos financeiros.
- `app/finance/`: calculos financeiros, indicadores, normalizacao de demonstrativos e regras quantitativas.
- `app/policies/`: politicas de credito, criterios de elegibilidade, limites, alcadas e regras de decisao.
- `app/reports/`: geracao de pareceres, templates, markdown, HTML ou PDF.
- `app/workers/`: jobs assincronos para processamento pesado, como OCR, analises longas e geracao de relatorios.
- `app/tests/`: testes automatizados da API e dos modulos internos.
- `scripts/`: scripts operacionais ou auxiliares, como cargas de exemplo, manutencao ou rotinas locais.

### `apps/web`

Pasta reservada para uma interface web. Ela pode futuramente conter um frontend para cadastro de propostas, upload de documentos, acompanhamento de analises, revisao humana e exibicao dos pareceres.

### `docs`

Pasta para documentacao tecnica e funcional. Bons candidatos para esta pasta:

- Desenho da arquitetura.
- Contratos de API.
- Decisoes de arquitetura.
- Modelo de dados.
- Fluxo dos agentes.
- Politicas de credito usadas no sistema.
- Guias de operacao e deploy.

### `infra`

Pasta reservada para infraestrutura. Pode incluir arquivos de deploy, Docker, Terraform, Helm, pipelines, configuracoes de observabilidade e recursos de ambiente.

### `samples`

Contem exemplos usados para desenvolvimento, testes e validacao.

- `samples/documents/`: documentos de exemplo para testar OCR, parsing e extracao.
- `samples/expected-results/`: saidas esperadas para comparar os resultados da analise.

## Fluxo Esperado de Analise

```text
1. Criacao do caso
   A API recebe dados da proposta, cliente, solicitacao de credito e documentos.

2. Ingestao documental
   O modulo de documentos extrai texto, tabelas e campos relevantes.

3. Normalizacao
   Dados extraidos sao convertidos para estruturas padronizadas.

4. Analise multiagente
   O coordenador aciona agentes especializados para avaliar documentos, numeros, politicas e riscos.

5. Consolidacao
   As respostas dos agentes sao combinadas em uma visao unica do caso.

6. Decisao ou recomendacao
   O sistema produz parecer: aprovado, reprovado, aprovado com ressalvas ou pendente de informacoes.

7. Relatorio
   O parecer final e gerado com justificativas, indicadores, evidencias e proximos passos.
```

## Modelos de Dados Esperados

Embora os modelos ainda nao estejam implementados, o dominio deve evoluir em torno de entidades como:

- `CreditCase`: caso de analise de credito.
- `Applicant`: solicitante, empresa ou pessoa analisada.
- `Document`: documento enviado para analise.
- `DocumentExtraction`: informacoes extraidas de um documento.
- `FinancialSnapshot`: indicadores financeiros consolidados.
- `PolicyCheck`: resultado de uma regra ou politica aplicada.
- `AgentRun`: execucao de um agente em um caso.
- `CreditDecision`: decisao ou recomendacao final.
- `Report`: parecer estruturado gerado pelo sistema.

## Como Preparar o Ambiente

Requisitos recomendados:

- Python 3.11 ou superior.
- Ambiente virtual Python.
- Tesseract OCR instalado, quando o processamento de imagem/OCR for usado.
- PostgreSQL e Redis, quando os modulos de banco, fila e cache estiverem ativos.

Instalacao local:

```powershell
cd credit-analysis
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Variaveis de ambiente esperadas para a evolucao do projeto:

```env
APP_ENV=development
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/credit_analysis
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your_api_key_here
```

## Como Executar a API

Depois que `apps/api/app/core/config.py` estiver implementado com `get_settings`, a API pode ser executada com:

```powershell
uvicorn app.main:app --reload --app-dir apps/api
```

Healthcheck esperado:

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok",
  "env": "development"
}
```

## Qualidade e Testes

Com as dependencias instaladas, os comandos previstos sao:

```powershell
pytest apps/api/app/tests
ruff check apps/api
mypy apps/api
```

Os testes devem crescer junto com cada modulo. Para este projeto, vale priorizar:

- Testes de parsing documental.
- Testes de calculos financeiros.
- Testes de regras de politica de credito.
- Testes do orquestrador multiagente.
- Testes dos endpoints publicos da API.
- Testes de regressao usando `samples/documents` e `samples/expected-results`.

## Convencoes de Desenvolvimento

- Manter modulos pequenos e com responsabilidades claras.
- Separar regras deterministicas de chamadas de IA.
- Registrar evidencias usadas pelos agentes para facilitar auditoria.
- Evitar que agentes tomem decisoes sem dados estruturados de apoio.
- Criar testes para regras financeiras e politicas de credito antes de alterar criterios sensiveis.
- Documentar decisoes importantes em `docs/`.
- Usar `samples/` para preservar exemplos reproduziveis.

## Roadmap Sugerido

1. Implementar configuracao em `app/core/config.py`.
2. Implementar sessao de banco em `app/db/session.py`.
3. Definir modelos principais do dominio de credito.
4. Criar endpoints para cadastro de casos e upload de documentos.
5. Implementar pipeline de extracao documental.
6. Implementar calculos financeiros iniciais.
7. Definir politicas de credito em formato testavel.
8. Criar o grafo multiagente com LangGraph.
9. Gerar relatorio final com rastreabilidade das evidencias.
10. Adicionar docker compose para PostgreSQL, Redis e API.
11. Criar testes de ponta a ponta com documentos de exemplo.

## Licenca

Defina a licenca do projeto antes de distribuir ou publicar o codigo.
