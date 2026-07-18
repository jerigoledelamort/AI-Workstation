# Changelog

Все заметные изменения AI Workstation документированы здесь.
Формат: [Keep a Changelog](https://keepachangelog.com/).

---

## [0.5.0] — 2026-07-18

### Router Proxy — автороутинг моделей
- FastAPI-прокси на порту `4001` между Cline и LiteLLM
- Модель `auto`: анализ сложности задачи (ключевые слова, контекст, code blocks)
- Пресеты: `preset-light`, `preset-medium`, `preset-heavy`
- Логирование в `logs/router.log`
- Streaming и non-streaming режимы
- Passthrough для остальных endpoint'ов

### GhidraMCP — реверс-инжиниринг
- GhidraMCP 1.4 установлен (плагин + Python bridge)
- Отдельный venv `.venv-mcp/` (Python 3.12, MCP SDK)
- Bridge на `127.0.0.1:8081` (SSE transport)
- Cline MCP config настроен: `cline_mcp_settings.json`
- Инструменты: decompile, rename, comment, xrefs, strings, disassemble
- Launcher: `scripts/setup/start-ghidra-mcp.bat`

### Obsidian — память проектов
- Генератор vault: `scripts/obsidian/create_vault.py`
- Авто-setup: `scripts/setup_helper.py` (определение типа проекта)
- Структура: architecture, decisions, research, rules, progress, issues, notes
- `.clinerules` — глобальные правила для Cline
- Шаблоны для заметок и ADR

### Документация
- Полная переработка всех документов
- Удалены устаревшие дубликаты в `docs/`
- README, Architecture, Troubleshooting, DisasterRecovery переписаны с нуля

---

## [0.4.0] — 2026-07-18

### Cline — автономный агент VS Code
- Расширение `saoudrizwan.claude-dev` установлено
- Настроен на Router Proxy (`http://127.0.0.1:4001/v1`)
- Plan/Act режимы: `preset-heavy` / `preset-medium`
- MCP config: `cline_mcp_settings.json`
- Capabilities: file R/W, terminal, browser, MCP

---

## [0.3.0] — 2026-07-18

### Aider — CLI coding agent
- Aider 0.86.2 установлен в `.venv` (`uv pip install aider-chat`)
- Подключение к LiteLLM Proxy
- Модель по умолчанию: `coder-low` (qwen2.5-coder:7b)
- `.aider.conf.yml` + `.aider.model.settings.yml`
- Wrapper: `scripts/setup/aider.bat`
- `OPENAI_API_KEY` — постоянная User env var
- Протестировано: SEARCH/REPLACE blocks работают

---

## [0.2.1] — 2026-07-18

### Автозапуск
- Task Scheduler задача `AI-Workstation-AutoStart`
- Trigger: AtLogOn
- `start-all.ps1` с `-ExecutionPolicy Bypass -WindowStyle Hidden`
- Логирование в `logs/autostart.log`
- `SOPS_AGE_KEY_FILE` — постоянная User env var
- Open WebUI через `.bat` wrapper (надёжная передача env vars)

---

## [0.2.0] — 2026-07-18

### Open WebUI
- Open WebUI 0.10.2 в отдельном venv (Python 3.12.13)
- `scripts/setup/start-webui.bat` — launcher с SOPS decrypt
- Подключение к Ollama (direct) + LiteLLM (OpenAI API)
- Порт 8080, localhost only
- `start-all.ps1` / `stop-all.ps1` / `health-check.ps1` обновлены
- `.gitignore`: `.venv-webui/` добавлен

---

## [0.1.0] — 2026-07-18

### Phase 1: Структура проекта
- Директории: `config/`, `scripts/`, `docs/`, `data/`, `tests/`
- `.gitignore`, `.gitattributes`
- `README.md`

### Phase 2: Базовая инфраструктура
- Python 3.10.10 venv через uv 0.11.29
- `pyproject.toml` с зависимостями
- MkDocs Material 9.7.7

### Phase 3: AI Inference
- Ollama 0.32.0, `OLLAMA_HOST=127.0.0.1:11434`
- 11 моделей (~97 ГБ): Low / Medium / High профили
- LiteLLM Proxy 1.92.0 на порту 4000
- `config/litellm/config.yaml` — роутинг через алиасы
- SOPS 3.13.2 + age 1.3.1 для `.secrets.yaml`

### Phase 4: Среда разработки
- Continue v2.0.0 (VS Code extension)
- `~/.continue/config.json` — 6 моделей + autocomplete + embeddings
- `.vscode/settings.json`, `.devcontainer/`

### Phase 5: Безопасность
- `tests/test-security.ps1` — 10/10 PASS
- 6 Windows Firewall inbound block правил
- SOPS + age шифрование секретов

### Phase 6: RAG и агенты
- Qdrant 1.18.3 (нативный бинарник)
- LangChain 1.3.14 + langchain-ollama + langchain-qdrant
- LangGraph 1.2.9
- `scripts/rag/rag_pipeline.py` — ingest + query
- `scripts/rag/agent_workflow.py` — tool calling (ReAct)

### Phase 7: Автоматизация
- 7 скриптов: start/stop-all, health-check, vram, update/cleanup models, backup

### Phase 8: Документация
- MkDocs Material, 7 страниц

### Phase 9: Тесты
- `tests/test-inference.ps1` — 6/6 PASS
- `tests/test-security.ps1` — 10/10 PASS

### Pre-Installation Safety
- Restore Point (ID 79)
- Бэкап пользовательских конфигов
- Лог установки: `logs/install.log`
