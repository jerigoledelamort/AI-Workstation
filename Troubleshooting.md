# Troubleshooting

## Сервисы

### Health check показывает FAIL

```powershell
.\scripts\monitoring\health-check.ps1
```

Если FAIL:
1. `.\scripts\setup\start-all.ps1`
2. Подождать 30 секунд
3. Повторить health check

### Ollama не отвечает

```powershell
# Процесс
Get-Process ollama

# Порт
Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5

# Env
[Environment]::GetEnvironmentVariable('OLLAMA_HOST', 'User')
# Должно быть: 127.0.0.1:11434

# Запуск вручную
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
```

**Причины:**
- `OLLAMA_HOST` не установлен
- Порт занят: `netstat -ano | findstr 11434`
- Models path недоступен

### LiteLLM не запускается

```powershell
Get-Process litellm
Invoke-RestMethod -Uri 'http://127.0.0.1:4000/health/liveliness' -TimeoutSec 5
.\scripts\setup\start-litellm.bat   # вручную, смотреть вывод
```

**Причины:**
- SOPS не может расшифровать `.secrets.yaml` → проверить `SOPS_AGE_KEY_FILE`
- `PYTHONUTF8=1` не установлен → Unicode ошибки
- Ollama не запущен

**Unicode ошибка:**
```
UnicodeEncodeError: 'charmap' codec can't encode characters
```
Решение: `start-litellm.bat` должен содержать `set PYTHONUTF8=1` и `set PYTHONIOENCODING=utf-8`.

### Router Proxy не запускается

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:4001/health' -TimeoutSec 5
.\scripts\setup\start-router.bat   # вручную
```

**Причины:**
- LiteLLM не запущен (Router проксирует на `:4000`)
- `.venv` повреждён → `uv sync`

### Qdrant не запускается

```powershell
Get-Process qdrant
Invoke-RestMethod -Uri 'http://127.0.0.1:6333/healthz' -TimeoutSec 5
.\scripts\setup\start-qdrant.bat
```

**Причины:**
- Порт 6333/6334 занят → `netstat -ano | findstr 633`
- Storage path недоступен

### Open WebUI не запускается

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8080/health' -TimeoutSec 10
.\scripts\setup\start-webui.bat
```

**Причины:**
- `.venv-webui/` повреждён → пересоздать
- `LITELLM_API_KEY` не передан → проверить SOPS decrypt

---

## GhidraMCP

### Cline не видит GhidraMCP

1. Ghidra запущен с бинарником, GhidraMCP plugin включён
2. HTTP сервер GhidraMCP на `127.0.0.1:8080` активен
3. MCP Bridge запущен: `Get-Process python` (должен быть процесс bridge)
4. `cline_mcp_settings.json` содержит:
   ```json
   { "mcpServers": { "ghidra": { "url": "http://127.0.0.1:8081/sse" } } }
   ```
5. Перезапустить VS Code

### Bridge падает

```powershell
.\scripts\setup\start-ghidra-mcp.bat   # вручную, смотреть вывод
```

**Причины:**
- `.venv-mcp/` повреждён → `uv pip install mcp httpx` в `.venv-mcp`
- Ghidra HTTP не отвечает → проверить plugin в Ghidra

---

## Python / uv

### No module named pip

uv venv не включает pip. Использовать:
```powershell
uv pip list
uv pip install <package>
uv sync
```

### venv повреждён

```powershell
Remove-Item -Recurse -Force .venv
uv venv .venv --python 3.10
uv sync
```

### ImportError в RAG скриптах

```
ImportError: cannot import name 'Qdrant' from 'langchain_community.vectorstores'
```

Решение — использовать `langchain-qdrant` и `langchain-ollama`:
```python
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings, ChatOllama
```

### SOPS decrypt IndexError

SOPS выводит `KEY: value` без кавычек. Парсинг:
```python
val = line.split(":", 1)[1].strip().strip('"').strip("'")
```

---

## Безопасность

### LiteLLM принимает запросы без API key

```powershell
$body = @{ model='chat-low'; messages=@(@{ role='user'; content='test' }) } | ConvertTo-Json
try {
    Invoke-RestMethod -Uri 'http://127.0.0.1:4000/v1/chat/completions' -Method POST -ContentType 'application/json' -Body $body -TimeoutSec 5
    Write-Host "FAIL: Auth disabled!"
} catch {
    Write-Host "OK: Auth working"
}
```

Если auth не работает:
1. Проверить `config/litellm/config.yaml` → `master_key`
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
Test-Path "$env:USERPROFILE\.config\sops\age\keys.txt"
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"
& 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
```

Если `keys.txt` утерян → [DisasterRecovery.md](DisasterRecovery.md) → «Только секреты».

---

## Производительность

### Модель загружается медленно

```powershell
.\scripts\monitoring\vram-check.ps1
# Использовать модель меньшего размера: chat-low вместо chat-high
```

### Ollama OOM

```powershell
nvidia-smi
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
ollama rm <unused-model>   # удалить неиспользуемые
```

### RAG работает медленно

- Уменьшить `chunk_size` (500 → 300)
- Уменьшить `k` в retriever (3 → 2)
- Использовать `nomic-embed-text` вместо `bge-m3`

---

## Cline / VS Code

### Cline не подключается

1. Проверить что Router запущен: `Invoke-RestMethod http://127.0.0.1:4001/health`
2. Проверить Cline config: Base URL `http://127.0.0.1:4001/v1`
3. Перезапустить VS Code

### Cline не видит MCP инструменты

1. Проверить `cline_mcp_settings.json`
2. Перезапустить VS Code
3. Проверить что MCP-сервер запущен (GhidraMCP Bridge на `:8081`)

### .clinerules не читается

- Файл должен быть в корне открытой папки
- Cline читает его автоматически при старте чата

---

## Автозапуск

### Сервисы не запускаются при логине

```powershell
Get-ScheduledTask -TaskName 'AI-Workstation-AutoStart'
Get-ScheduledTaskInfo -TaskName 'AI-Workstation-AutoStart'
Start-ScheduledTask -TaskName 'AI-Workstation-AutoStart'
```

**Причины:**
- Задача отключена → `Enable-ScheduledTask`
- `start-all.ps1` недоступен
- ExecutionPolicy → задача использует `-ExecutionPolicy Bypass`
- Конфликт сервисов → `stop-all.ps1` затем `start-all.ps1`

### Пересоздать задачу

```powershell
Unregister-ScheduledTask -TaskName 'AI-Workstation-AutoStart' -Confirm:$false

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"D:\Projects\ai\scripts\setup\start-all.ps1`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "AI-Workstation-AutoStart" -Action $action -Trigger $trigger -Settings $settings -Description "AI Workstation: start all services at logon"
```
