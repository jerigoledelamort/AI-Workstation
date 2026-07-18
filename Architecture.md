# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    AI Workstation                        │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │  VS Code │───▶│  LiteLLM     │───▶│   Ollama      │  │
│  │ Continue │    │  Proxy       │    │   :11434      │  │
│  │          │    │  :4000       │    │   11 models   │  │
│  └──────────┘    └──────┬───────┘    └───────┬───────┘  │
│                         │                    │          │
│                    API Key Auth         Embeddings      │
│                         │                    │          │
│  ┌──────────┐    ┌──────▼───────┐    ┌───────▼───────┐  │
│  │  RAG     │───▶│  Qdrant      │◀───│   Ollama      │  │
│  │  Pipeline│    │  :6333/6334  │    │   Embeddings  │  │
│  └──────────┘    └──────────────┘    └───────────────┘  │
│                                                         │
│  ┌──────────┐    ┌──────────────┐                       │
│  │  Agent   │───▶│  Ollama      │  Tool Calling         │
│  │  Workflow│    │  :11434      │  (LangGraph)          │
│  └──────────┘    └──────────────┘                       │
│                                                         │
│  ┌──────────┐    ┌──────────────┐                       │
│  │  MkDocs  │    │  SOPS + age  │  Secrets              │
│  │  :8000   │    │  .secrets    │  Encryption           │
│  └──────────┘    └──────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

All services bind to 127.0.0.1. No external network access required.

## Components

### Inference: Ollama 0.32.0

| Parameter | Value |
|-----------|-------|
| Binary | `C:\Users\egork\AppData\Local\Programs\Ollama\ollama.exe` |
| Host | `127.0.0.1:11434` |
| Models path | `C:\Users\egork\AppData\Local\Programs\Ollama` (env: `OLLAMA_MODELS`) |
| Env var | `OLLAMA_HOST=127.0.0.1:11434` (User scope) |
| Models | 11 (~97 ГБ total) |

### API Gateway: LiteLLM Proxy 1.92.0

| Parameter | Value |
|-----------|-------|
| Binary | `D:\Projects\ai\.venv\Scripts\litellm.exe` |
| Host | `127.0.0.1:4000` |
| Config | `config/litellm/config.yaml` |
| Auth | `master_key` from `os.environ/LITELLM_API_KEY` |
| Launch | `scripts/setup/start-litellm.bat` |
| Env | `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` |

LiteLLM decrypts `.secrets.yaml` через SOPS при запуске, устанавливая `LITELLM_API_KEY` в окружение.

### Vector DB: Qdrant 1.18.3

| Parameter | Value |
|-----------|-------|
| Binary | `C:\Tools\qdrant\qdrant.exe` |
| HTTP | `127.0.0.1:6333` |
| gRPC | `127.0.0.1:6334` |
| Config | `config/qdrant/qdrant.yaml` |
| Storage | `C:\Tools\qdrant\storage\` |
| Launch | `scripts/setup/start-qdrant.bat` |

### RAG: LangChain + langchain-qdrant + langchain-ollama

| Component | Package | Version |
|-----------|---------|---------|
| Framework | langchain | 1.3.14 |
| Ollama integration | langchain-ollama | 1.1.0 |
| Qdrant integration | langchain-qdrant | 1.1.0 |
| Text splitter | langchain-text-splitters | 1.1.2 |
| Qdrant client | qdrant-client | 1.18.0 |

Pipeline: `scripts/rag/rag_pipeline.py`
- `ingest <file>` — TextLoader → RecursiveCharacterTextSplitter (500/50) → OllamaEmbeddings → Qdrant
- `query "question"` — Qdrant retriever (k=3) → ChatOllama → answer

### Agents: LangGraph 1.2.9

| Component | Package | Version |
|-----------|---------|---------|
| Framework | langgraph | 1.2.9 |
| Prebuilt | langgraph-prebuilt | 1.1.0 |

Workflow: `scripts/rag/agent_workflow.py`
- `create_react_agent(llm, tools)` — ReAct pattern
- Tools: `calculate`, `echo`

### Secrets: SOPS 3.13.2 + age 1.3.1

| Parameter | Value |
|-----------|-------|
| SOPS binary | `C:\Tools\sops\sops.exe` |
| age binary | `C:\Tools\age\age\age.exe` |
| age keypair | `~/.config/sops/age/keys.txt` |
| SOPS config | `.sops.yaml` |
| Encrypted file | `.secrets.yaml` (gitignored) |
| age recipient | `age174mut7mmj64wxvjhkpnl7fc06egzwu4kfxxjeufqj837dlkflc0qhcetdh` |

### Python: uv 0.11.29 + Python 3.10.10

| Parameter | Value |
|-----------|-------|
| Python | 3.10.10 |
| uv | 0.11.29 |
| venv | `D:\Projects\ai\.venv\` |
| Lockfile | `uv.lock` |
| pyproject | `pyproject.toml` |

### Chat UI: Open WebUI 0.10.2

| Parameter | Value |
|-----------|-------|
| Binary | D:\Projects\ai\.venv-webui\Scripts\open-webui.exe |
| Python | 3.12.13 (separate venv: .venv-webui/) |
| Host | 127.0.0.1:8080 |
| Ollama URL | http://127.0.0.1:11434 |
| OpenAI API URL | http://127.0.0.1:4000/v1 (LiteLLM) |
| OpenAI API Key | $LITELLM_API_KEY (from SOPS) |
| Data dir | D:\Projects\ai\data\open-webui\ |
| Secret key | D:\Projects\ai\.webui_secret_key |
| Launch | scripts/setup/start-webui.ps1 |

### Chat UI: Open WebUI 0.10.2

| Parameter | Value |
|-----------|-------|
| Binary | `D:\Projectsi\.venv-webui\Scripts\open-webui.exe` |
| Python | 3.12.13 (separate venv: `.venv-webui/`) |
| Host | `127.0.0.1:8080` |
| Ollama URL | `http://127.0.0.1:11434` |
| OpenAI API URL | `http://127.0.0.1:4000/v1` (LiteLLM) |
| OpenAI API Key | `$LITELLM_API_KEY` (from SOPS) |
| Data dir | `D:\Projectsi\data\open-webui\` |
| Secret key | `D:\Projectsi\.webui_secret_key` |
| Launch | `scripts/setup/start-webui.ps1` |

### Docs: MkDocs Material 9.7.7

| Parameter | Value |
|-----------|-------|
| Config | `mkdocs.yml` |
| Pages | `docs/` (7 страниц) |
| Build | `python -m mkdocs build --strict` |
| Serve | `python -m mkdocs serve` → `127.0.0.1:8000` |

## Network Topology

```
127.0.0.1:11434  → Ollama (HTTP API)
127.0.0.1:4000   → LiteLLM Proxy (OpenAI-compatible API)
127.0.0.1:6333   → Qdrant REST API
127.0.0.1:6334   → Qdrant gRPC API
127.0.0.1:8000   → MkDocs (docs)
127.0.0.1:8080   → (reserved for Open WebUI)
```

All ports blocked inbound by Windows Firewall.

## Data Flow

### Chat Completion
```
VS Code/Continue → POST :4000/v1/chat/completions
  → LiteLLM auth (API key)
  → Route by model alias (e.g. "chat-low" → ollama/qwen3:8b)
  → POST :11434/api/chat
  → Ollama inference
  → Response → LiteLLM → Continue
```

### RAG Ingest
```
rag_pipeline.py ingest <file>
  → TextLoader (read file)
  → RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)
  → OllamaEmbeddings (nomic-embed-text via :11434)
  → QdrantVectorStore.from_documents (POST :6333/collections)
```

### RAG Query
```
rag_pipeline.py query "question"
  → OllamaEmbeddings (embed question)
  → Qdrant search (top-3 similar chunks)
  → ChatPromptTemplate (context + question)
  → ChatOllama (qwen3:8b via :11434)
  → StrOutputParser → answer
```

### Agent
```
agent_workflow.py "question"
  → create_react_agent(ChatOllama, [calculate, echo])
  → LLM decides tool call
  → Tool execution
  → LLM generates final answer
```

## Security Layers

1. **Network binding** — all services on `127.0.0.1` only
2. **Firewall** — 6 inbound block rules (11434, 4000, 6333, 6334, 8080, 8000)
3. **API auth** — LiteLLM `master_key` required for all requests
4. **Secrets encryption** — SOPS + age, `.secrets.yaml` encrypted at rest
5. **Git hygiene** — `.gitignore` excludes `.secrets.yaml`, `*.key`, `.env`, `.venv/`

## Environment Variables

| Variable | Scope | Value |
|----------|-------|-------|
| `OLLAMA_HOST` | User | `127.0.0.1:11434` |
| `OLLAMA_MODELS` | User | `C:\Users\egork\AppData\Local\Programs\Ollama` |
| `SOPS_AGE_KEY_FILE` | Runtime | `~/.config/sops/age/keys.txt` |
| `LITELLM_API_KEY` | Runtime (from SOPS) | `sk-...` (в .secrets.yaml) |
| `PYTHONUTF8` | Runtime (start-litellm.bat) | `1` |
| `PYTHONIOENCODING` | Runtime (start-litellm.bat) | `utf-8` |
| `CONTINUE_API_KEY` | User/Process | Same as LITELLM_API_KEY |

## PATH (User scope)

```
C:\Tools\age\age
C:\Tools\sops
C:\Tools\qdrant
```

## Configuration Files

### config/litellm/config.yaml

Роутинг 11 моделей через алиасы (chat-low, coder-medium, etc.) на Ollama. Master key из `os.environ/LITELLM_API_KEY`. Request timeout: 300s. `drop_params: true`.

### config/qdrant/qdrant.yaml

Host: `127.0.0.1`, HTTP: 6333, gRPC: 6334. Storage: `./storage`.

### .sops.yaml

Regex `\.secrets\.yaml$` → age recipient `age174mut7mmj64wxvjhkpnl7fc06egzwu4kfxxjeufqj837dlkflc0qhcetdh`.

### ~/.continue/config.json

6 моделей (chat/coder × low/medium/high) + tabAutocompleteModel (coder-low) + embeddingsProvider (embed-low). All via `http://127.0.0.1:4000/v1` with `CONTINUE_API_KEY`.

### .vscode/settings.json

Python interpreter: `.venv\Scripts\python.exe`. UTF-8. EOL: LF. Search/file excludes for `.venv`, `site`, `__pycache__`.

### .devcontainer/devcontainer.json

Docker dev container with Python 3.10 + Node LTS. Extensions: Python, Pylance, Continue. Forward ports: 4000, 11434. `OLLAMA_HOST=host.docker.internal:11434`.

### mkdocs.yml

Material theme, Russian language, dark/light toggle, 7 pages in nav.

### .gitignore

Excludes: `.venv/`, `logs/`, `backup/`, `site/`, `.secrets.yaml`, `*.key`, `.env`, `.obsidian/`, model files (`*.gguf`, `*.safetensors`), `data/qdrant/*`, `data/open-webui/*`.

### .gitattributes

LF by default, CRLF for `*.ps1`, `*.bat`, `*.cmd`. Binary for images, archives, executables, models. Git LFS for `*.gguf`, `*.safetensors`.

### .python-version

```
3.10
```