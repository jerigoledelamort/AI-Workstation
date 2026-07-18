# Changelog

Р’СЃРµ Р·Р°РјРµС‚РЅС‹Рµ РёР·РјРµРЅРµРЅРёСЏ AI Workstation РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅС‹ Р·РґРµСЃСЊ.
Р¤РѕСЂРјР°С‚ РѕСЃРЅРѕРІР°РЅ РЅР° [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] вЂ” 2026-07-18

### Phase 1: Project Structure
- РЎРѕР·РґР°РЅС‹ РґРёСЂРµРєС‚РѕСЂРёРё: `config/`, `scripts/`, `docs/`, `data/`, `tests/`
- `.gitkeep` С„Р°Р№Р»С‹ РґР»СЏ СЃРѕС…СЂР°РЅРµРЅРёСЏ СЃС‚СЂСѓРєС‚СѓСЂС‹
- `README.md` СЃ РѕРїРёСЃР°РЅРёРµРј РїСЂРѕРµРєС‚Р°
- `.gitignore` Рё `.gitattributes`

### Phase 2: Base Infrastructure
- Python 3.10.10 venv С‡РµСЂРµР· uv 0.11.29
- `pyproject.toml` СЃ Р·Р°РІРёСЃРёРјРѕСЃС‚СЏРјРё
- MkDocs Material 9.7.7
- `mkdocs.yml` СЃ С‚РµРјРѕР№ Material, РїРµСЂРµРєР»СЋС‡РµРЅРёРµРј dark/light
- `docs/index.md` вЂ” РіР»Р°РІРЅР°СЏ СЃС‚СЂР°РЅРёС†Р°

### Phase 3: AI Inference Layer
- Ollama 0.32.0 СѓСЃС‚Р°РЅРѕРІР»РµРЅ, `OLLAMA_HOST=127.0.0.1:11434`
- 11 РјРѕРґРµР»РµР№ Р·Р°РіСЂСѓР¶РµРЅС‹ (~97 Р“Р‘):
  - Low: qwen3:8b, qwen2.5-coder:7b, qwen2.5vl:3b, nomic-embed-text
  - Medium: qwen2.5:14b, deepseek-coder-v2:lite, qwen2.5vl:7b, bge-m3
  - High: qwen2.5:32b, qwen3-coder:30b, qwen2.5vl:32b
- LiteLLM Proxy 1.92.0 РЅР° РїРѕСЂС‚Сѓ 4000
- `config/litellm/config.yaml` вЂ” СЂРѕСѓС‚РёРЅРі 11 РјРѕРґРµР»РµР№ С‡РµСЂРµР· Р°Р»РёР°СЃС‹
- SOPS 3.13.2 + age 1.3.1 РґР»СЏ С€РёС„СЂРѕРІР°РЅРёСЏ `.secrets.yaml`
- `scripts/setup/start-litellm.bat` СЃ `PYTHONUTF8=1` РґР»СЏ Unicode

### Phase 4: Dev Environment
- Continue v2.0.0 (VS Code extension)
- `~/.continue/config.json` вЂ” 6 РјРѕРґРµР»РµР№ + autocomplete + embeddings
- `.vscode/settings.json` вЂ” Python interpreter, UTF-8, РёСЃРєР»СЋС‡РµРЅРёСЏ
- `.devcontainer/devcontainer.json` вЂ” Docker dev config

### Phase 5: Security
- `tests/test-security.ps1` вЂ” 10 РїСЂРѕРІРµСЂРѕРє (РІСЃРµ PASS):
  1. Ollama bind to localhost
  2. 6 firewall inbound block rules
  3. LiteLLM rejects unauthenticated requests
  4. Secrets encrypted (SOPS)
  5. age keypair exists
  6-8. .gitignore: .secrets.yaml, *.key, .env
  9. LiteLLM proxy healthy
  10. Ollama healthy
- 6 Windows Firewall РїСЂР°РІРёР»:
  - Block-Ollama-Inbound (11434)
  - Block-LiteLLM-Inbound (4000)
  - Block-Qdrant-REST-Inbound (6333)
  - Block-Qdrant-gRPC-Inbound (6334)
  - Block-OpenWebUI-Inbound (8080)
  - Block-MkDocs-Inbound (8000)

### Phase 6: RAG & Agents
- Qdrant 1.18.3 (РЅР°С‚РёРІРЅС‹Р№ Р±РёРЅР°СЂРЅРёРє, Р±РµР· Docker)
- `config/qdrant/qdrant.yaml` вЂ” localhost binding
- `scripts/setup/start-qdrant.bat`
- LangChain 1.3.14 + langchain-ollama 1.1.0 + langchain-qdrant 1.1.0
- LangGraph 1.2.9
- `scripts/rag/rag_pipeline.py` вЂ” ingest + query (С‚РµСЃС‚: 4 С‡Р°РЅРєР°, РѕС‚РІРµС‚ РєРѕСЂСЂРµРєС‚РЅС‹Р№)
- `scripts/rag/agent_workflow.py` вЂ” tool calling (С‚РµСЃС‚: 25*4=100)

### Phase 7: Automation
- 7 СЃРєСЂРёРїС‚РѕРІ:
  - `scripts/setup/start-all.ps1` вЂ” Р·Р°РїСѓСЃРє Ollama + Qdrant + LiteLLM
  - `scripts/setup/stop-all.ps1` вЂ” РѕСЃС‚Р°РЅРѕРІРєР° РІСЃРµС…
  - `scripts/monitoring/health-check.ps1` вЂ” РїСЂРѕРІРµСЂРєР° 3 СЃРµСЂРІРёСЃРѕРІ
  - `scripts/monitoring/vram-check.ps1` вЂ” nvidia-smi + RAM
  - `scripts/maintenance/update-models.ps1` вЂ” ollama pull
  - `scripts/maintenance/cleanup-models.ps1` вЂ” СЃРїРёСЃРѕРє РјРѕРґРµР»РµР№
  - `scripts/backup/backup.ps1` вЂ” СЂРµР·РµСЂРІРЅРѕРµ РєРѕРїРёСЂРѕРІР°РЅРёРµ

### Phase 8: Documentation
- 7 СЃС‚СЂР°РЅРёС† MkDocs: requirements, architecture, roadmap, ai-models, tdr, security, runbook
- `mkdocs build --strict` вЂ” PASS

### Phase 9: Tests & Audit
- `tests/test-inference.ps1` вЂ” 6/6 PASS (4 chat + 2 embed)
- `tests/test-security.ps1` вЂ” 10/10 PASS

### Pre-Installation Safety
- Restore Point (ID 79) СЃРѕР·РґР°РЅ
- Р‘СЌРєР°Рї РїРѕР»СЊР·РѕРІР°С‚РµР»СЊСЃРєРёС… РєРѕРЅС„РёРіРѕРІ РІ `D:\Projects\ai\backup\`
- Р›РѕРі СѓСЃС‚Р°РЅРѕРІРєРё: `D:\Projects\ai\logs\install.log`