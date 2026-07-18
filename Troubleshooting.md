# Troubleshooting

## Сервисы

### Ollama не отвечает

```powershell
# Проверить процесс
Get-Process ollama

# Проверить порт
Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5

# Проверить env
[Environment]::GetEnvironmentVariable('OLLAMA_HOST', 'User')
# Должно быть: 127.0.0.1:11434

# Запустить вручную
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
```

**Возможные причины:**
- `OLLAMA_HOST` не установлен или не `127.0.0.1:11434`
- Порт занят другим процессом: `netstat -ano | findstr 11434`
- Models path недоступен: проверить `OLLAMA_MODELS`

### LiteLLM не запускается

```powershell
# Проверить процесс
Get-Process litellm

# Проверить порт
Invoke-RestMethod -Uri 'http://127.0.0.1:4000/health/liveliness' -TimeoutSec 5

# Запустить вручную и посмотреть вывод
.\scripts\setup\start-litellm.bat
```

**Возможные причины:**
- SOPS не может расшифровать `.secrets.yaml` → проверить `SOPS_AGE_KEY_FILE`
- `PYTHONUTF8=1` не установлен → Unicode ошибки в Windows
- Ollama не запущен → LiteLLM не может проксировать
- venv повреждён → `uv sync` для переустановки

**Unicode ошибки:**
```
UnicodeEncodeError: 'charmap' codec can't encode characters
```
Решение: убедиться что `start-litellm.bat` содержит `set PYTHONUTF8=1` и `set PYTHONIOENCODING=utf-8`.

### Qdrant не запускается

```powershell
# Проверить процесс
Get-Process qdrant

# Проверить порт
Invoke-RestMethod -Uri 'http://127.0.0.1:6333/healthz' -TimeoutSec 5

# Запустить вручную
cd C:\Tools\qdrant
.\qdrant.exe --config-path D:\Projects\ai\config\qdrant\qdrant.yaml
```

**Возможные причины:**
- Порт 6333/6334 занят → `netstat -ano | findstr 633`
- Storage path недоступен → проверить `C:\Tools\qdrant\storage\`
- Config file не найден → проверить путь в `--config-path`

### Health check показывает FAIL

```powershell
.\scripts\monitoring\health-check.ps1
```

Проверяет 3 сервиса. Если FAIL:
1. Запустить `start-all.ps1`
2. Подождать 15 секунд
3. Повторить health check

## Python / uv

### No module named pip

```powershell
# НЕ использовать python -m pip
# Использовать uv:
uv pip list
uv pip install <package>
uv sync
```

### venv повреждён

```powershell
# Удалить и пересоздать
Remove-Item -Recurse -Force .venv
uv venv .venv --python 3.10
uv sync
```

### ImportError в RAG скриптах

```
ImportError: cannot import name 'Qdrant' from 'langchain_community.vectorstores'
```

**Решение:** Использовать `langchain-qdrant` и `langchain-ollama`:
```python
from langchain_qdrant import QdrantVectorStore  # НЕ langchain_community
from langchain_ollama import OllamaEmbeddings, ChatOllama  # НЕ langchain_community
```

### SOPS decrypt IndexError

```
IndexError: list index out of range
```

**Решение:** SOPS выводит `KEY: value` без кавычек. Парсинг:
```python
val = line.split(":", 1)[1].strip().strip('"').strip("'")
```

## Безопасность

### LiteLLM принимает запросы без API key

```powershell
# Проверить
$body = @{ model = 'chat-low'; messages = @(@{ role='user'; content='test' }) } | ConvertTo-Json
try {
    Invoke-RestMethod -Uri 'http://127.0.0.1:4000/v1/chat/completions' -Method POST -ContentType 'application/json' -Body $body -TimeoutSec 5
    Write-Host "FAIL: Auth disabled!"
} catch {
    Write-Host "OK: Auth working"
}
```

Если auth не работает:
1. Проверить `config/litellm/config.yaml` → `general_settings.master_key`
2. Проверить что `LITELLM_API_KEY` загружается из SOPS
3. Перезапустить LiteLLM

### Firewall правила отсутствуют

```powershell
# Проверить
Get-NetFirewallRule -DisplayName 'Block-*Inbound' | Where-Object { $_.DisplayName -match 'Ollama|LiteLLM|Qdrant|OpenWebUI|MkDocs' }

# Создать заново
$ports = @(
    @{ Name='Block-Ollama-Inbound'; Port=11434 },
    @{ Name='Block-LiteLLM-Inbound'; Port=4000 },
    @{ Name='Block-Qdrant-REST-Inbound'; Port=6333 },
    @{ Name='Block-Qdrant-gRPC-Inbound'; Port=6334 },
    @{ Name='Block-OpenWebUI-Inbound'; Port=8080 },
    @{ Name='Block-MkDocs-Inbound'; Port=8000 }
)
foreach ($p in $ports) {
    New-NetFirewallRule -DisplayName $p.Name -Direction Inbound -Action Block -Protocol TCP -LocalPort $p.Port
}
```

### SOPS не может расшифровать

```powershell
# Проверить key file
Test-Path "$env:USERPROFILE\.config\sops\age\keys.txt"

# Установить env
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"

# Попробовать расшифровать
& 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
```

Если keys.txt утерян — см. [DisasterRecovery.md](DisasterRecovery.md) → "Только секреты".

## Производительность

### Модель загружается медленно

```powershell
# Проверить VRAM
.\scripts\monitoring\vram-check.ps1

# Использовать модель меньшего размера
# chat-low вместо chat-high
```

### Ollama OOM (out of memory)

```powershell
# Проверить VRAM и RAM
nvidia-smi
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory

# Закрыть лишние модели
ollama rm <unused-model>

# Использовать Low profile модели
```

### RAG работает медленно

- Уменьшить `chunk_size` (500 → 300)
- Уменьшить `k` в retriever (3 → 2)
- Использовать `nomic-embed-text` вместо `bge-m3` (меньше размер)

## VS Code / Continue

### Continue не подключается к LiteLLM

1. Проверить `CONTINUE_API_KEY` environment variable
2. Проверить что LiteLLM запущен: `health-check.ps1`
3. Проверить `~/.continue/config.json` → `apiBase: http://127.0.0.1:4000/v1`
4. Перезапустить VS Code после установки env var

### Autocomplete не работает

- Проверить `tabAutocompleteModel` в config.json → `coder-low`
- Убедиться что Ollama запущен
- Проверить `embeddingsProvider` → `embed-low`

## MkDocs

### Build error

```powershell
cd D:\Projects\ai
& '.venv\Scripts\python.exe' -m mkdocs build --strict
```

Все ссылки в nav должны существовать в `docs/`.

### Serve не запускается

```powershell
& '.venv\Scripts\python.exe' -m mkdocs serve
# Доступен на http://127.0.0.1:8000
```

Если порт занят: `mkdocs serve --dev-addr 127.0.0.1:8001`