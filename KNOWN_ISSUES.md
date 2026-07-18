# Known Issues

## 1. langchain-community Deprecation Warning

**Симптом:** `DeprecationWarning: langchain-community is being sunset`

**Причина:** `langchain-community` устарел, пакеты переносятся в отдельные интеграции.

**Решение:** Использовать `langchain-ollama` и `langchain-qdrant` вместо `langchain-community`. В `rag_pipeline.py` остался импорт `TextLoader` из `langchain_community` — предупреждение не критично.

**Статус:** Non-blocking. Функциональность работает.

---

## 2. LangGraph create_react_agent Deprecation

**Симптом:** `LangGraphDeprecatedSinceV10: create_react_agent has been moved to langchain.agents`

**Причина:** LangGraph v1.0 перенёс `create_react_agent` в `langchain.agents`.

**Решение:** Обновить импорт на `from langchain.agents import create_agent` в будущих версиях.

**Статус:** Non-blocking. Агент работает.

---

## 3. Qdrant Config File Warning

**Симптом:** `WARN qdrant::settings: Config file not found: config/config`

**Причина:** Qdrant ищет дефолтные config файлы в `config/` относительно CWD.

**Решение:** Не критично. Qdrant использует наш `--config-path` + дефолты.

**Статус:** Non-blocking.

---

## 4. Qdrant Filesystem Warning

**Симптом:** `WARN qdrant: There is a potential issue with the filesystem for storage path ./storage. Filesystem type check is not supported on this platform`

**Причина:** Qdrant не может проверить тип ФС на Windows.

**Решение:** Не требуется. Работает корректно на NTFS.

**Статус:** Non-blocking.

---

## 5. Qdrant Web UI Not Available

**Симптом:** `WARN qdrant::actix::web_ui: Static content folder for Web UI './static' does not exist`

**Причина:** Бинарник Qdrant не включает static файлы Web UI.

**Решение:** Web UI недоступен. Использовать REST API напрямую.

**Статус:** Non-blocking. API работает.

---

## 6. uv Hardlink Warning

**Симптом:** `warning: Failed to hardlink files; falling back to full copy`

**Причина:** Cache uv и target директория на разных файловых системах.

**Решение:** `set UV_LINK_MODE=copy` или игнорировать.

**Статус:** Non-blocking.

---

## 7. Python pip Not Available

**Симптом:** `No module named pip` при `python -m pip list`

**Причина:** uv venv не включает pip по умолчанию.

**Решение:** Использовать `uv pip list` вместо `python -m pip list`.

**Статус:** By design. uv заменяет pip.

---

## 8. SOPS Decrypt Parsing

**Симптом:** `IndexError: list index out of range` в RAG скриптах

**Причина:** SOPS decrypt выводит `KEY: value` без кавычек, а парсинг ожидал `KEY: "value"`.

**Решение:** Исправлено. Парсинг использует `split(":", 1)` + `strip()`.

**Статус:** Fixed.