# Changelog

Все заметные изменения AI Workstation документированы здесь.
Формат основан на [Keep a Changelog](https://keepachangelog.com/).

## [0.3.0] — 2026-07-18

### Aider — AI Coding Agent
- Aider 0.86.2 installed in `.venv` (via `uv pip install aider-chat`)
- Connected to LiteLLM Proxy (OpenAI-compatible API)
- Default model: `coder-low` (qwen2.5-coder:7b) for speed
- `.aider.conf.yml` — config (model, api-base, edit-format=diff)
- `.aider.model.settings.yml` — custom model parameters
- `scripts/setup/aider.bat` — wrapper script
- `OPENAI_API_KEY` set as permanent User env var
- `.gitignore` — Aider history files excluded
- Tested: file editing, SEARCH/REPLACE blocks working

## [0.2.1] — 2026-07-18

### Autostart
- Windows Task Scheduler task AI-Workstation-AutoStart created
- Trigger: At logon (user: egork)
- Runs start-all.ps1 with -ExecutionPolicy Bypass -WindowStyle Hidden
- All 4 services (Ollama + Qdrant + LiteLLM + Open WebUI) start automatically

## [0.2.0] — 2026-07-18

### Open WebUI
- Open WebUI 0.10.2 installed in separate venv (Python 3.12.13)
- scripts/setup/start-webui.ps1 — PowerShell launch script with SOPS decrypt
- Connected to Ollama (direct) + LiteLLM Proxy (OpenAI API)
- Port 8080, localhost only
- start-all.ps1 / stop-all.ps1 / health-check.ps1 updated
- .gitignore: .venv-webui/ added

## [0.2.1] — 2026-07-18

### Autostart
- Windows Task Scheduler task `AI-Workstation-AutoStart` created
- Trigger: At logon (user: egork)
- Runs `start-all.ps1` with `-ExecutionPolicy Bypass -WindowStyle Hidden`
- All 4 services (Ollama + Qdrant + LiteLLM + Open WebUI) start automatically

## [0.2.0] — 2026-07-18

### Open WebUI
- Open WebUI 0.10.2 installed in separate venv (Python 3.12.13)
- `scripts/setup/start-webui.ps1` — PowerShell launch script with SOPS decrypt
- Connected to Ollama (direct) + LiteLLM Proxy (OpenAI API)
- Port 8080, localhost only
- `start-all.ps1` / `stop-all.ps1` / `health-check.ps1` updated
- `.gitignore`: `.venv-webui/` added

## [0.1.0] — 2026-07-18

### Phase 1: Project Structure
- Созданы директории: `config/`, `scripts/`, `docs/`, `data/`, `tests/`
- `.gitkeep` файлы для сохранения структуры
- `README.md` с описанием проекта
- `.gitignore` и `.gitattributes`

### Phase 2: Base Infrastructure
- Python 3.10.10 venv через uv 0.11.29
- `pyproject.toml` с зависимостями
- MkDocs Material 9.7.7
- `mkdocs.yml` с темой Material, переключением dark/light
- `docs/index.md` — главная страница

### Phase 3: AI Inference Layer
- Ollama 0.32.0 установлен, `OLLAMA_HOST=127.0.0.1:11434`
- 11 моделей загружены (~97 ГБ):
  - Low: qwen3:8b, qwen2.5-coder:7b, qwen2.5vl:3b, nomic-embed-text
  - Medium: qwen2.5:14b, deepseek-coder-v2:lite, qwen2.5vl:7b, bge-m3
  - High: qwen2.5:32b, qwen3-coder:30b, qwen2.5vl:32b
- LiteLLM Proxy 1.92.0 на порту 4000
- `config/litellm/config.yaml` — роутинг 11 моделей через алиасы
- SOPS 3.13.2 + age 1.3.1 для шифрования `.secrets.yaml`
- `scripts/setup/start-litellm.bat` с `PYTHONUTF8=1` для Unicode

### Phase 4: Dev Environment
- Continue v2.0.0 (VS Code extension)
- `~/.continue/config.json` — 6 моделей + autocomplete + embeddings
- `.vscode/settings.json` — Python interpreter, UTF-8, исключения
- `.devcontainer/devcontainer.json` — Docker dev config

### Phase 5: Security
- `tests/test-security.ps1` — 10 проверок (все PASS):
  1. Ollama bind to localhost
  2. 6 firewall inbound block rules
  3. LiteLLM rejects unauthenticated requests
  4. Secrets encrypted (SOPS)
  5. age keypair exists
  6-8. .gitignore: .secrets.yaml, *.key, .env
  9. LiteLLM proxy healthy
  10. Ollama healthy
- 6 Windows Firewall правил:
  - Block-Ollama-Inbound (11434)
  - Block-LiteLLM-Inbound (4000)
  - Block-Qdrant-REST-Inbound (6333)
  - Block-Qdrant-gRPC-Inbound (6334)
  - Block-OpenWebUI-Inbound (8080)
  - Block-MkDocs-Inbound (8000)

### Phase 6: RAG & Agents
- Qdrant 1.18.3 (нативный бинарник, без Docker)
- `config/qdrant/qdrant.yaml` — localhost binding
- `scripts/setup/start-qdrant.bat`
- LangChain 1.3.14 + langchain-ollama 1.1.0 + langchain-qdrant 1.1.0
- LangGraph 1.2.9
- `scripts/rag/rag_pipeline.py` — ingest + query (тест: 4 чанка, ответ корректный)
- `scripts/rag/agent_workflow.py` — tool calling (тест: 25*4=100)

### Phase 7: Automation
- 7 скриптов:
  - `scripts/setup/start-all.ps1` — запуск Ollama + Qdrant + LiteLLM
  - `scripts/setup/stop-all.ps1` — остановка всех
  - `scripts/monitoring/health-check.ps1` — проверка 3 сервисов
  - `scripts/monitoring/vram-check.ps1` — nvidia-smi + RAM
  - `scripts/maintenance/update-models.ps1` — ollama pull
  - `scripts/maintenance/cleanup-models.ps1` — список моделей
  - `scripts/backup/backup.ps1` — резервное копирование

### Phase 8: Documentation
- 7 страниц MkDocs: requirements, architecture, roadmap, ai-models, tdr, security, runbook
- `mkdocs build --strict` — PASS

### Phase 9: Tests & Audit
- `tests/test-inference.ps1` — 6/6 PASS (4 chat + 2 embed)
- `tests/test-security.ps1` — 10/10 PASS

### Pre-Installation Safety
- Restore Point (ID 79) создан
- Бэкап пользовательских конфигов в `D:\Projects\ai\backup\`
- Лог установки: `D:\Projects\ai\logs\install.log`