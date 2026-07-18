# Архитектура

## Обзор системы

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AI Workstation                                 │
│                                                                         │
│   ┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌────────────┐  │
│   │   VS Code   │────▶│  Router  │────▶│ LiteLLM  │────▶│   Ollama   │  │
│   │             │     │  Proxy   │     │  Proxy   │     │            │  │
│   │  • Cline    │     │  :4001   │     │  :4000   │     │   :11434   │  │
│   │  • Aider    │     │  (auto)  │     │  (auth)  │     │  11 models │  │
│   │  • Continue │     └──────────┘     └──────────┘     └────────────┘  │
│   └──────┬──────┘                                                        │
│          │                                                               │
│          │ MCP (SSE)                                                     │
│          ▼                                                               │
│   ┌─────────────┐     ┌──────────────────┐                               │
│   │   Ghidra    │◀───▶│  GhidraMCP Bridge│  Реверс-инжиниринг          │
│   │   :8080     │     │  :8081           │                               │
│   └─────────────┘     └──────────────────┘                               │
│                                                                         │
│   ┌─────────────┐     ┌──────────────────┐                               │
│   │  RAG        │────▶│     Qdrant       │  Векторная БД                │
│   │  Pipeline   │     │  :6333 / :6334   │                               │
│   └─────────────┘     └──────────────────┘                               │
│                                                                         │
│   ┌─────────────┐                                                       │
│   │ Open WebUI  │  Web-чат (браузер)                                   │
│   │   :8080     │                                                       │
│   └─────────────┘                                                       │
│                                                                         │
│   ┌───────────────────────────────────────────────────────────────────┐ │
│   │  SOPS 3.13.2  +  age 1.3.1  →  .secrets.yaml (encrypted)         │ │
│   └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│   ┌───────────────────────────────────────────────────────────────────┐ │
│   │  Task Scheduler: AI-Workstation-AutoStart (AtLogon)               │ │
│   └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

Все сервисы на `127.0.0.1`. Внешние подключения заблокированы firewall.

---

## Компоненты

### Inference: Ollama 0.32.0

| Параметр | Значение |
|----------|----------|
| Binary | `C:\Users\egork\AppData\Local\Programs\Ollama\ollama.exe` |
| Host | `127.0.0.1:11434` |
| Models path | `C:\Users\egork\AppData\Local\Programs\Ollama` |
| Env | `OLLAMA_HOST=127.0.0.1:11434` (User scope) |
| Моделей | 11 (~97 ГБ) |
| Keep-alive | 5 минут (выгрузка из VRAM при простое) |

### API Gateway: LiteLLM Proxy 1.92.0

| Параметр | Значение |
|----------|----------|
| Binary | `D:\Projects\ai\.venv\Scripts\litellm.exe` |
| Host | `127.0.0.1:4000` |
| Config | `config/litellm/config.yaml` |
| Auth | `master_key` из `os.environ/LITELLM_API_KEY` |
| Launch | `scripts/setup/start-litellm.bat` |
| Env | `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` |

Расшифровывает `.secrets.yaml` через SOPS при запуске.

### Router Proxy (автороутинг)

| Параметр | Значение |
|----------|----------|
| Binary | `D:\Projects\ai\.venv\Scripts\python.exe` |
| Script | `scripts/ai/router_proxy.py` |
| Host | `127.0.0.1:4001` |
| Backend | LiteLLM (`127.0.0.1:4000`) |
| Launch | `scripts/setup/start-router.bat` |
| Лог | `logs/router.log` |

**Модели:**

| Model ID | Поведение |
|----------|----------|
| `auto` | Анализ сложности → выбор модели |
| `preset-light` | Всегда `coder-low` |
| `preset-medium` | Всегда `coder-medium` |
| `preset-heavy` | Всегда `coder-high` |

**Эвристика `auto`:**

| Сигнал | Балл |
|--------|------|
| Ключевые слова "refactor, architecture, rewrite" | +3 |
| Ключевые слова "fix, add, implement" | +1 |
| Ключевые слова "rename, comment, format" | −1 |
| Контекст > 10K символов | +4 |
| Контекст > 5K символов | +2 |
| Каждый code block | +2 (макс 6) |
| Каждая ссылка на файл | +1 (макс 3) |

Итог: score ≥ 6 → `coder-high`, ≥ 2 → `coder-medium`, иначе `coder-low`.

### Vector DB: Qdrant 1.18.3

| Параметр | Значение |
|----------|----------|
| Binary | `C:\Tools\qdrant\qdrant.exe` |
| HTTP | `127.0.0.1:6333` |
| gRPC | `127.0.0.1:6334` |
| Config | `config/qdrant/qdrant.yaml` |
| Storage | `C:\Tools\qdrant\storage\` |
| Launch | `scripts/setup/start-qdrant.bat` |

### Chat UI: Open WebUI 0.10.2

| Параметр | Значение |
|----------|----------|
| Binary | `D:\Projects\ai\.venv-webui\Scripts\open-webui.exe` |
| Python | 3.12.13 (отдельный venv `.venv-webui/`) |
| Host | `127.0.0.1:8080` |
| Ollama URL | `http://127.0.0.1:11434` |
| OpenAI API | `http://127.0.0.1:4000/v1` (LiteLLM) |
| Data dir | `D:\Projects\ai\data\open-webui\` |
| Secret key | `D:\Projects\ai\.webui_secret_key` |
| Launch | `scripts/setup/start-webui.bat` |

### Autonomous Agent: Cline (VS Code)

| Параметр | Значение |
|----------|----------|
| Extension | `saoudrizwan.claude-dev` |
| Provider | OpenAI Compatible |
| Base URL | `http://127.0.0.1:4001/v1` (Router) |
| Plan-модель | `preset-heavy` (qwen3-coder:30b) |
| Act-модель | `preset-medium` (deepseek-coder-v2:lite) |
| Config | `globalStorage/saoudrizwan.claude-dev/settings/` |
| MCP config | `cline_mcp_settings.json` |
| Capabilities | File R/W, terminal, browser, MCP |

### Coding Agent: Aider 0.86.2

| Параметр | Значение |
|----------|----------|
| Binary | `D:\Projects\ai\.venv\Scripts\aider.exe` |
| Wrapper | `scripts/setup/aider.bat` |
| API | LiteLLM (`http://127.0.0.1:4000/v1`) |
| Модель по умолчанию | `openai/coder-low` |
| Config | `.aider.conf.yml` |
| Edit format | diff (SEARCH/REPLACE) |
| Git | Auto-commit |

### GhidraMCP 1.4

| Параметр | Значение |
|----------|----------|
| Plugin | `tools/ghidramcp/GhidraMCP-1-4.zip` |
| Bridge | `tools/ghidramcp/bridge_mcp_ghidra.py` |
| Python venv | `.venv-mcp/` (Python 3.12) |
| Ghidra HTTP | `127.0.0.1:8080` |
| MCP Bridge | `127.0.0.1:8081` (SSE) |
| Launch | `scripts/setup/start-ghidra-mcp.bat` |

**Инструменты MCP:**
`list_functions`, `decompile_function`, `disassemble_function`,
`rename_function`, `set_comment`, `get_xrefs_to`, `list_strings`,
`get_function_info`

### Obsidian Vault Generator

| Параметр | Значение |
|----------|----------|
| Script | `scripts/obsidian/create_vault.py` |
| Auto-setup | `scripts/setup_helper.py` |
| Структура | `.obsidian-memory/` в папке проекта |
| Rules file | `.clinerules` в корне проекта |

### RAG: LangChain + Qdrant + Ollama

| Компонент | Пакет | Версия |
|-----------|-------|--------|
| Framework | langchain | 1.3.14 |
| Ollama | langchain-ollama | 1.1.0 |
| Qdrant | langchain-qdrant | 1.1.0 |
| Splitter | langchain-text-splitters | 1.1.2 |
| Client | qdrant-client | 1.18.0 |

Pipeline: `scripts/rag/rag_pipeline.py`
- `ingest <file>` — TextLoader → RecursiveCharacterTextSplitter (500/50) → OllamaEmbeddings → Qdrant
- `query "question"` — Qdrant retriever (k=3) → ChatOllama → answer

### Agents: LangGraph 1.2.9

Workflow: `scripts/rag/agent_workflow.py`
- `create_react_agent(llm, tools)` — ReAct pattern
- Tools: `calculate`, `echo`

### Secrets: SOPS 3.13.2 + age 1.3.1

| Параметр | Значение |
|----------|----------|
| SOPS | `C:\Tools\sops\sops.exe` |
| age | `C:\Tools\age\age\age.exe` |
| Keypair | `~/.config/sops/age/keys.txt` |
| Config | `.sops.yaml` |
| Encrypted | `.secrets.yaml` (gitignored) |
| Recipient | `age174mut7mmj64wxvjhkpnl7fc06egzwu4kfxxjeufqj837dlkflc0qhcetdh` |

### Python: uv 0.11.29

| Параметр | Значение |
|----------|----------|
| Python | 3.10.10 (основной), 3.12.13 (WebUI, MCP) |
| uv | 0.11.29 |
| venv | `.venv/` (основной), `.venv-webui/`, `.venv-mcp/` |
| Lockfile | `uv.lock` |

---

## Сетевая топология

```
127.0.0.1:11434  → Ollama (HTTP API)
127.0.0.1:4000   → LiteLLM Proxy (OpenAI-compatible)
127.0.0.1:4001   → Router Proxy (автороутинг)
127.0.0.1:6333   → Qdrant REST API
127.0.0.1:6334   → Qdrant gRPC API
127.0.0.1:8080   → Open WebUI / Ghidra HTTP
127.0.0.1:8081   → GhidraMCP Bridge (SSE)
```

Все порты заблокированы inbound через Windows Firewall.

---

## Потоки данных

### Chat Completion (через Router)

```
VS Code (Cline) → POST :4001/v1/chat/completions
  → Router анализирует сложность
  → Выбирает модель (coder-low / medium / high)
  → POST :4000/v1/chat/completions
  → LiteLLM auth (API key)
  → Route by alias → POST :11434/api/chat
  → Ollama inference
  → Response → LiteLLM → Router → Cline
```

### RAG Ingest

```
rag_pipeline.py ingest <file>
  → TextLoader
  → RecursiveCharacterTextSplitter (chunk=500, overlap=50)
  → OllamaEmbeddings (nomic-embed-text)
  → QdrantVectorStore.from_documents (:6333)
```

### RAG Query

```
rag_pipeline.py query "question"
  → OllamaEmbeddings (embed question)
  → Qdrant search (top-3)
  → ChatPromptTemplate (context + question)
  → ChatOllama (qwen3:8b)
  → Answer
```

### Ghidra Analysis (через Cline MCP)

```
Cline → MCP SSE :8081
  → bridge_mcp_ghidra.py
  → HTTP :8080 (GhidraMCP plugin)
  → Ghidra decompile/rename/comment
  → Result → Bridge → Cline
  → Cline writes findings to .obsidian-memory/research/
```

---

## Уровни безопасности

| # | Слой | Реализация |
|---|------|-----------|
| 1 | Сеть | Все сервисы на `127.0.0.1` |
| 2 | Firewall | 6+ inbound block правил |
| 3 | API auth | LiteLLM `master_key` |
| 4 | Секреты | SOPS + age, `.secrets.yaml` |
| 5 | Git | `.gitignore` исключает секреты, ключи, venv |

---

## Переменные окружения

| Переменная | Scope | Значение |
|------------|-------|----------|
| `OLLAMA_HOST` | User | `127.0.0.1:11434` |
| `OLLAMA_MODELS` | User | `C:\Users\egork\AppData\Local\Programs\Ollama` |
| `SOPS_AGE_KEY_FILE` | User | `~/.config/sops/age/keys.txt` |
| `LITELLM_API_KEY` | Runtime (SOPS) | `sk-...` |
| `OPENAI_API_KEY` | User | То же что `LITELLM_API_KEY` (для Aider) |
| `CONTINUE_API_KEY` | User | То же что `LITELLM_API_KEY` |
| `PYTHONUTF8` | Runtime | `1` |
| `PYTHONIOENCODING` | Runtime | `utf-8` |

## PATH (User scope)

```
C:\Tools\age\age
C:\Tools\sops
C:\Tools\qdrant
```

---

## Конфигурационные файлы

| Файл | Описание |
|------|----------|
| `config/litellm/config.yaml` | Роутинг 11 моделей, master_key, timeout 300s |
| `config/qdrant/qdrant.yaml` | Host, порты, storage path |
| `.sops.yaml` | Regex `\.secrets\.yaml$` → age recipient |
| `.secrets.yaml` | Зашифрованные ключи (gitignored) |
| `.aider.conf.yml` | Модель, API base, edit-format |
| `.aider.model.settings.yml` | Параметры моделей для Aider |
| `.clinerules` | Глобальные правила для Cline |
| `.vscode/settings.json` | Python interpreter, UTF-8 |
| `.devcontainer/devcontainer.json` | Docker dev container |
| `.gitignore` | Исключения |
| `.gitattributes` | Line endings + LFS |
| `.python-version` | `3.10` |
