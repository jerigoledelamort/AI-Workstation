# Roadmap

## РўРµРєСѓС‰РёР№ СЃС‚Р°С‚СѓСЃ (v0.1.0)

| Phase | Name | Status |
|-------|------|--------|
| 1 | Project structure | вњ… Complete |
| 2 | Base infrastructure | вњ… Complete |
| 3 | AI inference layer | вњ… Complete |
| 4 | Dev environment | вњ… Complete |
| 5 | Security | вњ… Complete |
| 6 | RAG & agents | вњ… Complete |
| 7 | Automation | вњ… Complete |
| 8 | Documentation | вњ… Complete |
| 9 | Tests & audit | вњ… Complete |

## РџР»Р°РЅС‹ СЂР°Р·РІРёС‚РёСЏ

### v0.2 вЂ” Open WebUI

- РЈСЃС‚Р°РЅРѕРІРєР° Open WebUI (`pip install open-webui`)
- РРЅС‚РµРіСЂР°С†РёСЏ СЃ LiteLLM Proxy
- Web UI РґР»СЏ С‡Р°С‚Р° СЃ РјРѕРґРµР»СЏРјРё
- РџРѕСЂС‚ 8080 (firewall rule СѓР¶Рµ СЃРѕР·РґР°РЅ)

### v0.3 вЂ” MCP Server

- Model Context Protocol server
- РРЅС‚РµРіСЂР°С†РёСЏ СЃ Continue
- Tool calling РёР· VS Code

### v0.4 вЂ” Advanced RAG

- РџРѕРґРґРµСЂР¶РєР° PDF, Markdown, РєРѕРґР°
- Chunking СЃС‚СЂР°С‚РµРіРёРё (semantic, code-aware)
- Hybrid search (dense + sparse)
- Re-ranking РјРѕРґРµР»РµР№

### v0.5 вЂ” Multi-agent Workflows

- LangGraph multi-agent orchestration
- РЎРїРµС†РёР°Р»РёР·РёСЂРѕРІР°РЅРЅС‹Рµ Р°РіРµРЅС‚С‹ (coder, reviewer, tester)
- Workflow templates

### v0.6 вЂ” Model Fine-tuning

- LoRA fine-tuning С‡РµСЂРµР· Unsloth
- Р›РѕРєР°Р»СЊРЅС‹Рµ РґР°С‚Р°СЃРµС‚С‹
- Custom model registry

### v1.0 вЂ” Production Ready

- Systemd/Windows Service РґР»СЏ Р°РІС‚РѕР·Р°РїСѓСЃРєР°
- Monitoring dashboard (Prometheus + Grafana)
- CI/CD pipeline
- Full backup/restore automation