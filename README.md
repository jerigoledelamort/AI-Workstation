<div align="center">

# 🧠 Project Aegis

**Полностью локальная AI-станция для разработки ПО и реверс-инжиниринга.**

Без облака. Без API-ключей. Без телеметрии. Только твоё железо.

</div>

---

## 📋 Содержание

- [Быстрый старт](#-быстрый-старт)
- [Архитектура](#-архитектура)
- [Сервисы](#-сервисы)
- [Модели](#-модели-11-штук)
- [Cline — автономный агент](#-cline--автономный-агент)
- [Router — автороутинг моделей](#-router--автороутинг-моделей)
- [Obsidian — память проектов](#-obsidian--память-проектов)
- [GhidraMCP — реверс-инжиниринг](#-ghidramcp--реверс-инжиниринг)
- [Автозапуск](#-автозапуск)
- [Команды](#-команды)
- [Безопасность](#-безопасность)
- [Структура проекта](#-структура-проекта)
- [Hardware](#-hardware)
- [Документация](#-документация)

---

## 🚀 Быстрый старт

Все сервисы запускаются **автоматически при входе в Windows** (Task Scheduler).
Ничего писать не нужно. Просто открой VS Code и начни работать.

```powershell
# Проверить, что всё работает
.\scripts\monitoring\health-check.ps1

# Ручной запуск (если нужно)
.\scripts\setup\start-all.ps1

# Остановка
.\scripts\setup\stop-all.ps1
```

---

## 🏗 Архитектура

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Project Aegis                               │
│                                                                     │
│   ┌──────────┐    ┌─────────┐    ┌──────────┐    ┌───────────────┐  │
│   │  VS Code │───▶│ Router  │───▶│ LiteLLM  │───▶│    Ollama     │  │
│   │  Cline   │    │ :4001   │    │ Proxy    │    │    :11434     │  │
│   │  Aider   │    │ (auto)  │    │ :4000    │    │  11 моделей   │  │
│   └────┬─────┘    └─────────┘    └──────────┘    └───────────────┘  │
│        │                                                            │
│        │ MCP                                                        │
│        ▼                                                            │
│   ┌──────────┐    ┌─────────────────┐                               │
│   │ Ghidra   │───▶│ GhidraMCP Bridge│  Реверс-инжиниринг           │
│   │ :8080    │    │ :8081           │                               │
│   └──────────┘    └─────────────────┘                               │
│                                                                     │
│   ┌──────────┐    ┌─────────────────┐                               │
│   │  RAG     │───▶│     Qdrant      │  Векторная БД                │
│   │ Pipeline │    │  :6333 / :6334  │                               │
│   └──────────┘    └─────────────────┘                               │
│                                                                     │
│   ┌──────────┐                                                      │
│   │Open WebUI│  Chat UI (браузер)                                  │
│   │  :8080   │                                                      │
│   └──────────┘                                                      │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │  SOPS + age  →  .secrets.yaml (зашифрованные ключи)         │  │
│   └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

Все сервисы на `127.0.0.1`. Никаких внешних подключений.

---

## 📡 Сервисы

| Сервис | Порт | Назначение | Статус |
|--------|------|------------|--------|
| **Ollama** | `11434` | Inference-движок, 11 моделей (~97 ГБ) | ✅ Автозапуск |
| **LiteLLM Proxy** | `4000` | API-шлюз с авторизацией (OpenAI-совместимый) | ✅ Автозапуск |
| **Router Proxy** | `4001` | Автороутинг: сам выбирает модель по сложности задачи | ✅ Автозапуск |
| **Qdrant** | `6333` / `6334` | Векторная БД для RAG | ✅ Автозапуск |
| **Open WebUI** | `8080` | Web-интерфейс чата | ✅ Автозапуск |
| **GhidraMCP** | `8080` / `8081` | Ghidra HTTP + MCP Bridge | 🔧 По запросу |

---

## 🤖 Модели (11 штук)

3 профиля по нагрузке на VRAM (12 ГБ RTX 5070):

| Профиль | Chat | Coding | Vision | Embeddings |
|---------|------|--------|--------|------------|
| **Low** (быстро) | qwen3:8b | qwen2.5-coder:7b | qwen2.5vl:3b | nomic-embed-text |
| **Medium** (баланс) | qwen2.5:14b | deepseek-coder-v2:lite | qwen2.5vl:7b | bge-m3 |
| **High** (максимум) | qwen2.5:32b | qwen3-coder:30b | qwen2.5vl:32b | bge-m3 |

### Алиасы LiteLLM

| Алиас | Модель | Алиас | Модель |
|-------|-------|-------|-------|
| `chat-low` | qwen3:8b | `coder-low` | qwen2.5-coder:7b |
| `chat-medium` | qwen2.5:14b | `coder-medium` | deepseek-coder-v2:lite |
| `chat-high` | qwen2.5:32b | `coder-high` | qwen3-coder:30b |
| `vision-low` | qwen2.5vl:3b | `embed-low` | nomic-embed-text |
| `vision-medium` | qwen2.5vl:7b | `embed-medium` | bge-m3 |
| `vision-high` | qwen2.5vl:32b | `embed-high` | bge-m3 |

---

## 🧑‍💻 Cline — автономный агент

Cline — расширение VS Code. Работает как облачный AI-ассистент, но локально.

**Возможности:**
- 📖 Читает файлы проекта
- ✏️ Пишет и редактирует код
- 🖥 Выполняет команды в терминале
- 🌐 Работает с браузером
- 🔧 Использует MCP-инструменты (Ghidra, и др.)

**Настройка (уже выполнена):**

| Параметр | Значение |
|----------|----------|
| Провайдер | OpenAI Compatible |
| Base URL | `http://127.0.0.1:4001/v1` (через Router) |
| Plan-модель | `preset-heavy` (qwen3-coder:30b) |
| Act-модель | `preset-medium` (deepseek-coder-v2:lite) |
| Конфиг | `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\` |

**Режимы:**
- **Plan** — агент анализирует задачу, составляет план (тяжёлая модель)
- **Act** — агент выполняет план, пишет код (быстрая модель)

---

## 🧭 Router — автороутинг моделей

Прокси на порту `4001`. Анализирует сложность запроса и сам выбирает модель.

| Model ID | Что делает |
|----------|-----------|
| `auto` | **Авто-роутинг** — анализирует ключевые слова, размер контекста, код |
| `preset-light` | Всегда qwen2.5-coder:7b (быстро) |
| `preset-medium` | Всегда deepseek-coder-v2:lite (баланс) |
| `preset-heavy` | Всегда qwen3-coder:30b (максимум) |

**Как работает `auto`:**
- "refactor", "architecture", "rewrite" → `coder-high` (тяжёлая)
- "fix", "add", "implement" → `coder-medium` (средняя)
- "rename", "comment", "format" → `coder-low` (лёгкая)
- Большой контекст (>10K символов) → тяжесть вверх

Логи: `logs/router.log`

---

## 📓 Obsidian — память проектов

Каждый проект получает Obsidian-vault с автоматической структурой:

```
project/
├── .clinerules              ← Cline читает автоматически
└── .obsidian-memory/        ← Obsidian vault
    ├── README.md            ← Индекс
    ├── architecture/        ← Архитектура, диаграммы Mermaid
    ├── decisions/           ← ADR (Architecture Decision Records)
    ├── research/            ← Находки, анализ
    ├── rules/               ← Правила и конвенции
    ├── progress/            ← Лог работы агента
    ├── issues/              ← Баги, TODO
    ├── notes/               ← Заметки
    └── _templates/          ← Шаблоны
```

**Создание нового проекта:**

```powershell
python D:\Projects\ai\scripts\setup_helper.py D:\Projects\<имя_проекта>
```

Скрипт сам определит тип проекта (reverse, python, javascript, cpp, generic) и создаст нужную структуру. Cline может вызвать его сам по запросу: «Создай структуру проекта».

---

## 🔬 GhidraMCP — реверс-инжиниринг

Интеграция Ghidra с Cline через MCP. Агент может:

| Инструмент | Что делает |
|------------|-----------|
| `list_functions` | Список всех функций в бинарнике |
| `decompile_function` | Декомпилированный псевдокод |
| `disassemble_function` | Дизассемблированный код |
| `rename_function` | Переименовать функцию в Ghidra |
| `set_comment` | Добавить комментарий |
| `get_xrefs_to` | Перекрёстные ссылки на адрес |
| `list_strings` | Строки в бинарнике |

**Запуск:**

1. Открой бинарник в Ghidra (GhidraMCP HTTP сервер поднимется на `:8080`)
2. Запусти MCP Bridge:
   ```powershell
   Start-Process 'D:\Projects\ai\scripts\setup\start-ghidra-mcp.bat' -WindowStyle Hidden
   ```
3. В Cline: «Проанализируй бинарник в Ghidra, работай автономно»

**Для ночной работы:** включи авто-апрув на чтение/правку файлов. Агент будет декомпилировать, переименовывать, комментировать и записывать находки в `.obsidian-memory/research/`.

---

## ⏰ Автозапуск

Task Scheduler задача `AI-Workstation-AutoStart` запускает все сервисы при входе в Windows.

```powershell
# Проверить статус
Get-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Отключить
Disable-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Включить
Enable-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Запустить вручную
Start-ScheduledTask -TaskName 'AI-Workstation-AutoStart'

# Удалить
Unregister-ScheduledTask -TaskName 'AI-Workstation-AutoStart' -Confirm:$false
```

**Потребление в простое:** ~500 МБ — 1 ГБ RAM, 0% CPU, 0 VRAM.
Модели грузятся в VRAM только при запросе, выгружаются через 5 минут бездействия.

---

## 🛠 Команды

| Команда | Описание |
|---------|----------|
| `.\scripts\setup\start-all.ps1` | Запуск всех сервисов |
| `.\scripts\setup\stop-all.ps1` | Остановка всех сервисов |
| `.\scripts\monitoring\health-check.ps1` | Health check всех сервисов |
| `.\scripts\monitoring\vram-check.ps1` | Мониторинг VRAM / RAM |
| `.\scripts\maintenance\update-models.ps1` | Обновление моделей Ollama |
| `.\scripts\maintenance\cleanup-models.ps1` | Список моделей для очистки |
| `.\scripts\backup\backup.ps1` | Резервное копирование конфигов |
| `.\tests\test-security.ps1` | Аудит безопасности (10 проверок) |
| `.	ests	est-inference.ps1` | Тест inference всех моделей |

### RAG

```powershell
# Загрузить документ в Qdrant
.venv\Scripts\python.exe scripts\rag\rag_pipeline.py ingest <file_path>

# Запрос по документам
.venv\Scripts\python.exe scripts\rag\rag_pipeline.py query "question"

# Агент с tool calling
.venv\Scripts\python.exe scripts\rag\agent_workflow.py "question"
```

### Aider (CLI-агент)

```powershell
D:\Projects\ai\scripts\setup\aider.bat <файлы> --message "задача"
```

---

## 🔒 Безопасность

| Слой | Реализация |
|------|-----------|
| **Сеть** | Все сервисы на `127.0.0.1` только |
| **Firewall** | 6 inbound block правил (11434, 4000, 4001, 6333, 6334, 8080) |
| **API auth** | LiteLLM `master_key` (SOPS-зашифрованный) |
| **Секреты** | SOPS 3.13.2 + age 1.3.1, `.secrets.yaml` |
| **Git** | `.gitignore` исключает секреты, ключи, `.env`, venv |

Аудит: `.\tests\test-security.ps1` → 10/10 PASS

---

## 📁 Структура проекта

```
ai/
├── .clinerules                 # Глобальные правила для Cline
├── .aider.conf.yml             # Конфиг Aider
├── .secrets.yaml               # SOPS-зашифрованные секреты (gitignored)
├── .sops.yaml                  # SOPS config (age recipient)
├── .gitignore / .gitattributes
├── .python-version             # 3.10
├── pyproject.toml / uv.lock    # Зависимости
│
├── config/
│   ├── litellm/config.yaml     # Роутинг 11 моделей
│   └── qdrant/qdrant.yaml      # Qdrant config
│
├── scripts/
│   ├── setup_helper.py         # Авто-создание проектов (Obsidian vault)
│   ├── ai/router_proxy.py      # Router Proxy (автороутинг моделей)
│   ├── setup/                  # start/stop скрипты, aider, ghidra-mcp
│   ├── monitoring/             # health-check, vram
│   ├── maintenance/            # update/cleanup models
│   ├── backup/                 # backup
│   ├── rag/                    # RAG pipeline + agent
│   └── obsidian/               # Obsidian vault generator
│
├── tools/
│   └── ghidramcp/              # GhidraMCP plugin + bridge
│
├── tests/                      # Security + inference тесты
├── data/                       # Qdrant, Open WebUI data (gitignored)
├── logs/                       # Логи сервисов (gitignored)
└── backup/                     # Резервные копии (gitignored)
```

---

## 💻 Hardware

| Компонент | Спецификация |
|-----------|-------------|
| **CPU** | AMD Ryzen 7 7800X3D (8C/8T, 96MB 3D V-Cache) |
| **RAM** | 64GB DDR5 6400MHz |
| **GPU** | NVIDIA RTX 5070 (12GB VRAM) |
| **Storage** | Samsung 990 PRO 2TB NVMe + Seagate 4TB HDD |

---

## 📚 Документация

| Документ | Описание |
|----------|----------|
| [Architecture.md](Architecture.md) | Подробная архитектура всех компонентов |
| [DisasterRecovery.md](DisasterRecovery.md) | Восстановление с нуля без интернета |
| [Troubleshooting.md](Troubleshooting.md) | Решение проблем |
| [ROADMAP.md](ROADMAP.md) | План развития |
| [CHANGELOG.md](CHANGELOG.md) | История изменений |
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | Известные проблемы |

---

<div align="center">

**GitHub:** [jerigoledelamort/AI-Workstation](https://github.com/jerigoledelamort/AI-Workstation)

</div>
