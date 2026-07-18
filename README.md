# AI Workstation

Р›РѕРєР°Р»СЊРЅР°СЏ AI-СЃС‚Р°РЅС†РёСЏ РґР»СЏ СЂР°Р·СЂР°Р±РѕС‚РєРё РџРћ. РџРѕР»РЅРѕСЃС‚СЊСЋ Р»РѕРєР°Р»СЊРЅР°СЏ, Р±РµР· РѕР±Р»Р°С‡РЅС‹С… API.

## Quick Start

```powershell
# Р—Р°РїСѓСЃРє РІСЃРµС… СЃРµСЂРІРёСЃРѕРІ
.\scripts\setup\start-all.ps1

# РџСЂРѕРІРµСЂРєР°
.\scripts\monitoring\health-check.ps1

# РћСЃС‚Р°РЅРѕРІРєР°
.\scripts\setup\stop-all.ps1
```

## РЎРµСЂРІРёСЃС‹

| РЎРµСЂРІРёСЃ | РџРѕСЂС‚ | РќР°Р·РЅР°С‡РµРЅРёРµ |
|--------|------|------------|
| Ollama | 127.0.0.1:11434 | Inference (11 РјРѕРґРµР»РµР№, ~97 Р“Р‘) |
| LiteLLM Proxy | 127.0.0.1:4000 | API gateway СЃ auth |
| Qdrant | 127.0.0.1:6333/6334 | Р’РµРєС‚РѕСЂРЅР°СЏ Р‘Р” РґР»СЏ RAG |
| MkDocs | 127.0.0.1:8000 | Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ |

## РљРѕРјР°РЅРґС‹

| РљРѕРјР°РЅРґР° | РћРїРёСЃР°РЅРёРµ |
|---------|----------|
| `.\scripts\setup\start-all.ps1` | Р—Р°РїСѓСЃРє Ollama + Qdrant + LiteLLM |
| `.\scripts\setup\stop-all.ps1` | РћСЃС‚Р°РЅРѕРІРєР° РІСЃРµС… СЃРµСЂРІРёСЃРѕРІ |
| `.\scripts\monitoring\health-check.ps1` | Health check РІСЃРµС… СЃРµСЂРІРёСЃРѕРІ |
| `.\scripts\monitoring\vram-check.ps1` | РњРѕРЅРёС‚РѕСЂРёРЅРі VRAM/RAM |
| `.\scripts\maintenance\update-models.ps1` | РћР±РЅРѕРІР»РµРЅРёРµ РјРѕРґРµР»РµР№ Ollama |
| `.\scripts\maintenance\cleanup-models.ps1` | РЎРїРёСЃРѕРє РјРѕРґРµР»РµР№ РґР»СЏ РѕС‡РёСЃС‚РєРё |
| `.\scripts\backup\backup.ps1` | Р РµР·РµСЂРІРЅРѕРµ РєРѕРїРёСЂРѕРІР°РЅРёРµ РєРѕРЅС„РёРіРѕРІ |
| `.\tests\test-security.ps1` | РђСѓРґРёС‚ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё (10 РїСЂРѕРІРµСЂРѕРє) |
| `.\tests\test-inference.ps1` | РўРµСЃС‚ inference РІСЃРµС… РјРѕРґРµР»РµР№ |
| `python -m mkdocs serve` | Р›РѕРєР°Р»СЊРЅР°СЏ РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ |

## RAG Рё Р°РіРµРЅС‚С‹

```powershell
# Р—Р°РіСЂСѓР·РёС‚СЊ РґРѕРєСѓРјРµРЅС‚ РІ Qdrant
.venv\Scripts\python.exe scripts\rag\rag_pipeline.py ingest <file_path>

# Р—Р°РїСЂРѕСЃ РїРѕ РґРѕРєСѓРјРµРЅС‚Р°Рј
.venv\Scripts\python.exe scripts\rag\rag_pipeline.py query "question"

# РђРіРµРЅС‚ СЃ tool calling
.venv\Scripts\python.exe scripts\rag\agent_workflow.py "question"
```

## РњРѕРґРµР»Рё

11 РјРѕРґРµР»РµР№ РІ 3 РїСЂРѕС„РёР»СЏС… VRAM. РџРѕРґСЂРѕР±РЅРѕСЃС‚Рё: [docs/ai-models.md](docs/ai-models.md).

| Profile | Chat | Coding | Vision | Embeddings |
|---------|------|--------|--------|------------|
| Low | qwen3:8b | qwen2.5-coder:7b | qwen2.5vl:3b | nomic-embed-text |
| Medium | qwen2.5:14b | deepseek-coder-v2:lite | qwen2.5vl:7b | bge-m3 |
| High | qwen2.5:32b | qwen3-coder:30b | qwen2.5vl:32b | bge-m3 |

## Р‘РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ

- Р’СЃРµ СЃРµСЂРІРёСЃС‹ РЅР° `127.0.0.1` С‚РѕР»СЊРєРѕ
- LiteLLM: API key auth (SOPS-encrypted)
- 6 firewall РїСЂР°РІРёР» (inbound block)
- SOPS + age РґР»СЏ СЃРµРєСЂРµС‚РѕРІ
- `.gitignore` РёСЃРєР»СЋС‡Р°РµС‚ СЃРµРєСЂРµС‚С‹, РєР»СЋС‡Рё, `.env`

## РЎС‚СЂСѓРєС‚СѓСЂР° РїСЂРѕРµРєС‚Р°

```
ai/
в”њв”Ђв”Ђ .secrets.yaml          # SOPS-Р·Р°С€РёС„СЂРѕРІР°РЅРЅС‹Рµ СЃРµРєСЂРµС‚С‹ (gitignored)
в”њв”Ђв”Ђ .sops.yaml             # SOPS config (age recipient)
в”њв”Ђв”Ђ .gitignore             # РСЃРєР»СЋС‡РµРЅРёСЏ
в”њв”Ђв”Ђ .gitattributes         # Line endings + LFS
в”њв”Ђв”Ђ .python-version        # 3.10
в”њв”Ђв”Ђ pyproject.toml         # Р—Р°РІРёСЃРёРјРѕСЃС‚Рё
в”њв”Ђв”Ђ uv.lock                # Lockfile
в”њв”Ђв”Ђ mkdocs.yml             # MkDocs config
в”њв”Ђв”Ђ config/
в”‚   в”њв”Ђв”Ђ litellm/config.yaml  # Р РѕСѓС‚РёРЅРі РјРѕРґРµР»РµР№
в”‚   в””в”Ђв”Ђ qdrant/qdrant.yaml   # Qdrant config
в”њв”Ђв”Ђ scripts/
в”‚   в”њв”Ђв”Ђ setup/             # start/stop СЃРєСЂРёРїС‚С‹
в”‚   в”њв”Ђв”Ђ monitoring/        # health-check, vram
в”‚   в”њв”Ђв”Ђ maintenance/       # update/cleanup models
в”‚   в”њв”Ђв”Ђ backup/            # backup
в”‚   в””в”Ђв”Ђ rag/               # RAG pipeline + agent
в”њв”Ђв”Ђ tests/                 # Security + inference С‚РµСЃС‚С‹
в”њв”Ђв”Ђ docs/                  # MkDocs СЃС‚СЂР°РЅРёС†С‹
в”њв”Ђв”Ђ .vscode/settings.json  # VS Code config
в””в”Ђв”Ђ .devcontainer/         # DevContainer config
```

## Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ

| Р¤Р°Р№Р» | РћРїРёСЃР°РЅРёРµ |
|------|----------|
| [Architecture.md](Architecture.md) | РђСЂС…РёС‚РµРєС‚СѓСЂР° СЃРёСЃС‚РµРјС‹ |
| [DisasterRecovery.md](DisasterRecovery.md) | Р’РѕСЃСЃС‚Р°РЅРѕРІР»РµРЅРёРµ Р±РµР· РёРЅС‚РµСЂРЅРµС‚Р° |
| [Troubleshooting.md](Troubleshooting.md) | Р РµС€РµРЅРёРµ РїСЂРѕР±Р»РµРј |
| [ROADMAP.md](ROADMAP.md) | РџР»Р°РЅ СЂР°Р·РІРёС‚РёСЏ |
| [CHANGELOG.md](CHANGELOG.md) | РСЃС‚РѕСЂРёСЏ РёР·РјРµРЅРµРЅРёР№ |
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | РР·РІРµСЃС‚РЅС‹Рµ РїСЂРѕР±Р»РµРјС‹ |

## Hardware

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen 7 7800X3D (8C/8T, 96MB 3D V-Cache) |
| RAM | 64GB DDR5 6400MHz |
| GPU | NVIDIA RTX 5070 (12GB VRAM) |
| Storage | Samsung 990 PRO 2TB NVMe + Seagate 4TB HDD |