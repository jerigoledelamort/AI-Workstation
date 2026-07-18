# Architecture

## System Overview

```
в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ
в”‚                    AI Workstation                        в”‚
в”‚                                                         в”‚
в”‚  в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ    в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ    в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ  в”‚
в”‚  в”‚  VS Code в”‚в”Ђв”Ђв”Ђв–¶в”‚  LiteLLM     в”‚в”Ђв”Ђв”Ђв–¶в”‚   Ollama      в”‚  в”‚
в”‚  в”‚ Continue в”‚    в”‚  Proxy       в”‚    в”‚   :11434      в”‚  в”‚
в”‚  в”‚          в”‚    в”‚  :4000       в”‚    в”‚   11 models   в”‚  в”‚
в”‚  в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”    в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”¬в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”    в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”¬в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”  в”‚
в”‚                         в”‚                    в”‚          в”‚
в”‚                    API Key Auth         Embeddings      в”‚
в”‚                         в”‚                    в”‚          в”‚
в”‚  в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ    в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв–јв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ    в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв–јв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ  в”‚
в”‚  в”‚  RAG     в”‚в”Ђв”Ђв”Ђв–¶в”‚  Qdrant      в”‚в—Ђв”Ђв”Ђв”Ђв”‚   Ollama      в”‚  в”‚
в”‚  в”‚  Pipelineв”‚    в”‚  :6333/6334  в”‚    в”‚   Embeddings  в”‚  в”‚
в”‚  в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”    в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”    в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”  в”‚
в”‚                                                         в”‚
в”‚  в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ    в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ                       в”‚
в”‚  в”‚  Agent   в”‚в”Ђв”Ђв”Ђв–¶в”‚  Ollama      в”‚  Tool Calling         в”‚
в”‚  в”‚  Workflowв”‚    в”‚  :11434      в”‚  (LangGraph)          в”‚
в”‚  в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”    в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”                       в”‚
в”‚                                                         в”‚
в”‚  в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ    в”Њв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”ђ                       в”‚
в”‚  в”‚  MkDocs  в”‚    в”‚  SOPS + age  в”‚  Secrets              в”‚
в”‚  в”‚  :8000   в”‚    в”‚  .secrets    в”‚  Encryption           в”‚
в”‚  в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”    в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”                       в”‚
в””в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”
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
| Models | 11 (~97 Р“Р‘ total) |

### API Gateway: LiteLLM Proxy 1.92.0

| Parameter | Value |
|-----------|-------|
| Binary | `D:\Projects\ai\.venv\Scripts\litellm.exe` |
| Host | `127.0.0.1:4000` |
| Config | `config/litellm/config.yaml` |
| Auth | `master_key` from `os.environ/LITELLM_API_KEY` |
| Launch | `scripts/setup/start-litellm.bat` |
| Env | `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` |

LiteLLM decrypts `.secrets.yaml` С‡РµСЂРµР· SOPS РїСЂРё Р·Р°РїСѓСЃРєРµ, СѓСЃС‚Р°РЅР°РІР»РёРІР°СЏ `LITELLM_API_KEY` РІ РѕРєСЂСѓР¶РµРЅРёРµ.

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
- `ingest <file>` вЂ” TextLoader в†’ RecursiveCharacterTextSplitter (500/50) в†’ OllamaEmbeddings в†’ Qdrant
- `query "question"` вЂ” Qdrant retriever (k=3) в†’ ChatOllama в†’ answer

### Agents: LangGraph 1.2.9

| Component | Package | Version |
|-----------|---------|---------|
| Framework | langgraph | 1.2.9 |
| Prebuilt | langgraph-prebuilt | 1.1.0 |

Workflow: `scripts/rag/agent_workflow.py`
- `create_react_agent(llm, tools)` вЂ” ReAct pattern
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
| Binary | `D:\Projects\ai\.venv-webui\Scripts\open-webui.exe` |
| Python | 3.12.13 (separate venv: `.venv-webui/`) |
| Host | `127.0.0.1:8080` |
| Ollama URL | `http://127.0.0.1:11434` |
| OpenAI API URL | `http://127.0.0.1:4000/v1` (LiteLLM) |
| OpenAI API Key | `$LITELLM_API_KEY` (from SOPS) |
| Data dir | `D:\Projects\ai\data\open-webui\` |
| Secret key | `D:\Projects\ai\.webui_secret_key` |
| Launch | `scripts/setup/start-webui.ps1` |

### Docs: MkDocs Material 9.7.7

| Parameter | Value |
|-----------|-------|
| Config | `mkdocs.yml` |
| Pages | `docs/` (7 СЃС‚СЂР°РЅРёС†) |
| Build | `python -m mkdocs build --strict` |
| Serve | `python -m mkdocs serve` в†’ `127.0.0.1:8000` |

## Network Topology

```
127.0.0.1:11434  в†’ Ollama (HTTP API)
127.0.0.1:4000   в†’ LiteLLM Proxy (OpenAI-compatible API)
127.0.0.1:6333   в†’ Qdrant REST API
127.0.0.1:6334   в†’ Qdrant gRPC API
127.0.0.1:8000   в†’ MkDocs (docs)
127.0.0.1:8080   в†’ (reserved for Open WebUI)
```

All ports blocked inbound by Windows Firewall.

## Data Flow

### Chat Completion
```
VS Code/Continue в†’ POST :4000/v1/chat/completions
  в†’ LiteLLM auth (API key)
  в†’ Route by model alias (e.g. "chat-low" в†’ ollama/qwen3:8b)
  в†’ POST :11434/api/chat
  в†’ Ollama inference
  в†’ Response в†’ LiteLLM в†’ Continue
```

### RAG Ingest
```
rag_pipeline.py ingest <file>
  в†’ TextLoader (read file)
  в†’ RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)
  в†’ OllamaEmbeddings (nomic-embed-text via :11434)
  в†’ QdrantVectorStore.from_documents (POST :6333/collections)
```

### RAG Query
```
rag_pipeline.py query "question"
  в†’ OllamaEmbeddings (embed question)
  в†’ Qdrant search (top-3 similar chunks)
  в†’ ChatPromptTemplate (context + question)
  в†’ ChatOllama (qwen3:8b via :11434)
  в†’ StrOutputParser в†’ answer
```

### Agent
```
agent_workflow.py "question"
  в†’ create_react_agent(ChatOllama, [calculate, echo])
  в†’ LLM decides tool call
  в†’ Tool execution
  в†’ LLM generates final answer
```

## Security Layers

1. **Network binding** вЂ” all services on `127.0.0.1` only
2. **Firewall** вЂ” 6 inbound block rules (11434, 4000, 6333, 6334, 8080, 8000)
3. **API auth** вЂ” LiteLLM `master_key` required for all requests
4. **Secrets encryption** вЂ” SOPS + age, `.secrets.yaml` encrypted at rest
5. **Git hygiene** вЂ” `.gitignore` excludes `.secrets.yaml`, `*.key`, `.env`, `.venv/`

## Environment Variables

| Variable | Scope | Value |
|----------|-------|-------|
| `OLLAMA_HOST` | User | `127.0.0.1:11434` |
| `OLLAMA_MODELS` | User | `C:\Users\egork\AppData\Local\Programs\Ollama` |
| `SOPS_AGE_KEY_FILE` | Runtime | `~/.config/sops/age/keys.txt` |
| `LITELLM_API_KEY` | Runtime (from SOPS) | `sk-...` (РІ .secrets.yaml) |
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

Р РѕСѓС‚РёРЅРі 11 РјРѕРґРµР»РµР№ С‡РµСЂРµР· Р°Р»РёР°СЃС‹ (chat-low, coder-medium, etc.) РЅР° Ollama. Master key РёР· `os.environ/LITELLM_API_KEY`. Request timeout: 300s. `drop_params: true`.

### config/qdrant/qdrant.yaml

Host: `127.0.0.1`, HTTP: 6333, gRPC: 6334. Storage: `./storage`.

### .sops.yaml

Regex `\.secrets\.yaml$` в†’ age recipient `age174mut7mmj64wxvjhkpnl7fc06egzwu4kfxxjeufqj837dlkflc0qhcetdh`.

### ~/.continue/config.json

6 РјРѕРґРµР»РµР№ (chat/coder Г— low/medium/high) + tabAutocompleteModel (coder-low) + embeddingsProvider (embed-low). All via `http://127.0.0.1:4000/v1` with `CONTINUE_API_KEY`.

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