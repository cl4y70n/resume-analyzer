# Resume Analyzer (MVP) - Full skeleton with Celery and simple API-Key auth

Analisador de Currículos para RH — versão MVP leve (5–10 currículos), com:
- FastAPI (API)
- Hugging Face NER (default: Portuguese-capable model)
- spaCy (hooks for rules)
- OCR (Tesseract)
- Celery + Redis (background jobs for OCR / heavy processing)
- Autenticação simples via API-KEY (header `x-api-key`)
- Docker + docker-compose for local testing

## Quick start (local, usando docker-compose)
1. Copie `.env.example` para `.env` e ajuste `API_KEY`.
2. `docker compose up --build`
3. App disponível em `http://localhost:8000`

## Estrutura
- `app/` - backend
- `models/` - modelos opcionais
- `tests/samples/` - exemplos de currículos (anônimos)
- `docker-compose.yml` - orquestra serviços (web, worker, redis)

## Nota
O modelo default no `NerWrapper` é sugerido para português. Você pode trocar para outro modelo do Hugging Face facilmente.
