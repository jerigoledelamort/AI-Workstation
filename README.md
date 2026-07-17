# AI Workstation

Локальная AI-станция для разработки ПО. Полностью локальная, без облачных API.

## Hardware

- CPU: AMD Ryzen 7 7800X3D (8C/8T, 96MB 3D V-Cache)
- RAM: 64GB DDR5 6400MHz
- GPU: NVIDIA RTX 5070 (12GB VRAM)
- Storage: Samsung 990 PRO 2TB NVMe + Seagate 4TB HDD

## Components

| Component | Technology | Status |
|-----------|-----------|--------|
| Inference | Ollama | Active |
| API Gateway | LiteLLM Proxy | Configured |
| Vector DB | Qdrant | Planned |
| Chat UI | Open WebUI | Planned |
| RAG | LangChain | Planned |
| Agents | LangGraph | Planned |
| Secrets | SOPS + age | Active |
| Python | uv | Active |
| Docs | MkDocs Material | Planned |

## Project Structure

```
config/     — Service configurations
scripts/    — Automation scripts
docs/       — MkDocs documentation
data/       — Service data (gitignored)
tests/      — Test scripts
```

## Documentation

- [Requirements](Requirements.md)
- [Architecture](Architecture.md)
- [Roadmap](Roadmap.md)
- [AI Workstation Models](AI-Workstation.md)
- [Technology Decisions](TechnologyDecisionRecord.md)
- [System Report](SystemReport.md)
- [Remediation Plan](FinalRemediationPlan.md)
