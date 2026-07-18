# Roadmap

## Текущий статус (v0.1.0)

| Phase | Name | Status |
|-------|------|--------|
| 1 | Project structure | ✅ Complete |
| 2 | Base infrastructure | ✅ Complete |
| 3 | AI inference layer | ✅ Complete |
| 4 | Dev environment | ✅ Complete |
| 5 | Security | ✅ Complete |
| 6 | RAG & agents | ✅ Complete |
| 7 | Automation | ✅ Complete |
| 8 | Documentation | ✅ Complete |
| 9 | Tests & audit | ✅ Complete |

## Планы развития

### v0.2 — Open WebUI ✅ ✅

- Установка Open WebUI (`pip install open-webui`)
- Интеграция с LiteLLM Proxy
- Web UI для чата с моделями
- Порт 8080 (firewall rule уже создан)

### v0.3 — MCP Server

- Model Context Protocol server
- Интеграция с Continue
- Tool calling из VS Code

### v0.4 — Advanced RAG

- Поддержка PDF, Markdown, кода
- Chunking стратегии (semantic, code-aware)
- Hybrid search (dense + sparse)
- Re-ranking моделей

### v0.5 — Multi-agent Workflows

- LangGraph multi-agent orchestration
- Специализированные агенты (coder, reviewer, tester)
- Workflow templates

### v0.6 — Model Fine-tuning

- LoRA fine-tuning через Unsloth
- Локальные датасеты
- Custom model registry

### v1.0 — Production Ready

- Systemd/Windows Service для автозапуска
- Monitoring dashboard (Prometheus + Grafana)
- CI/CD pipeline
- Full backup/restore automation