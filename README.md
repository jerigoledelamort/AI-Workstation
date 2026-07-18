# AI Workstation

Локальная AI-станция для разработки ПО. Полностью локальная, без облачных API.

## Quick Start

```powershell
# Запуск всех сервисов
.\scripts\setup\start-all.ps1

# Проверка
.\scripts\monitoring\health-check.ps1

# Остановка
.\scripts\setup\stop-all.ps1
```

## Сервисы

| Сервис | Порт | Назначение |
|--------|------|------------|
| Ollama | 127.0.0.1:11434 | Inference (11 моделей, ~97 ГБ) |
| LiteLLM Proxy | 127.0.0.1:4000 | API gateway с auth |
| Qdrant | 127.0.0.1:6333/6334 | Векторная БД для RAG |
| MkDocs | 127.0.0.1:8000 | Документация |

## Команды

| Команда | Описание |
|---------|----------|
| `.\scripts\setup\start-all.ps1` | Запуск Ollama + Qdrant + LiteLLM |
| `.\scripts\setup\stop-all.ps1` | Остановка всех сервисов |
| `.\scripts\monitoring\health-check.ps1` | Health check всех сервисов |
| `.\scripts\monitoring\vram-check.ps1` | Мониторинг VRAM/RAM |
| `.\scripts\maintenance\update-models.ps1` | Обновление моделей Ollama |
| `.\scripts\maintenance\cleanup-models.ps1` | Список моделей для очистки |
| `.\scripts\backup\backup.ps1` | Резервное копирование конфигов |
| `.\tests\test-security.ps1` | Аудит безопасности (10 проверок) |
| `.\tests\test-inference.ps1` | Тест inference всех моделей |
| `python -m mkdocs serve` | Локальная документация |

## RAG и агенты

```powershell
# Загрузить документ в Qdrant
.venv\Scripts\python.exe scripts\rag\rag_pipeline.py ingest <file_path>

# Запрос по документам
.venv\Scripts\python.exe scripts\rag\rag_pipeline.py query "question"

# Агент с tool calling
.venv\Scripts\python.exe scripts\rag\agent_workflow.py "question"
```

## Модели

11 моделей в 3 профилях VRAM. Подробности: [docs/ai-models.md](docs/ai-models.md).

| Profile | Chat | Coding | Vision | Embeddings |
|---------|------|--------|--------|------------|
| Low | qwen3:8b | qwen2.5-coder:7b | qwen2.5vl:3b | nomic-embed-text |
| Medium | qwen2.5:14b | deepseek-coder-v2:lite | qwen2.5vl:7b | bge-m3 |
| High | qwen2.5:32b | qwen3-coder:30b | qwen2.5vl:32b | bge-m3 |

## Безопасность

- Все сервисы на `127.0.0.1` только
- LiteLLM: API key auth (SOPS-encrypted)
- 6 firewall правил (inbound block)
- SOPS + age для секретов
- `.gitignore` исключает секреты, ключи, `.env`

## Структура проекта

```
ai/
├── .secrets.yaml          # SOPS-зашифрованные секреты (gitignored)
├── .sops.yaml             # SOPS config (age recipient)
├── .gitignore             # Исключения
├── .gitattributes         # Line endings + LFS
├── .python-version        # 3.10
├── pyproject.toml         # Зависимости
├── uv.lock                # Lockfile
├── mkdocs.yml             # MkDocs config
├── config/
│   ├── litellm/config.yaml  # Роутинг моделей
│   └── qdrant/qdrant.yaml   # Qdrant config
├── scripts/
│   ├── setup/             # start/stop скрипты
│   ├── monitoring/        # health-check, vram
│   ├── maintenance/       # update/cleanup models
│   ├── backup/            # backup
│   └── rag/               # RAG pipeline + agent
├── tests/                 # Security + inference тесты
├── docs/                  # MkDocs страницы
├── .vscode/settings.json  # VS Code config
└── .devcontainer/         # DevContainer config
```

## Документация

| Файл | Описание |
|------|----------|
| [Architecture.md](Architecture.md) | Архитектура системы |
| [DisasterRecovery.md](DisasterRecovery.md) | Восстановление без интернета |
| [Troubleshooting.md](Troubleshooting.md) | Решение проблем |
| [ROADMAP.md](ROADMAP.md) | План развития |
| [CHANGELOG.md](CHANGELOG.md) | История изменений |
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | Известные проблемы |

## Hardware

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen 7 7800X3D (8C/8T, 96MB 3D V-Cache) |
| RAM | 64GB DDR5 6400MHz |
| GPU | NVIDIA RTX 5070 (12GB VRAM) |
| Storage | Samsung 990 PRO 2TB NVMe + Seagate 4TB HDD |