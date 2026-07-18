# Disaster Recovery

Полное руководство по восстановлению AI Workstation с нуля без доступа к интернету.

> **Важно:** Все бинарники и модели должны быть заранее сохранены на локальном носителе.
> Рекомендуется периодическое резервное копирование в `D:\Projects\ai\backup\`.

## Предварительные требования

### Локальные артефакты (должны быть сохранены заранее)

| Артефакт | Путь | Размер |
|----------|------|--------|
| Git репозиторий | `D:\Projects\ai\` | ~50 МБ (без .venv) |
| Python 3.10.10 | `C:\Python310\` или установщик | ~30 МБ |
| uv 0.11.29 | `C:\Users\egork\.local\bin\uv.exe` | ~15 МБ |
| Ollama 0.32.0 | `C:\Users\egork\AppData\Local\Programs\Ollama\` | ~500 МБ |
| Ollama models | `C:\Users\egork\AppData\Local\Programs\Ollama\` | ~97 ГБ |
| SOPS 3.13.2 | `C:\Tools\sops\sops.exe` | ~30 МБ |
| age 1.3.1 | `C:\Tools\age\age\` | ~5 МБ |
| Qdrant 1.18.3 | `C:\Tools\qdrant\qdrant.exe` | ~81 МБ |
| age keypair | `~/.config/sops/age/keys.txt` | <1 КБ |
| .secrets.yaml | `D:\Projects\ai\.secrets.yaml` | <1 КБ |
| Continue config | `~/.continue/config.json` | <1 КБ |

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
| Continue extension | VS Code marketplace (offline: .vsix file) | v2.0.0 |

## Процедура восстановления (полная)

### Шаг 1. Восстановление инструментов

#### 1.1. Python 3.10

```powershell
# Установить Python 3.10.10 (из сохранённого установщика)
# Убедиться, что python --version == 3.10.10
python --version
```

#### 1.2. uv

```powershell
# Восстановить uv.exe в ~/.local/bin/
# Или установить из сохранённого zip
uv --version  # должно быть 0.11.29
```

#### 1.3. Ollama

```powershell
# Восстановить C:\Users\egork\AppData\Local\Programs\Ollama\
# Включая models/ директорию (~97 ГБ)

# Установить environment variables
[Environment]::SetEnvironmentVariable('OLLAMA_HOST', '127.0.0.1:11434', 'User')
[Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'C:\Users\egork\AppData\Local\Programs\Ollama', 'User')

# Проверить
ollama --version   # 0.32.0
ollama list        # 11 моделей
```

#### 1.4. SOPS

```powershell
# Восстановить C:\Tools\sops\sops.exe
# Добавить в PATH
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\sops", 'User')

# Проверить
& 'C:\Tools\sops\sops.exe' --version  # sops 3.13.2
```

#### 1.5. age

```powershell
# Восстановить C:\Tools\age\age\ (age.exe, age-keygen.exe, age-inspect.exe)
# Добавить в PATH
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\age\age", 'User')

# Восстановить age keypair
# КРИТИЧНО: без keys.txt невозможно расшифровать .secrets.yaml
New-Item -ItemType Directory -Path "$env:USERPROFILE\.config\sops\age" -Force
# Восстановить keys.txt из резервной копии в ~/.config/sops/age/keys.txt
# Файл содержит приватный ключ. НЕ коммитить в git.

# Проверить
& 'C:\Tools\age\age\age.exe' --version  # 1.3.1
```

#### 1.6. Qdrant

```powershell
# Восстановить C:\Tools\qdrant\qdrant.exe
# Добавить в PATH
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\qdrant", 'User')

# Проверить
& 'C:\Tools\qdrant\qdrant.exe' --version  # 1.18.3
```

### Шаг 2. Восстановление проекта

```powershell
# Восстановить git репозиторий
cd D:\Projects
# Если есть backup — распаковать
# Если есть git remote — git clone

cd D:\Projects\ai

# Восстановить .secrets.yaml (из резервной копии, НЕ из git)
# Файл gitignored, должен быть сохранён отдельно

# Восстановить ~/.continue/config.json (из резервной копии)
```

### Шаг 3. Python окружение

```powershell
cd D:\Projects\ai

# Создать venv
uv venv .venv --python 3.10

# Установить зависимости
uv sync

# Проверить
& '.venv\Scripts\python.exe' -c "import litellm; import langchain; import qdrant_client; print('OK')"
```

### Шаг 4. Firewall правила

```powershell
# 6 inbound block rules
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

### Шаг 5. Запуск и проверка

```powershell
# Запустить все сервисы
.\scripts\setup\start-all.ps1

# Проверить
.\scripts\monitoring\health-check.ps1
# Ожидаемый результат: [OK] Ollama, [OK] LiteLLM, [OK] Qdrant

# Аудит безопасности
.\tests\test-security.ps1
# Ожидаемый результат: 10/10 PASS

# Тест inference
.\tests\test-inference.ps1
# Ожидаемый результат: 6/6 PASS
```

### Шаг 6. VS Code + Continue

```powershell
# Установить VS Code
# Установить Continue extension (v2.0.0)

# Установить CONTINUE_API_KEY
# Расшифровать из .secrets.yaml:
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"
$decrypted = & 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
$apiKey = ($decrypted | Select-String 'LITELLM_API_KEY:').ToString() -replace '.*:\s*',''
[Environment]::SetEnvironmentVariable('CONTINUE_API_KEY', $apiKey, 'User')

# Перезапустить VS Code
```

## Резервное копирование

### Что копировать регулярно

```powershell
# Скрипт резервного копирования
.\scripts\backup\backup.ps1

# Дополнительно сохранить вручную:
# 1. ~/.config/sops/age/keys.txt (CRITICAL — без него нет доступа к секретам)
# 2. ~/.continue/config.json
# 3. D:\Projects\ai\.secrets.yaml
# 4. C:\Tools\ (sops, age, qdrant — небольшие бинарники)
# 5. Git push на remote (если настроен)
```

### Критичные файлы (порядок важности)

1. **age keys.txt** — без него невозможно расшифровать секреты
2. **.secrets.yaml** — содержит API ключи
3. **Git репозиторий** — весь код и конфиги
4. **Ollama models** — ~97 ГБ, долго скачивать заново
5. **~/.continue/config.json** — конфигурация Continue

### Рекомендуемая стратегия

| Частота | Что | Куда |
|---------|-----|------|
| Еженедельно | `backup.ps1` (конфиги) | `D:\Projects\ai\backup\` |
| Ежемесячно | Git push | Remote (приватный repo) |
| После изменений | age keys.txt | Внешний носитель (USB) |
| После установки | Все бинарники | Внешний HDD |

## Восстановление отдельных компонентов

### Только Ollama

```powershell
# Остановить
Get-Process ollama | Stop-Process -Force

# Восстановить models/ директорию
# Запустить заново
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
```

### Только LiteLLM

```powershell
# Остановить
Get-Process litellm | Stop-Process -Force

# Пересоздать venv если нужно
uv venv .venv --python 3.10
uv sync

# Запустить
.\scripts\setup\start-litellm.bat
```

### Только Qdrant

```powershell
# Остановить
Get-Process qdrant | Stop-Process -Force

# Восстановить storage/ если нужно
# Запустить
Start-Process '.\scripts\setup\start-qdrant.bat' -WindowStyle Minimized
```

### Только секреты (если keys.txt утерян)

> **ВНИМАНИЕ:** Если age keys.txt утерян, секреты невозможно восстановить.
> Необходимо сгенерировать новый keypair и пересоздать .secrets.yaml.

```powershell
# Генерация нового keypair
& 'C:\Tools\age\age\age-keygen.exe' -o "$env:USERPROFILE\.config\sops\age\keys.txt"

# Получить public key
$pubKey = (& 'C:\Tools\age\age\age-keygen.exe' -y "$env:USERPROFILE\.config\sops\age\keys.txt").Trim()

# Обновить .sops.yaml с новым recipient
# Создать новый .secrets.yaml
$secrets = @"
LITELLM_API_KEY: sk-$( -join ((48..57)+(97..122) | Get-Random -Count 48 | ForEach-Object {[char]$_}))
OLLAMA_API_BASE: http://127.0.0.1:11434
"@
$secrets | & 'C:\Tools\sops\sops.exe' --encrypt --age "$pubKey" /dev/stdin > .secrets.yaml

# Обновить CONTINUE_API_KEY
$decrypted = & 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
$apiKey = ($decrypted | Select-String 'LITELLM_API_KEY:').ToString() -replace '.*:\s*',''
[Environment]::SetEnvironmentVariable('CONTINUE_API_KEY', $apiKey, 'User')
```