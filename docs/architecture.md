# Architecture

## System Overview

```
[User] → [LiteLLM Proxy :4000] → [Ollama :11434] → [Models]
                ↑                         ↓
        [API Key Auth]          [Embeddings :11434]
                                        ↓
[User] → [RAG Pipeline] → [Qdrant :6333/:6334]
[User] → [Agent Workflow] → [Ollama :11434]
```

## Components

| Component | Technology | Port |
|-----------|-----------|------|
| Inference | Ollama 0.32 | 11434 |
| API Gateway | LiteLLM Proxy | 4000 |
| Vector DB | Qdrant 1.18.3 | 6333/6334 |
| RAG | LangChain + langchain-qdrant | — |
| Agents | LangGraph | — |
| Secrets | SOPS + age | — |
| Python | uv + venv | — |
| Docs | MkDocs Material | 8000 |

## Network Topology

All services bind to `127.0.0.1` only. Windows Firewall blocks all inbound traffic on service ports.

## Security Layers

1. Ollama: localhost-only (OLLAMA_HOST=127.0.0.1:11434)
2. LiteLLM: API key auth (master_key from SOPS)
3. Firewall: 6 inbound block rules
4. SOPS: age-encrypted secrets
5. Git: .gitignore excludes secrets, keys, .env