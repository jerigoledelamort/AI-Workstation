# Architecture — системная архитектура

> Основание: Requirements.md, AI-Workstation.md.
> Принципы: безопасность #1, воспроизводимость #2, исключительно локально.

---

## 1. Обзор архитектуры

```
┌─────────────────────────────────────────────────────────────┐
│                    Windows 11 Home                           │
│                                                             │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │   VS Code       │    │       PowerShell             │   │
│  │  + Koda         │    │   (automation, monitoring)    │   │
│  │  + Continue     │    │                               │   │
│  │  + DevContainers│    │                               │   │
│  └────────┬────────┘    └──────────────────────────────┘   │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │  LiteLLM Proxy  │◄──►│         Ollama               │   │
│  │  (API Gateway)   │    │   (Inference Engine)         │   │
│  │  localhost:4000  │    │   localhost:11434            │   │
│  │  + API key auth  │    │   GPU: RTX 5070 (12 GB)     │   │
│  └────────┬────────┘    └──────────────────────────────┘   │
│           │                                                  │
│           ▼                                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Docker Desktop (WSL2)                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │  │
│  │  │ Qdrant   │  │ Open WebUI│  │  DevContainers    │  │  │
│  │  │ (vector) │  │  (chat)  │  │  (isolated dev)   │  │  │
│  │  └──────────┘  └──────────┘  └───────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Python (uv-managed)                      │  │
│  │  LangChain | LangGraph | RAG pipeline | Scripts      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Secrets (SOPS + age)                     │  │
│  │  Encrypted configs in git                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Сетевая топология

### 2.1. Порты и сервисы

| Сервис | Порт | Интерфейс | Auth | Назначение |
|--------|------|-----------|------|------------|
| Ollama | 11434 | localhost ONLY | ❌ (нет) | Inference API (GGUF) |
| LiteLLM Proxy | 4000 | localhost ONLY | ✅ (API key) | Unified OpenAI-совместимый API |
| Open WebUI | 8080 | localhost ONLY | ✅ (login) | Web UI для чата |
| Qdrant | 6333 | localhost ONLY | ✅ (API key) | Vector DB REST API |
| Qdrant gRPC | 6334 | localhost ONLY | ✅ (API key) | Vector DB gRPC |
| MkDocs | 8000 | localhost ONLY | ❌ | Документация (dev server) |

### 2.2. Принцип изоляции сети

```
Интернет ──✕──► Локальные сервисы (нет внешнего доступа)

Все сервисы слушают ТОЛЬКО на 127.0.0.1 / localhost.
Никаких привязок к 0.0.0.0 или внешним интерфейсам.

Ollama: OLLAMA_HOST=127.0.0.1:11434
LiteLLM: --host 127.0.0.1 --port 4000
Open WebUI: --env HOST=127.0.0.1
Qdrant: --env QDRANT__SERVICE__HOST=127.0.0.1
```

### 2.3. Firewall правила (Windows Defender Firewall)

| Правило | Действие | Назначение |
|---------|----------|------------|
| Block inbound on 11434 | Deny | Ollama не доступен извне |
| Block inbound on 4000 | Deny | LiteLLM не доступен извне |
| Block inbound on 8080 | Deny | Open WebUI не доступен извне |
| Block inbound on 6333-6334 | Deny | Qdrant не доступен извне |

---

## 3. Уровни безопасности

### 3.1. Многоуровневая модель защиты

```
┌─────────────────────────────────────────────────┐
│ Уровень 5: Физический (доступ к машине)         │
├─────────────────────────────────────────────────┤
│ Уровень 4: ОС (Windows Hello, BitLocker?)       │
├─────────────────────────────────────────────────┤
│ Уровень 3: Сеть (localhost-only, firewall)      │
├─────────────────────────────────────────────────┤
│ Уровень 2: API (LiteLLM auth, API keys)         │
├─────────────────────────────────────────────────┤
│ Уровень 1: Данные (SOPS+age, .env isolation)    │
└─────────────────────────────────────────────────┘
```

### 3.2. Управление секретами

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  age keypair │────►│  SOPS encrypt│────►│  git commit  │
│  (local)     │     │  secrets.yaml│     │  (encrypted) │
└──────────────┘     └──────────────┘     └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  SOPS decrypt│────► .env (local, gitignored)
                    │  at runtime  │
                    └──────────────┘
```

| Секрет | Хранение | Доступ |
|--------|----------|--------|
| LiteLLM API key | SOPS-encrypted в git | Расшифровывается при старте |
| Qdrant API key | SOPS-encrypted в git | Расшифровывается при старте |
| age private key | ~/.config/sops/age/keys.txt (НЕ в git) | Локальный файл |
| Ollama | Без auth (localhost-only) | Только через LiteLLM |

### 3.3. Изоляция сред разработки

```
┌─────────────────────────────────────────────────┐
│                  Host (Windows)                  │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  DevContainer (Docker + WSL2)           │   │
│  │  ├── Python 3.12 + uv                   │   │
│  │  ├── LangChain, LangGraph               │   │
│  │  ├── Доступ к Ollama (host.docker)      │   │
│  │  └── Изолированные зависимости          │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  Host Python (uv venv)                  │   │
│  │  ├── LiteLLM, скрипты обслуживания      │   │
│  │  └── Доступ ко всем сервисам            │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 4. Поток данных

### 4.1. Inference pipeline (базовый)

```
Пользователь (VS Code / Open WebUI / CLI)
    │
    ▼
LiteLLM Proxy (localhost:4000)
    │  ── auth: API key
    │  ── routing: выбор модели по сценарию
    │  ── logging: запрос + ответ
    ▼
Ollama (localhost:11434)
    │  ── загрузка модели в VRAM (если не загружена)
    │  ── GPU inference (RTX 5070)
    │  ── CPU offload (при нехватке VRAM)
    ▼
Ответ → LiteLLM → Пользователь
```

### 4.2. RAG pipeline

```
Документы / Код
    │
    ▼
Chunking (LangChain text splitters)
    │
    ▼
Embeddings (Ollama: nomic-embed-text / bge-m3)
    │
    ▼
Qdrant (localhost:6333)
    │  ── хранение векторов + metadata
    │
    ▼
Query → Embed query → Qdrant search (top-k)
    │
    ▼
Augmented prompt (context + query)
    │
    ▼
LiteLLM → Ollama → Generate answer
```

### 4.3. Agent pipeline

```
Пользователь (задача)
    │
    ▼
LangGraph (agent workflow)
    │  ── state management
    │  ── tool calling
    │
    ├──► Ollama (inference: qwen3-coder:30b-a3b)
    ├──► File system (через MCP / tools)
    ├──► Git (через tools)
    ├──► Terminal (через tools, изолированно)
    ├──► Qdrant (RAG retrieval)
    │
    ▼
Результат (код / документация / анализ)
```

### 4.4. Vision pipeline

```
Изображение (PNG/JPG)
    │
    ▼
Open WebUI / LiteLLM
    │
    ▼
Ollama (qwen2.5vl:7b / qwen2.5vl:32b)
    │  ── vision encoder + LLM
    ▼
Текстовый ответ (OCR / анализ / описание)
```

---

## 5. Управление ресурсами

### 5.1. VRAM стратегия

```
┌─────────────────────────────────────────────────┐
│           RTX 5070 — 12 ГБ VRAM                 │
│                                                 │
│  Сценарий A (интерактив):                       │
│  ┌────────────────────────────────────┐         │
│  │  Model: 5 ГБ  │  Context: 2 ГБ     │         │
│  │  (qwen3:8b)   │  (32K tokens)      │         │
│  └────────────────────────────────────┘         │
│  Свободно: ~5 ГБ                                │
│                                                 │
│  Сценарий B (качество + offload):               │
│  ┌────────────────────────────────────┐         │
│  │  VRAM: 12 ГБ  │  RAM: 7 ГБ (offload)│        │
│  │  (qwen3-coder:30b-a3b, 19 ГБ)      │         │
│  └────────────────────────────────────┘         │
│  Свободно: 0 ГБ VRAM                            │
│                                                 │
│  Сценарий C (RAG):                              │
│  ┌────────────────────────────────────┐         │
│  │  Embed: 0.3 ГБ │  Gen: 5 ГБ        │         │
│  │  (nomic)       │  (qwen3:8b)       │         │
│  └────────────────────────────────────┘         │
│  Свободно: ~6.7 ГБ                              │
└─────────────────────────────────────────────────┘
```

### 5.2. RAM стратегия

| Компонент | RAM | Условие |
|-----------|-----|---------|
| Ollama (runtime) | 1-2 ГБ | Постоянно |
| Docker Desktop + WSL2 | 4-8 ГБ | Постоянно |
| Qdrant | 1-2 ГБ | Постоянно |
| Open WebUI | 0.5-1 ГБ | По необходимости |
| VS Code | 1-2 ГБ | Постоянно |
| LiteLLM | 0.2-0.5 ГБ | Постоянно |
| CPU offload (модели) | 0-15 ГБ | При больших моделях |
| **Итого базово** | ~10-15 ГБ | |
| **Доступно для offload** | ~45-50 ГБ | |

### 5.5. Дисковая стратегия

| Диск | Содержимое | Причина |
|------|-----------|---------|
| C: (NVMe) | ОС, Docker, Ollama модели, Python envs, инструменты | Скорость загрузки моделей в VRAM |
| D: (HDD) | Проекты, бэкапы, датасеты, архивы | Объём, не критична скорость |
| D:\Projects\ai | Репозиторий AI Workstation (конфиги, скрипты, доки) | Проекты на HDD |

**Ollama модели на NVMe:**
```
OLLAMA_MODELS=C:\Users\egork\.ollama\models (на NVMe по умолчанию)
```

---

## 6. Жизненный цикл моделей

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Pull    │───►│  Load    │───►│  Serve   │───►│  Unload  │
│ (download│    │ (VRAM +  │    │ (inference│    │ (free    │
│  to NVMe)│    │  RAM)    │    │  requests)│    │  VRAM)   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │                                                │
     │           ┌──────────┐                         │
     └──────────►│  Update  │◄────────────────────────┘
                 │ (re-pull)│
                 └──────────┘
                      │
                 ┌──────────┐
                 │  Remove  │
                 │ (rm)     │
                 └──────────┘
```

| Этап | Команда | Триггер |
|------|---------|---------|
| Pull | `ollama pull <model>` | Установка / обновление |
| Load | Автоматически при первом запросе | Запрос через API |
| Serve | Ollama держит модель в VRAM | Пока активна |
| Unload | `ollama stop <model>` или таймаут | Неиспользование / нехватка VRAM |
| Update | `ollama pull <model>` (обновляет digest) | Скрипт обслуживания |
| Remove | `ollama rm <model>` | Очистка / смена модели |

---

## 7. Конфигурация сервисов

### 7.1. Ollama

```env
OLLAMA_HOST=127.0.0.1:11434
OLLAMA_MODELS=C:\Users\egork\.ollama\models
OLLAMA_KEEP_ALIVE=10m
OLLAMA_NUM_PARALLEL=1
OLLAMA_MAX_LOADED_MODELS=2
```

### 7.2. LiteLLM Proxy

```yaml
# litellm_config.yaml
model_list:
  - model_name: chat-fast
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://127.0.0.1:11434
  - model_name: chat-quality
    litellm_params:
      model: ollama/qwen2.5:32b
      api_base: http://127.0.0.1:11434
  - model_name: coder-fast
    litellm_params:
      model: ollama/qwen2.5-coder:7b
      api_base: http://127.0.0.1:11434
  - model_name: coder-quality
    litellm_params:
      model: ollama/qwen3-coder:30b-a3b
      api_base: http://127.0.0.1:11434
  - model_name: vision
    litellm_params:
      model: ollama/qwen2.5vl:7b
      api_base: http://127.0.0.1:11434
  - model_name: embeddings
    litellm_params:
      model: ollama/nomic-embed-text
      api_base: http://127.0.0.1:11434

litellm_settings:
  drop_params: true
  request_timeout: 300

general_settings:
  master_key: sk-litellm-<SOPS_ENCRYPTED>
```

### 7.3. Docker Compose (сервисы)

```yaml
# docker-compose.yml (структура)
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports: ["127.0.0.1:6333:6333", "127.0.0.1:6334:6334"]
    volumes: ["./data/qdrant:/qdrant/storage"]
    environment:
      QDRANT__SERVICE__HOST: "127.0.0.1"

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports: ["127.0.0.1:8080:8080"]
    environment:
      OLLAMA_BASE_URL: "http://host.docker.internal:11434"
      HOST: "127.0.0.1"
    volumes: ["./data/open-webui:/app/backend/data"]
    depends_on: [qdrant]
```

---

## 8. Стратегия восстановления

### 8.1. Компоненты и их восстановление

| Компонент | Время восстановления | Метод |
|-----------|---------------------|-------|
| Ollama | <1 мин | Перезапуск сервиса |
| LiteLLM | <30 сек | Перезапуск процесса |
| Qdrant | <1 мин | Docker restart (данные в volume) |
| Open WebUI | <1 мин | Docker restart |
| Модели | <5 мин | `ollama pull` из кэша или репозитория |
| Конфиги | <1 мин | `git checkout` из репозитория |
| Секреты | <1 мин | SOPS decrypt из git + age key |

### 8.2. Backup стратегия

| Что | Где | Частота | Метод |
|-----|-----|---------|-------|
| Конфиги + скрипты + доки | D:\Projects\ai (git) | На каждое изменение | git commit + push (local/remote) |
| Qdrant data | ./data/qdrant | Еженедельно | robocopy на D: |
| Open WebUI data | ./data/open-webui | Еженедельно | robocopy на D: |
| age key | ~/.config/sops/age/ | Однократно + при ротации | Ручное копирование на безопасный носитель |
| Ollama models | ~/.ollama/models | При установке новых | Список моделей в git, pull при восстановлении |

---

*Документ основан на Requirements.md и AI-Workstation.md.
Дата: 2026-07-17.*
