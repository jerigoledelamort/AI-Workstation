# Roadmap — план реализации

> Основание: Requirements.md, AI-Workstation.md, Architecture.md.
> Принцип: поэтапная реализация с тестированием после каждой фазы.

---

## Обзор фаз

| Фаза | Название | Длительность (оценка) | Зависимости | Опасные действия |
|------|----------|-----------------------|-------------|------------------|
| 1 | Структура проекта | 15 мин | — | Нет |
| 2 | Базовая инфраструктура | 30-60 мин | Фаза 1 | Установка ПО |
| 3 | AI inference слой | 30-90 мин | Фаза 2 | Загрузка моделей (~25 ГБ) |
| 4 | Среда разработки | 30 мин | Фаза 2 | Нет |
| 5 | Безопасность | 30 мин | Фаза 1, 3 | Firewall правила |
| 6 | RAG и агентность | 60 мин | Фаза 3, 4 | Нет |
| 7 | Автоматизация | 45 мин | Фаза 3, 6 | Нет |
| 8 | Документация | 45 мин | Все фазы | Нет |
| 9 | Тесты и аудит | 30 мин | Все фазы | Нет |

**Общая оценка: 5-7 часов** (без ограничений по времени).

---

## Фаза 1: Структура проекта

### Цель
Создать скелет репозитория с директориями, .gitignore, базовыми конфигами.

### Шаги

| # | Действие | Результат |
|---|----------|-----------|
| 1.1 | Создать структуру директорий | `config/`, `scripts/`, `docs/`, `data/`, `tests/` |
| 1.2 | Инициализировать git | `git init` + `.gitignore` |
| 1.3 | Создать `.gitignore` | Исключения: `data/`, `.env`, `*.key`, `__pycache__/` |
| 1.4 | Создать базовый `README.md` | Описание проекта, ссылки на доки |
| 1.5 | Коммит структуры | Первый commit |

### Структура

```
D:\Projects\ai\
├── config/              # Конфигурации сервисов
│   ├── ollama/          # Ollama env, Modelfiles
│   ├── litellm/         # LiteLLM config
│   ├── docker/          # docker-compose.yml
│   └── vscode/          # VS Code settings
├── scripts/             # Скрипты автоматизации
│   ├── setup/           # Установка и настройка
│   ├── maintenance/     # Обслуживание
│   ├── monitoring/      # Health checks
│   └── backup/          # Резервное копирование
├── docs/                # Документация (MkDocs)
│   ├── index.md
│   ├── architecture.md
│   ├── setup-guide.md
│   ├── runbook.md
│   └── security.md
├── data/                # Данные сервисов (gitignored)
│   ├── qdrant/
│   └── open-webui/
├── tests/               # Тесты и проверки
│   ├── test-inference.ps1
│   ├── test-rag.ps1
│   └── test-security.ps1
├── .sops.yaml           # SOPS конфиг
├── secrets.enc.yaml     # Зашифрованные секреты
├── pyproject.toml       # Python проект (uv)
├── mkdocs.yml           # MkDocs конфиг
├── Requirements.md
├── AI-Workstation.md
├── Architecture.md
├── Roadmap.md
└── TechnologyDecisionRecord.md
```

### Критерии завершения
- [ ] Директории созданы
- [ ] Git инициализирован
- [ ] .gitignore настроен
- [ ] Первый коммит

---

## Фаза 2: Базовая инфраструктура

### Цель
Установить недостающие инструменты: uv, Node.js, SOPS, age, LiteLLM, MkDocs.

### Шаги

| # | Действие | Команда | Результат |
|---|----------|---------|-----------|
| 2.1 | Установить uv | `pip install uv` | uv доступен |
| 2.2 | Установить Node.js LTS | Через nvm-windows | node + npm доступны |
| 2.3 | Установить SOPS | `choco install sops` или ручная установка | sops доступен |
| 2.4 | Установить age | `choco install age` или ручная установка | age доступен |
| 2.5 | Создать age keypair | `age-keygen -o keys.txt` | Приватный ключ |
| 2.6 | Настроить SOPS | `.sops.yaml` с age recipient | SOPS работает |
| 2.7 | Создать Python venv (uv) | `uv venv` + `uv pip install litellm mkdocs-material` | Окружение |
| 2.8 | Проверить установки | Версии всех инструментов | Все доступны |

### Критерии завершения
- [ ] uv установлен и работает
- [ ] Node.js LTS установлен
- [ ] SOPS + age установлены, keypair создан
- [ ] Python venv создан с LiteLLM и MkDocs
- [ ] Все версии проверены

---

## Фаза 3: AI inference слой

### Цель
Настроить Ollama, загрузить модели всех профилей, запустить LiteLLM Proxy.

### Шаги

| # | Действие | Команда / Действие | Результат |
|---|----------|---------------------|-----------|
| 3.1 | Настроить Ollama env | OLLAMA_HOST=127.0.0.1:11434 | Ollama на localhost |
| 3.2 | Загрузить Low VRAM модели | `ollama pull qwen2.5-coder:7b` + `ollama pull nomic-embed-text` + `ollama pull qwen2.5vl:3b` | 3 модели |
| 3.3 | Загрузить Medium VRAM модели | `ollama pull qwen2.5:14b` + `ollama pull deepseek-coder-v2` + `ollama pull qwen2.5vl:7b` + `ollama pull bge-m3` | 4 модели |
| 3.4 | Загрузить High VRAM модели | `ollama pull qwen3-coder:30b-a3b` + `ollama pull qwen2.5:32b` + `ollama pull qwen2.5vl:32b` | 3 модели |
| 3.5 | Создать LiteLLM config | `config/litellm/config.yaml` | Конфиг с routing |
| 3.6 | Создать секреты | SOPS encrypt API keys | secrets.enc.yaml |
| 3.7 | Запустить LiteLLM Proxy | `litellm --config config/litellm/config.yaml` | API на :4000 |
| 3.8 | Тест inference | Запрос через LiteLLM к каждой модели | Все отвечают |

### Объём загрузок

| Профиль | Модели | Объём |
|---------|--------|-------|
| Low | qwen2.5-coder:7b, nomic-embed-text, qwen2.5vl:3b | ~8 ГБ |
| Medium | qwen2.5:14b, deepseek-coder-v2, qwen2.5vl:7b, bge-m3 | ~25 ГБ |
| High | qwen3-coder:30b-a3b, qwen2.5:32b, qwen2.5vl:32b | ~60 ГБ |
| **Итого** | 10 моделей (+ qwen3:8b уже есть) | **~93 ГБ** |

### Критерии завершения
- [ ] Ollama настроен на localhost
- [ ] Все модели загружены
- [ ] LiteLLM Proxy запущен с auth
- [ ] Inference тест пройден для всех моделей

---

## Фаза 4: Среда разработки

### Цель
Настроить VS Code, DevContainers, расширения.

### Шаги

| # | Действие | Результат |
|---|----------|-----------|
| 4.1 | Установить расширение Dev Containers | Расширение в VS Code |
| 4.2 | Установить расширение Continue | MCP-клиент |
| 4.3 | Создать devcontainer.json | Базовый контейнер с Python 3.12 + uv |
| 4.4 | Настроить Continue (config.json) | Подключение к LiteLLM |
| 4.5 | Настроить VS Code settings.json | Форматирование, линтер, AI |
| 4.6 | Тест DevContainer | Открыть проект в контейнере |

### Критерии завершения
- [ ] DevContainers работает
- [ ] Continue подключён к LiteLLM
- [ ] VS Code настроен

---

## Фаза 5: Безопасность

### Цель
Настроить firewall, проверить изоляцию, протестировать auth.

### Шаги

| # | Действие | Результат |
|---|----------|-----------|
| 5.1 | Настроить Windows Firewall | Block inbound на все порты сервисов |
| 5.2 | Проверить localhost-only | Сервисы не доступны извне |
| 5.3 | Тест LiteLLM auth | Запрос без API key отклонён |
| 5.4 | Тест Qdrant auth | Запрос без API key отклонён |
| 5.5 | Проверить SOPS | Расшифровка работает, ключ в безопасности |
| 5.6 | Проверить .gitignore | .env, keys.txt исключены |
| 5.7 | Security audit script | `tests/test-security.ps1` |

### Критерии завершения
- [ ] Firewall правила активны
- [ ] Все сервисы localhost-only
- [ ] Auth работает на LiteLLM и Qdrant
- [ ] Секреты зашифрованы (SOPS)
- [ ] .gitignore корректен
- [ ] Security audit пройден

---

## Фаза 6: RAG и агентность

### Цель
Развернуть Qdrant, Open WebUI, RAG pipeline, агентный framework.

### Шаги

| # | Действие | Результат |
|---|----------|-----------|
| 6.1 | Создать docker-compose.yml | Qdrant + Open WebUI |
| 6.2 | Запустить Docker сервисы | `docker compose up -d` |
| 6.3 | Настроить Open WebUI | Подключение к Ollama, auth |
| 6.4 | Создать RAG pipeline скрипт | LangChain + Qdrant + Ollama |
| 6.5 | Тест RAG | Запрос по документации |
| 6.6 | Установить LangGraph | `uv pip install langgraph` |
| 6.7 | Создать агентный workflow | Базовый агент с tool calling |
| 6.8 | Тест агентности | Многошаговая задача |

### Критерии завершения
- [ ] Qdrant запущен и доступен
- [ ] Open WebUI работает с Ollama
- [ ] RAG pipeline функционален
- [ ] Агентный workflow работает

---

## Фаза 7: Автоматизация

### Цель
Создать скрипты обслуживания, мониторинга, бэкапа.

### Шаги

| # | Действие | Скрипт | Результат |
|---|----------|--------|-----------|
| 7.1 | Health check скрипт | `scripts/monitoring/health-check.ps1` | Проверка всех сервисов |
| 7.2 | VRAM monitor | `scripts/monitoring/vram-check.ps1` | Мониторинг VRAM/RAM |
| 7.3 | Model update скрипт | `scripts/maintenance/update-models.ps1` | Обновление моделей |
| 7.4 | Model cleanup скрипт | `scripts/maintenance/cleanup-models.ps1` | Удаление неиспользуемых |
| 7.5 | Backup скрипт | `scripts/backup/backup.ps1` | Бэкап Qdrant + Open WebUI |
| 7.6 | Start all скрипт | `scripts/setup/start-all.ps1` | Запуск всех сервисов |
| 7.7 | Stop all скрипт | `scripts/setup/stop-all.ps1` | Остановка всех сервисов |
| 7.8 | Scheduled task | Windows Task Scheduler | Еженедельные бэкапы |

### Критерии завершения
- [ ] Все скрипты созданы и работают
- [ ] Health check проходит
- [ ] Backup работает
- [ ] Start/Stop скрипты работают
- [ ] Scheduled task настроена

---

## Фаза 8: Документация

### Цель
Создать полную документацию в MkDocs.

### Шаги

| # | Действие | Документ | Результат |
|---|----------|----------|-----------|
| 8.1 | Настроить MkDocs | `mkdocs.yml` | Конфиг Material theme |
| 8.2 | Создать index.md | Главная страница | Обзор станции |
| 8.3 | Создать setup-guide.md | Руководство установки | Пошаговая установка |
| 8.4 | Создать runbook.md | Operational runbook | Процедуры обслуживания |
| 8.5 | Создать security.md | Security guide | Политика безопасности |
| 8.6 | Перенести существующие доки | Architecture, AI-Workstation и др. | В docs/ |
| 8.7 | Собрать MkDocs | `mkdocs build` | Статический сайт |
| 8.8 | Тест рендеринга | `mkdocs serve` | Проверка на :8000 |

### Критерии завершения
- [ ] MkDocs настроен
- [ ] Все документы созданы
- [ ] MkDocs собирается без ошибок
- [ ] Документация доступна на localhost:8000

---

## Фаза 9: Тесты и финальный аудит

### Цель
Провести комплексное тестирование всех компонентов и финальный аудит.

### Шаги

| # | Действие | Тест | Результат |
|---|----------|------|-----------|
| 9.1 | Тест inference | `tests/test-inference.ps1` | Все модели отвечают через LiteLLM |
| 9.2 | Тест RAG | `tests/test-rag.ps1` | RAG pipeline работает |
| 9.3 | Тест безопасности | `tests/test-security.ps1` | Auth, firewall, secrets |
| 9.4 | Тест Docker | `tests/test-docker.ps1` | Все контейнеры здоровы |
| 9.5 | Тест автоматизации | `tests/test-automation.ps1` | Скрипты работают |
| 9.6 | Тест восстановления | Симуляция сбоя | Восстановление < 5 мин |
| 9.7 | Финальный аудит | Чек-лист | Все критерии пройдены |

### Финальный чек-лист аудита

| # | Критерий | Статус |
|---|----------|--------|
| 1 | Все сервисы запущены и отвечают | ☐ |
| 2 | Все сервисы localhost-only | ☐ |
| 3 | Firewall правила активны | ☐ |
| 4 | API auth работает (LiteLLM, Qdrant) | ☐ |
| 5 | Секреты зашифрованы (SOPS+age) | ☐ |
| 6 | Модели всех профилей загружены | ☐ |
| 7 | Inference работает через LiteLLM | ☐ |
| 8 | RAG pipeline функционален | ☐ |
| 9 | Vision pipeline функционален | ☐ |
| 10 | DevContainers работают | ☐ |
| 11 | MCP/Continue подключён | ☐ |
| 12 | Open WebUI работает | ☐ |
| 13 | Скрипты обслуживания работают | ☐ |
| 14 | Backup работает | ☐ |
| 15 | Документация полная и собрана | ☐ |
| 16 | Все тесты пройдены | ☐ |

### Критерии завершения
- [ ] Все тесты пройдены
- [ ] Финальный чек-лист заполнен
- [ ] Документация полная
- [ ] Автоматизация работает

---

## Зависимости между фазами

```
Фаза 1 (Структура)
  │
  ├──► Фаза 2 (Инфраструктура)
  │      │
  │      ├──► Фаза 3 (AI inference)
  │      │      │
  │      │      ├──► Фаза 5 (Безопасность)
  │      │      ├──► Фаза 6 (RAG + Agent)
  │      │      │      │
  │      │      │      └──► Фаза 7 (Автоматизация)
  │      │      │               │
  │      ├──► Фаза 4 (Dev Env)  │
  │      │      │               │
  │      │      └───────────────┤
  │      │                      │
  │      └──────────────────────┴──► Фаза 8 (Документация)
  │                                      │
  └──────────────────────────────────────► Фаза 9 (Тесты + Аудит)
```

---

*Документ основан на Requirements.md, AI-Workstation.md, Architecture.md.
Дата: 2026-07-17.*
