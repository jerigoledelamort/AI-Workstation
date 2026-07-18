# Roadmap

## Текущий статус: v0.5.0

| Версия | Компонент | Статус |
|--------|-----------|--------|
| 0.1 | Базовая инфраструктура + inference + security + RAG | ✅ Complete |
| 0.2 | Open WebUI + автозапуск | ✅ Complete |
| 0.3 | Aider (CLI coding agent) | ✅ Complete |
| 0.4 | Cline (autonomous VS Code agent) | ✅ Complete |
| 0.5 | Router Proxy + GhidraMCP + Obsidian | ✅ Complete |

---

## Планы развития

### v0.6 — Advanced RAG

- [ ] Поддержка PDF, Markdown, кода
- [ ] Semantic chunking (code-aware)
- [ ] Hybrid search (dense + sparse)
- [ ] Re-ranking моделей
- [ ] Qdrant Web UI (или替代)

### v0.7 — Multi-agent Workflows

- [ ] LangGraph multi-agent orchestration
- [ ] Специализированные агенты (coder, reviewer, tester)
- [ ] Workflow templates
- [ ] Agent-to-agent коммуникация

### v0.8 — Model Fine-tuning

- [ ] LoRA fine-tuning через Unsloth
- [ ] Локальные датасеты
- [ ] Custom model registry
- [ ] Evaluation pipeline

### v0.9 — Monitoring & Observability

- [ ] Prometheus metrics (LiteLLM, Ollama)
- [ ] Grafana dashboard
- [ ] Alerting (VRAM, latency, errors)
- [ ] Token usage tracking

### v1.0 — Production Ready

- [ ] Windows Service (вместо Task Scheduler)
- [ ] CI/CD pipeline
- [ ] Full backup/restore automation
- [ ] Multi-user support (если понадобится)
- [ ] Performance benchmarking suite

---

## Идеи (без приоритета)

- Voice interface (Whisper локально)
- Code search across all projects (Qdrant)
- Automated code review на git hooks
- Custom MCP servers для других инструментов (IDA Pro, x64dbg)
- Distributed inference (если появится 2-я GPU)
