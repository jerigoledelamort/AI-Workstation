# Disaster Recovery

Полное руководство по восстановлению AI Workstation с нуля без доступа к интернету.

> **Важно:** Все бинарники и модели должны быть заранее сохранены на локальном носителе.
> Рекомендуется периодическое резервное копирование через `.\scripts\backup\backup.ps1`.

---

## Предварительные требования

### Локальные артефакты (сохранить заранее)

| Артефакт | Путь | Размер |
|----------|------|--------|
| Git репозиторий | `D:\Projects\ai\` | ~50 МБ (без venv) |
| Python 3.10.10 | `C:\Python310\` или установщик | ~30 МБ |
| Python 3.12.13 | uv-managed (`uv python install 3.12`) | ~25 МБ |
| uv 0.11.29 | `C:\Users\egork\.local\bin\uv.exe` | ~15 МБ |
| Ollama 0.32.0 | `C:\Users\egork\AppData\Local\Programs\Ollama\` | ~500 МБ |
| Ollama models | (там же, `models/`) | ~97 ГБ |
| SOPS 3.13.2 | `C:\Tools\sops\sops.exe` | ~30 МБ |
| age 1.3.1 | `C:\Tools\age\age\` | ~5 МБ |
| Qdrant 1.18.3 | `C:\Tools\qdrant\qdrant.exe` | ~81 МБ |
| Open WebUI 0.10.2 | `D:\Projects\ai\.venv-webui\` | ~500 МБ |
| Ghidra 12.1.2 | `D:\Applications\Coding\Ghidra\` | ~400 МБ |
| age keypair | `~/.config/sops/age/keys.txt` | <1 КБ |
| `.secrets.yaml` | `D:\Projects\ai\.secrets.yaml` | <1 КБ |

### Скачать заранее (для offline-установки)

| Tool | URL | Version |
|------|-----|---------|
| Python 3.10 | https://www.python.org/downloads/release/python-31010/ | 3.10.10 |
| uv | https://github.com/astral-sh/uv/releases/download/0.11.29/uv-x86_64-pc-windows-msvc.zip | 0.11.29 |
| Ollama | https://ollama.com/download/OllamaSetup.exe | 0.32.0 |
| SOPS | https://github.com/getsops/sops/releases/download/v3.13.2/sops-v3.13.2.exe | 3.13.2 |
| age | https://github.com/FiloSottile/age/releases/download/v1.3.1/age-v1.3.1-windows-amd64.zip | 1.3.1 |
| Qdrant | https://github.com/qdrant/qdrant/releases/download/v1.18.3/qdrant-x86_64-pc-windows-msvc.zip | 1.18.3 |
| VS Code | https://code.visualstudio.com/Download | latest |
| Cline extension | VS Code marketplace (offline: .vsix) | latest |
| Open WebUI | `pip install open-webui` (Python >=3.11) | 0.10.2 |

---

## Процедура восстановления (полная)

### Шаг 1. Инструменты

#### Python 3.10

```powershell
python --version  # должно быть 3.10.10
```

#### uv

```powershell
uv --version  # 0.11.29
```

#### Ollama

```powershell
# Восстановить C:\Users\egork\AppData\Local\Programs\Ollama\ (с models/)
[Environment]::SetEnvironmentVariable('OLLAMA_HOST', '127.0.0.1:11434', 'User')
[Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'C:\Users\egork\AppData\Local\Programs\Ollama', 'User')
ollama --version   # 0.32.0
ollama list        # 11 моделей
```

#### SOPS + age

```powershell
# Восстановить C:\Tools\sops\ и C:\Tools\age\age\
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\sops;C:\Tools\age\age", 'User')

# Восстановить age keypair (КРИТИЧНО)
New-Item -ItemType Directory -Path "$env:USERPROFILE\.config\sops\age" -Force
# Скопировать keys.txt из резервной копии

& 'C:\Tools\sops\sops.exe' --version   # 3.13.2
& 'C:\Tools\age\age\age.exe' --version # 1.3.1
```

#### Qdrant

```powershell
# Восстановить C:\Tools\qdrant\
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\qdrant", 'User')
& 'C:\Tools\qdrant\qdrant.exe' --version  # 1.18.3
```

### Шаг 2. Проект

```powershell
cd D:\Projects
# Если есть backup — распаковать
# Если есть git remote — git clone https://github.com/jerigoledelamort/AI-Workstation.git

cd D:\Projects\ai

# Восстановить .secrets.yaml (из резервной копии, НЕ из git)
# Восстановить ~/.continue/config.json (если используется Continue)
```

### Шаг 3. Python окружения

```powershell
cd D:\Projects\ai

# Основной venv (Python 3.10)
uv venv .venv --python 3.10
uv sync

# Open WebUI venv (Python 3.12)
uv python install 3.12
uv venv .venv-webui --python 3.12
.venv-webui\Scripts\pip install open-webui

# MCP venv (Python 3.12)
uv venv .venv-mcp --python 3.12
.venv-mcp\Scripts\pip install mcp httpx

# Проверка
& '.venv\Scripts\python.exe' -c "import litellm, langchain, qdrant_client; print('OK')"
```

### Шаг 4. Environment variables

```powershell
[Environment]::SetEnvironmentVariable('SOPS_AGE_KEY_FILE', "$env:USERPROFILE\.config\sops\age\keys.txt", 'User')

# Расшифровать API key
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"
$decrypted = & 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
$apiKey = ($decrypted | Select-String 'LITELLM_API_KEY:').ToString() -replace '.*:\s*',''
[Environment]::SetEnvironmentVariable('LITELLM_API_KEY', $apiKey, 'User')
[Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $apiKey, 'User')
[Environment]::SetEnvironmentVariable('CONTINUE_API_KEY', $apiKey, 'User')
```

### Шаг 5. Firewall

```powershell
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

### Шаг 6. Запуск и проверка

```powershell
.\scripts\setup\start-all.ps1
.\scripts\monitoring\health-check.ps1    # Все [OK]
.\tests\test-security.ps1                 # 10/10 PASS
.\tests\test-inference.ps1                # 6/6 PASS
```

### Шаг 7. VS Code + Cline

1. Установить VS Code
2. Установить расширение Cline (`saoudrizwan.claude-dev`)
3. Настроить Cline:
   - Provider: OpenAI Compatible
   - Base URL: `http://127.0.0.1:4001/v1`
   - Model: `auto`
4. Перезапустить VS Code

### Шаг 8. Автозапуск

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"D:\Projects\ai\scripts\setup\start-all.ps1`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "AI-Workstation-AutoStart" -Action $action -Trigger $trigger -Settings $settings -Description "AI Workstation: start all services at logon"

Get-ScheduledTask -TaskName "AI-Workstation-AutoStart"  # State: Ready
```

---

## Резервное копирование

### Что копировать регулярно

```powershell
.\scripts\backup\backup.ps1
```

Дополнительно вручную:
1. `~/.config/sops/age/keys.txt` — **КРИТИЧНО** (без него нет доступа к секретам)
2. `~/.continue/config.json`
3. `D:\Projects\ai\.secrets.yaml`
4. `C:\Tools\` (sops, age, qdrant — небольшие бинарники)
5. Git push на remote

### Критичные файлы (порядок важности)

| # | Файл | Почему критичен |
|---|------|-----------------|
| 1 | `age keys.txt` | Без него невозможно расшифровать секреты |
| 2 | `.secrets.yaml` | API ключи |
| 3 | Git репозиторий | Весь код и конфиги |
| 4 | Ollama models | ~97 ГБ, долго скачивать |
| 5 | `~/.continue/config.json` | Конфигурация Continue |

### Стратегия

| Частота | Что | Куда |
|---------|-----|------|
| Еженедельно | `backup.ps1` (конфиги) | `D:\Projects\ai\backup\` |
| Ежемесячно | `git push` | Remote (приватный repo) |
| После изменений | `keys.txt` | Внешний носитель (USB) |
| После установки | Все бинарники | Внешний HDD |

---

## Восстановление отдельных компонентов

### Только Ollama

```powershell
Get-Process ollama | Stop-Process -Force
# Восстановить models/ директорию
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
```

### Только LiteLLM

```powershell
Get-Process litellm | Stop-Process -Force
uv venv .venv --python 3.10
uv sync
.\scripts\setup\start-litellm.bat
```

### Только Qdrant

```powershell
Get-Process qdrant | Stop-Process -Force
# Восстановить storage/ если нужно
.\scripts\setup\start-qdrant.bat
```

### Только секреты (если keys.txt утерян)

> **ВНИМАНИЕ:** Если `keys.txt` утерян, старые секреты невозможно восстановить.
> Нужно сгенерировать новый keypair и пересоздать `.secrets.yaml`.

```powershell
# Новый keypair
& 'C:\Tools\age\age\age-keygen.exe' -o "$env:USERPROFILE\.config\sops\age\keys.txt"
$pubKey = (& 'C:\Tools\age\age\age-keygen.exe' -y "$env:USERPROFILE\.config\sops\age\keys.txt").Trim()

# Обновить .sops.yaml с новым recipient
# Создать новый .secrets.yaml
$secrets = @"
LITELLM_API_KEY: sk-$( -join ((48..57)+(97..122) | Get-Random -Count 48 | ForEach-Object {[char]$_}))
OLLAMA_API_BASE: http://127.0.0.1:11434
"@
$secrets | & 'C:\Tools\sops\sops.exe' --encrypt --age "$pubKey" /dev/stdin > .secrets.yaml

# Обновить env vars
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"
$decrypted = & 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
$apiKey = ($decrypted | Select-String 'LITELLM_API_KEY:').ToString() -replace '.*:\s*',''
[Environment]::SetEnvironmentVariable('LITELLM_API_KEY', $apiKey, 'User')
[Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $apiKey, 'User')
[Environment]::SetEnvironmentVariable('CONTINUE_API_KEY', $apiKey, 'User')
```
