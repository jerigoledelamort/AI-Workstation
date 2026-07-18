# Changelog

Р вЂ™РЎРѓР Вµ Р В·Р В°Р СР ВµРЎвЂљР Р…РЎвЂ№Р Вµ Р С‘Р В·Р СР ВµР Р…Р ВµР Р…Р С‘РЎРЏ AI Workstation Р Т‘Р С•Р С”РЎС“Р СР ВµР Р…РЎвЂљР С‘РЎР‚Р С•Р Р†Р В°Р Р…РЎвЂ№ Р В·Р Т‘Р ВµРЎРѓРЎРЉ.
Р В¤Р С•РЎР‚Р СР В°РЎвЂљ Р С•РЎРѓР Р…Р С•Р Р†Р В°Р Р… Р Р…Р В° [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] РІР‚вЂќ 2026-07-18

### Phase 1: Project Structure
- Р РЋР С•Р В·Р Т‘Р В°Р Р…РЎвЂ№ Р Т‘Р С‘РЎР‚Р ВµР С”РЎвЂљР С•РЎР‚Р С‘Р С‘: `config/`, `scripts/`, `docs/`, `data/`, `tests/`
- `.gitkeep` РЎвЂћР В°Р в„–Р В»РЎвЂ№ Р Т‘Р В»РЎРЏ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…Р С‘РЎРЏ РЎРѓРЎвЂљРЎР‚РЎС“Р С”РЎвЂљРЎС“РЎР‚РЎвЂ№
- `README.md` РЎРѓ Р С•Р С—Р С‘РЎРѓР В°Р Р…Р С‘Р ВµР С Р С—РЎР‚Р С•Р ВµР С”РЎвЂљР В°
- `.gitignore` Р С‘ `.gitattributes`

### Phase 2: Base Infrastructure
- Python 3.10.10 venv РЎвЂЎР ВµРЎР‚Р ВµР В· uv 0.11.29
- `pyproject.toml` РЎРѓ Р В·Р В°Р Р†Р С‘РЎРѓР С‘Р СР С•РЎРѓРЎвЂљРЎРЏР СР С‘
- MkDocs Material 9.7.7
- `mkdocs.yml` РЎРѓ РЎвЂљР ВµР СР С•Р в„– Material, Р С—Р ВµРЎР‚Р ВµР С”Р В»РЎР‹РЎвЂЎР ВµР Р…Р С‘Р ВµР С dark/light
- `docs/index.md` РІР‚вЂќ Р С–Р В»Р В°Р Р†Р Р…Р В°РЎРЏ РЎРѓРЎвЂљРЎР‚Р В°Р Р…Р С‘РЎвЂ Р В°

### Phase 3: AI Inference Layer
- Ollama 0.32.0 РЎС“РЎРѓРЎвЂљР В°Р Р…Р С•Р Р†Р В»Р ВµР Р…, `OLLAMA_HOST=127.0.0.1:11434`
- 11 Р СР С•Р Т‘Р ВµР В»Р ВµР в„– Р В·Р В°Р С–РЎР‚РЎС“Р В¶Р ВµР Р…РЎвЂ№ (~97 Р вЂњР вЂ):
  - Low: qwen3:8b, qwen2.5-coder:7b, qwen2.5vl:3b, nomic-embed-text
  - Medium: qwen2.5:14b, deepseek-coder-v2:lite, qwen2.5vl:7b, bge-m3
  - High: qwen2.5:32b, qwen3-coder:30b, qwen2.5vl:32b
- LiteLLM Proxy 1.92.0 Р Р…Р В° Р С—Р С•РЎР‚РЎвЂљРЎС“ 4000
- `config/litellm/config.yaml` РІР‚вЂќ РЎР‚Р С•РЎС“РЎвЂљР С‘Р Р…Р С– 11 Р СР С•Р Т‘Р ВµР В»Р ВµР в„– РЎвЂЎР ВµРЎР‚Р ВµР В· Р В°Р В»Р С‘Р В°РЎРѓРЎвЂ№
- SOPS 3.13.2 + age 1.3.1 Р Т‘Р В»РЎРЏ РЎв‚¬Р С‘РЎвЂћРЎР‚Р С•Р Р†Р В°Р Р…Р С‘РЎРЏ `.secrets.yaml`
- `scripts/setup/start-litellm.bat` РЎРѓ `PYTHONUTF8=1` Р Т‘Р В»РЎРЏ Unicode

### Phase 4: Dev Environment
- Continue v2.0.0 (VS Code extension)
- `~/.continue/config.json` РІР‚вЂќ 6 Р СР С•Р Т‘Р ВµР В»Р ВµР в„– + autocomplete + embeddings
- `.vscode/settings.json` РІР‚вЂќ Python interpreter, UTF-8, Р С‘РЎРѓР С”Р В»РЎР‹РЎвЂЎР ВµР Р…Р С‘РЎРЏ
- `.devcontainer/devcontainer.json` РІР‚вЂќ Docker dev config

### Phase 5: Security
- `tests/test-security.ps1` РІР‚вЂќ 10 Р С—РЎР‚Р С•Р Р†Р ВµРЎР‚Р С•Р С” (Р Р†РЎРѓР Вµ PASS):
  1. Ollama bind to localhost
  2. 6 firewall inbound block rules
  3. LiteLLM rejects unauthenticated requests
  4. Secrets encrypted (SOPS)
  5. age keypair exists
  6-8. .gitignore: .secrets.yaml, *.key, .env
  9. LiteLLM proxy healthy
  10. Ollama healthy
- 6 Windows Firewall Р С—РЎР‚Р В°Р Р†Р С‘Р В»:
  - Block-Ollama-Inbound (11434)
  - Block-LiteLLM-Inbound (4000)
  - Block-Qdrant-REST-Inbound (6333)
  - Block-Qdrant-gRPC-Inbound (6334)
  - Block-OpenWebUI-Inbound (8080)
  - Block-MkDocs-Inbound (8000)

### Phase 6: RAG & Agents
- Qdrant 1.18.3 (Р Р…Р В°РЎвЂљР С‘Р Р†Р Р…РЎвЂ№Р в„– Р В±Р С‘Р Р…Р В°РЎР‚Р Р…Р С‘Р С”, Р В±Р ВµР В· Docker)
- `config/qdrant/qdrant.yaml` РІР‚вЂќ localhost binding
- `scripts/setup/start-qdrant.bat`
- LangChain 1.3.14 + langchain-ollama 1.1.0 + langchain-qdrant 1.1.0
- LangGraph 1.2.9
- `scripts/rag/rag_pipeline.py` РІР‚вЂќ ingest + query (РЎвЂљР ВµРЎРѓРЎвЂљ: 4 РЎвЂЎР В°Р Р…Р С”Р В°, Р С•РЎвЂљР Р†Р ВµРЎвЂљ Р С”Р С•РЎР‚РЎР‚Р ВµР С”РЎвЂљР Р…РЎвЂ№Р в„–)
- `scripts/rag/agent_workflow.py` РІР‚вЂќ tool calling (РЎвЂљР ВµРЎРѓРЎвЂљ: 25*4=100)

### Phase 7: Automation
- 7 РЎРѓР С”РЎР‚Р С‘Р С—РЎвЂљР С•Р Р†:
  - `scripts/setup/start-all.ps1` РІР‚вЂќ Р В·Р В°Р С—РЎС“РЎРѓР С” Ollama + Qdrant + LiteLLM
  - `scripts/setup/stop-all.ps1` РІР‚вЂќ Р С•РЎРѓРЎвЂљР В°Р Р…Р С•Р Р†Р С”Р В° Р Р†РЎРѓР ВµРЎвЂ¦
  - `scripts/monitoring/health-check.ps1` РІР‚вЂќ Р С—РЎР‚Р С•Р Р†Р ВµРЎР‚Р С”Р В° 3 РЎРѓР ВµРЎР‚Р Р†Р С‘РЎРѓР С•Р Р†
  - `scripts/monitoring/vram-check.ps1` РІР‚вЂќ nvidia-smi + RAM
  - `scripts/maintenance/update-models.ps1` РІР‚вЂќ ollama pull
  - `scripts/maintenance/cleanup-models.ps1` РІР‚вЂќ РЎРѓР С—Р С‘РЎРѓР С•Р С” Р СР С•Р Т‘Р ВµР В»Р ВµР в„–
  - `scripts/backup/backup.ps1` РІР‚вЂќ РЎР‚Р ВµР В·Р ВµРЎР‚Р Р†Р Р…Р С•Р Вµ Р С”Р С•Р С—Р С‘РЎР‚Р С•Р Р†Р В°Р Р…Р С‘Р Вµ

### Phase 8: Documentation
- 7 РЎРѓРЎвЂљРЎР‚Р В°Р Р…Р С‘РЎвЂ  MkDocs: requirements, architecture, roadmap, ai-models, tdr, security, runbook
- `mkdocs build --strict` РІР‚вЂќ PASS

### Phase 9: Tests & Audit
- `tests/test-inference.ps1` РІР‚вЂќ 6/6 PASS (4 chat + 2 embed)
- `tests/test-security.ps1` РІР‚вЂќ 10/10 PASS

### Pre-Installation Safety
- Restore Point (ID 79) РЎРѓР С•Р В·Р Т‘Р В°Р Р…
- Р вЂРЎРЊР С”Р В°Р С— Р С—Р С•Р В»РЎРЉР В·Р С•Р Р†Р В°РЎвЂљР ВµР В»РЎРЉРЎРѓР С”Р С‘РЎвЂ¦ Р С”Р С•Р Р…РЎвЂћР С‘Р С–Р С•Р Р† Р Р† `D:\Projects\ai\backup\`
- Р вЂєР С•Р С– РЎС“РЎРѓРЎвЂљР В°Р Р…Р С•Р Р†Р С”Р С‘: `D:\Projects\ai\logs\install.log`