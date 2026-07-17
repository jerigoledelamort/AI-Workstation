# Requirements

Локальная AI-станция для разработки ПО. Полностью локальная, без облачных API.

## Hardware

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen 7 7800X3D (8C/8T, 96MB 3D V-Cache) |
| RAM | 64GB DDR5 6400MHz |
| GPU | NVIDIA RTX 5070 (12GB VRAM) |
| Storage | Samsung 990 PRO 2TB NVMe + Seagate 4TB HDD |

## Principles

1. **Privacy** — exclusively local, no cloud APIs
2. **Quality > Performance** — larger models with CPU offload acceptable
3. **Security** — localhost-only, API key auth, SOPS encrypted secrets
4. **Reproducibility** — uv lock, .python-version, .gitattributes

## VRAM Profiles

| Profile | Chat | Coding | Vision | Embeddings |
|---------|------|--------|--------|------------|
| Low | qwen3:8b | qwen2.5-coder:7b | qwen2.5vl:3b | nomic-embed-text |
| Medium | qwen2.5:14b | deepseek-coder-v2:lite | qwen2.5vl:7b | bge-m3 |
| High | qwen2.5:32b | qwen3-coder:30b | qwen2.5vl:32b | bge-m3 |