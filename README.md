# AI Workstation

Локальная AI-станция для разработки ПО. Полностью локальная, без облачных API.

## Quick Start

Все сервисы запускаются **автоматически при входе в систему** (Task Scheduler: `AI-Workstation-AutoStart`).

Ручное управление:

`powershell
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
| Open WebUI | 127.0.0.1:8080 | Chat UI (Web) |
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



## Автозапуск

Все сервисы запускаются автоматически при входе в систему через Windows Task Scheduler.

**Задача:** \AI-Workstation-AutoStart\ (Trigger: AtLogOn)

\\powershell
# Проверить статус
Get-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Отключить автозапуск
Disable-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Включить обратно
Enable-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Запустить вручную
Start-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Удалить задачу
Unregister-ScheduledTask -TaskName 'AI-Workstation-AutoStart' -Confirm:\False
\
**Потребление в простое:** ~500 МБ — 1 ГБ RAM, 0% CPU, 0 VRAM.
Модели грузятся в VRAM только при запросе, выгружаются через 5 минут бездействия.




## Автозапуск

Все сервисы запускаются автоматически при входе в систему через Windows Task Scheduler.

**Задача:** `AI-Workstation-AutoStart` (Trigger: AtLogOn)

```powershell
# Проверить статус
Get-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Отключить автозапуск
Disable-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Включить обратно
Enable-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Запустить вручную
Start-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Удалить задачу
Unregister-ScheduledTask -TaskName 'AI-Workstation-AutoStart' -Confirm:$false
```

**Потребление в простое:** ~500 МБ — 1 ГБ RAM, 0% CPU, 0 VRAM.
Модели грузятся в VRAM только при запросе, выгружаются через 5 минут бездействия.






## Cline - Autonomous AI Agent (VS Code)

Cline - extension VS Code, autonomous AI agent for development. Works like AI assistant:
reads files, writes code, executes commands, does refactoring.

**Configured:**
- Provider: OpenAI Compatible (LiteLLM)
- Base URL: `http://127.0.0.1:4000/v1`
- Model: `coder-low` (qwen2.5-coder:7b)
- API Key: from SOPS

**Usage:**

1. Open VS Code
2. Click Cline icon on sidebar (or Ctrl+Shift+P -> Cline)
3. Open project folder (File -> Open Folder)
4. Write task in chat
5. Cline reads files, proposes changes, applies them
6. Confirm or reject each action

**Change model** in Cline settings:
- `coder-low` - qwen2.5-coder:7b (fast, default)
- `coder-medium` - deepseek-coder-v2:lite (more accurate)
- `coder-high` - qwen3-coder:30b (best quality, slow)

**Config:** `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_api_config.json`




## Cline - Autonomous AI Agent (VS Code)

Cline - extension VS Code, autonomous AI agent for development. Works like AI assistant:
reads files, writes code, executes commands, does refactoring.

**Configured:**
- Provider: OpenAI Compatible (LiteLLM)
- Base URL: `http://127.0.0.1:4000/v1`
- Model: `coder-low` (qwen2.5-coder:7b)
- API Key: from SOPS

**Usage:**

1. Open VS Code
2. Click Cline icon on sidebar (or Ctrl+Shift+P -> Cline)
3. Open project folder (File -> Open Folder)
4. Write task in chat
5. Cline reads files, proposes changes, applies them
6. Confirm or reject each action

**Change model** in Cline settings:
- `coder-low` - qwen2.5-coder:7b (fast, default)
- `coder-medium` - deepseek-coder-v2:lite (more accurate)
- `coder-high` - qwen3-coder:30b (best quality, slow)

**Config:** `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_api_config.json`


## Aider — AI Coding Agent

Aider — CLI-инструмент для AI-парного программирования. Работает с git-репозиториями,
читает файлы, пишет код, делает коммиты.

**Запуск:**

```powershell
# В терминале VS Code (откройте папку проекта):
D:\Projectsi\scripts\setupider.bat <файлы> --message "задача"

# Пример: добавить логирование
D:\Projectsi\scripts\setupider.bat main.py --message "Add logging to all functions"

# Рефакторинг
D:\Projectsi\scripts\setupider.bat src/ --message "Refactor: extract helper functions"

# Исправить баг
D:\Projectsi\scripts\setupider.bat bug.py --message "Fix: handle null pointer in parse function"
```

**Модели:**

| Алиас | Модель | Скорость | Качество |
|-------|--------|----------|----------|
| `coder-low` | qwen2.5-coder:7b | Быстро | Хорошо |
| `coder-medium` | deepseek-coder-v2:lite | Средне | Отлично |
| `coder-high` | qwen3-coder:30b | Медленно | Лучшее |

Сменить модель: `--model openai/coder-medium`

**Конфиг:** `.aider.conf.yml` (model, api-base, edit-format)


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