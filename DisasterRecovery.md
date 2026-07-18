# Disaster Recovery

РџРѕР»РЅРѕРµ СЂСѓРєРѕРІРѕРґСЃС‚РІРѕ РїРѕ РІРѕСЃСЃС‚Р°РЅРѕРІР»РµРЅРёСЋ AI Workstation СЃ РЅСѓР»СЏ Р±РµР· РґРѕСЃС‚СѓРїР° Рє РёРЅС‚РµСЂРЅРµС‚Сѓ.

> **Р’Р°Р¶РЅРѕ:** Р’СЃРµ Р±РёРЅР°СЂРЅРёРєРё Рё РјРѕРґРµР»Рё РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ Р·Р°СЂР°РЅРµРµ СЃРѕС…СЂР°РЅРµРЅС‹ РЅР° Р»РѕРєР°Р»СЊРЅРѕРј РЅРѕСЃРёС‚РµР»Рµ.
> Р РµРєРѕРјРµРЅРґСѓРµС‚СЃСЏ РїРµСЂРёРѕРґРёС‡РµСЃРєРѕРµ СЂРµР·РµСЂРІРЅРѕРµ РєРѕРїРёСЂРѕРІР°РЅРёРµ РІ `D:\Projects\ai\backup\`.

## РџСЂРµРґРІР°СЂРёС‚РµР»СЊРЅС‹Рµ С‚СЂРµР±РѕРІР°РЅРёСЏ

### Р›РѕРєР°Р»СЊРЅС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹ (РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ СЃРѕС…СЂР°РЅРµРЅС‹ Р·Р°СЂР°РЅРµРµ)

| РђСЂС‚РµС„Р°РєС‚ | РџСѓС‚СЊ | Р Р°Р·РјРµСЂ |
|----------|------|--------|
| Git СЂРµРїРѕР·РёС‚РѕСЂРёР№ | `D:\Projects\ai\` | ~50 РњР‘ (Р±РµР· .venv) |
| Python 3.10.10 | `C:\Python310\` РёР»Рё СѓСЃС‚Р°РЅРѕРІС‰РёРє | ~30 РњР‘ |
| uv 0.11.29 | `C:\Users\egork\.local\bin\uv.exe` | ~15 РњР‘ |
| Ollama 0.32.0 | `C:\Users\egork\AppData\Local\Programs\Ollama\` | ~500 РњР‘ |
| Ollama models | `C:\Users\egork\AppData\Local\Programs\Ollama\` | ~97 Р“Р‘ |
| SOPS 3.13.2 | `C:\Tools\sops\sops.exe` | ~30 РњР‘ |
| age 1.3.1 | `C:\Tools\age\age\` | ~5 РњР‘ |
| Qdrant 1.18.3 | `C:\Tools\qdrant\qdrant.exe` | ~81 РњР‘ |
| age keypair | `~/.config/sops/age/keys.txt` | <1 РљР‘ |
| .secrets.yaml | `D:\Projects\ai\.secrets.yaml` | <1 РљР‘ |
| Continue config | `~/.continue/config.json` | <1 РљР‘ |

### РЎРєР°С‡Р°С‚СЊ Р·Р°СЂР°РЅРµРµ (РґР»СЏ offline-СѓСЃС‚Р°РЅРѕРІРєРё)

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
| Open WebUI | `pip install open-webui` (requires Python >=3.11) | 0.10.2 |

## РџСЂРѕС†РµРґСѓСЂР° РІРѕСЃСЃС‚Р°РЅРѕРІР»РµРЅРёСЏ (РїРѕР»РЅР°СЏ)

### РЁР°Рі 1. Р’РѕСЃСЃС‚Р°РЅРѕРІР»РµРЅРёРµ РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ

#### 1.1. Python 3.10

```powershell
# РЈСЃС‚Р°РЅРѕРІРёС‚СЊ Python 3.10.10 (РёР· СЃРѕС…СЂР°РЅС‘РЅРЅРѕРіРѕ СѓСЃС‚Р°РЅРѕРІС‰РёРєР°)
# РЈР±РµРґРёС‚СЊСЃСЏ, С‡С‚Рѕ python --version == 3.10.10
python --version
```

#### 1.2. uv

```powershell
# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ uv.exe РІ ~/.local/bin/
# РР»Рё СѓСЃС‚Р°РЅРѕРІРёС‚СЊ РёР· СЃРѕС…СЂР°РЅС‘РЅРЅРѕРіРѕ zip
uv --version  # РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ 0.11.29
```

#### 1.3. Ollama

```powershell
# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ C:\Users\egork\AppData\Local\Programs\Ollama\
# Р’РєР»СЋС‡Р°СЏ models/ РґРёСЂРµРєС‚РѕСЂРёСЋ (~97 Р“Р‘)

# РЈСЃС‚Р°РЅРѕРІРёС‚СЊ environment variables
[Environment]::SetEnvironmentVariable('OLLAMA_HOST', '127.0.0.1:11434', 'User')
[Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'C:\Users\egork\AppData\Local\Programs\Ollama', 'User')

# РџСЂРѕРІРµСЂРёС‚СЊ
ollama --version   # 0.32.0
ollama list        # 11 РјРѕРґРµР»РµР№
```

#### 1.4. SOPS

```powershell
# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ C:\Tools\sops\sops.exe
# Р”РѕР±Р°РІРёС‚СЊ РІ PATH
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\sops", 'User')

# РџСЂРѕРІРµСЂРёС‚СЊ
& 'C:\Tools\sops\sops.exe' --version  # sops 3.13.2
```

#### 1.5. age

```powershell
# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ C:\Tools\age\age\ (age.exe, age-keygen.exe, age-inspect.exe)
# Р”РѕР±Р°РІРёС‚СЊ РІ PATH
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\age\age", 'User')

# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ age keypair
# РљР РРўРР§РќРћ: Р±РµР· keys.txt РЅРµРІРѕР·РјРѕР¶РЅРѕ СЂР°СЃС€РёС„СЂРѕРІР°С‚СЊ .secrets.yaml
New-Item -ItemType Directory -Path "$env:USERPROFILE\.config\sops\age" -Force
# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ keys.txt РёР· СЂРµР·РµСЂРІРЅРѕР№ РєРѕРїРёРё РІ ~/.config/sops/age/keys.txt
# Р¤Р°Р№Р» СЃРѕРґРµСЂР¶РёС‚ РїСЂРёРІР°С‚РЅС‹Р№ РєР»СЋС‡. РќР• РєРѕРјРјРёС‚РёС‚СЊ РІ git.

# РџСЂРѕРІРµСЂРёС‚СЊ
& 'C:\Tools\age\age\age.exe' --version  # 1.3.1
```

#### 1.6. Qdrant

```powershell
# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ C:\Tools\qdrant\qdrant.exe
# Р”РѕР±Р°РІРёС‚СЊ РІ PATH
$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;C:\Tools\qdrant", 'User')

# РџСЂРѕРІРµСЂРёС‚СЊ
& 'C:\Tools\qdrant\qdrant.exe' --version  # 1.18.3
```

### РЁР°Рі 2. Р’РѕСЃСЃС‚Р°РЅРѕРІР»РµРЅРёРµ РїСЂРѕРµРєС‚Р°

```powershell
# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ git СЂРµРїРѕР·РёС‚РѕСЂРёР№
cd D:\Projects
# Р•СЃР»Рё РµСЃС‚СЊ backup вЂ” СЂР°СЃРїР°РєРѕРІР°С‚СЊ
# Р•СЃР»Рё РµСЃС‚СЊ git remote вЂ” git clone

cd D:\Projects\ai

# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ .secrets.yaml (РёР· СЂРµР·РµСЂРІРЅРѕР№ РєРѕРїРёРё, РќР• РёР· git)
# Р¤Р°Р№Р» gitignored, РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СЃРѕС…СЂР°РЅС‘РЅ РѕС‚РґРµР»СЊРЅРѕ

# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ ~/.continue/config.json (РёР· СЂРµР·РµСЂРІРЅРѕР№ РєРѕРїРёРё)
```

### РЁР°Рі 3. Python РѕРєСЂСѓР¶РµРЅРёРµ

```powershell
cd D:\Projects\ai

# РЎРѕР·РґР°С‚СЊ venv
uv venv .venv --python 3.10

# РЈСЃС‚Р°РЅРѕРІРёС‚СЊ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё
uv sync

# РџСЂРѕРІРµСЂРёС‚СЊ
& '.venv\Scripts\python.exe' -c "import litellm; import langchain; import qdrant_client; print('OK')"
```

### РЁР°Рі 4. Firewall РїСЂР°РІРёР»Р°

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

### РЁР°Рі 5. Р—Р°РїСѓСЃРє Рё РїСЂРѕРІРµСЂРєР°

```powershell
# Р—Р°РїСѓСЃС‚РёС‚СЊ РІСЃРµ СЃРµСЂРІРёСЃС‹
.\scripts\setup\start-all.ps1

# РџСЂРѕРІРµСЂРёС‚СЊ
.\scripts\monitoring\health-check.ps1
# РћР¶РёРґР°РµРјС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚: [OK] Ollama, [OK] LiteLLM, [OK] Qdrant

# РђСѓРґРёС‚ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё
.\tests\test-security.ps1
# РћР¶РёРґР°РµРјС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚: 10/10 PASS

# РўРµСЃС‚ inference
.\tests\test-inference.ps1
# РћР¶РёРґР°РµРјС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚: 6/6 PASS
```

### РЁР°Рі 6. VS Code + Continue

```powershell
# РЈСЃС‚Р°РЅРѕРІРёС‚СЊ VS Code
# РЈСЃС‚Р°РЅРѕРІРёС‚СЊ Continue extension (v2.0.0)

# РЈСЃС‚Р°РЅРѕРІРёС‚СЊ CONTINUE_API_KEY
# Р Р°СЃС€РёС„СЂРѕРІР°С‚СЊ РёР· .secrets.yaml:
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"
$decrypted = & 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
$apiKey = ($decrypted | Select-String 'LITELLM_API_KEY:').ToString() -replace '.*:\s*',''
[Environment]::SetEnvironmentVariable('CONTINUE_API_KEY', $apiKey, 'User')

# РџРµСЂРµР·Р°РїСѓСЃС‚РёС‚СЊ VS Code
```

## Р РµР·РµСЂРІРЅРѕРµ РєРѕРїРёСЂРѕРІР°РЅРёРµ

### Р§С‚Рѕ РєРѕРїРёСЂРѕРІР°С‚СЊ СЂРµРіСѓР»СЏСЂРЅРѕ

```powershell
# РЎРєСЂРёРїС‚ СЂРµР·РµСЂРІРЅРѕРіРѕ РєРѕРїРёСЂРѕРІР°РЅРёСЏ
.\scripts\backup\backup.ps1

# Р”РѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕ СЃРѕС…СЂР°РЅРёС‚СЊ РІСЂСѓС‡РЅСѓСЋ:
# 1. ~/.config/sops/age/keys.txt (CRITICAL вЂ” Р±РµР· РЅРµРіРѕ РЅРµС‚ РґРѕСЃС‚СѓРїР° Рє СЃРµРєСЂРµС‚Р°Рј)
# 2. ~/.continue/config.json
# 3. D:\Projects\ai\.secrets.yaml
# 4. C:\Tools\ (sops, age, qdrant вЂ” РЅРµР±РѕР»СЊС€РёРµ Р±РёРЅР°СЂРЅРёРєРё)
# 5. Git push РЅР° remote (РµСЃР»Рё РЅР°СЃС‚СЂРѕРµРЅ)
```

### РљСЂРёС‚РёС‡РЅС‹Рµ С„Р°Р№Р»С‹ (РїРѕСЂСЏРґРѕРє РІР°Р¶РЅРѕСЃС‚Рё)

1. **age keys.txt** вЂ” Р±РµР· РЅРµРіРѕ РЅРµРІРѕР·РјРѕР¶РЅРѕ СЂР°СЃС€РёС„СЂРѕРІР°С‚СЊ СЃРµРєСЂРµС‚С‹
2. **.secrets.yaml** вЂ” СЃРѕРґРµСЂР¶РёС‚ API РєР»СЋС‡Рё
3. **Git СЂРµРїРѕР·РёС‚РѕСЂРёР№** вЂ” РІРµСЃСЊ РєРѕРґ Рё РєРѕРЅС„РёРіРё
4. **Ollama models** вЂ” ~97 Р“Р‘, РґРѕР»РіРѕ СЃРєР°С‡РёРІР°С‚СЊ Р·Р°РЅРѕРІРѕ
5. **~/.continue/config.json** вЂ” РєРѕРЅС„РёРіСѓСЂР°С†РёСЏ Continue

### Р РµРєРѕРјРµРЅРґСѓРµРјР°СЏ СЃС‚СЂР°С‚РµРіРёСЏ

| Р§Р°СЃС‚РѕС‚Р° | Р§С‚Рѕ | РљСѓРґР° |
|---------|-----|------|
| Р•Р¶РµРЅРµРґРµР»СЊРЅРѕ | `backup.ps1` (РєРѕРЅС„РёРіРё) | `D:\Projects\ai\backup\` |
| Р•Р¶РµРјРµСЃСЏС‡РЅРѕ | Git push | Remote (РїСЂРёРІР°С‚РЅС‹Р№ repo) |
| РџРѕСЃР»Рµ РёР·РјРµРЅРµРЅРёР№ | age keys.txt | Р’РЅРµС€РЅРёР№ РЅРѕСЃРёС‚РµР»СЊ (USB) |
| РџРѕСЃР»Рµ СѓСЃС‚Р°РЅРѕРІРєРё | Р’СЃРµ Р±РёРЅР°СЂРЅРёРєРё | Р’РЅРµС€РЅРёР№ HDD |

## Р’РѕСЃСЃС‚Р°РЅРѕРІР»РµРЅРёРµ РѕС‚РґРµР»СЊРЅС‹С… РєРѕРјРїРѕРЅРµРЅС‚РѕРІ

### РўРѕР»СЊРєРѕ Ollama

```powershell
# РћСЃС‚Р°РЅРѕРІРёС‚СЊ
Get-Process ollama | Stop-Process -Force

# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ models/ РґРёСЂРµРєС‚РѕСЂРёСЋ
# Р—Р°РїСѓСЃС‚РёС‚СЊ Р·Р°РЅРѕРІРѕ
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
```

### РўРѕР»СЊРєРѕ LiteLLM

```powershell
# РћСЃС‚Р°РЅРѕРІРёС‚СЊ
Get-Process litellm | Stop-Process -Force

# РџРµСЂРµСЃРѕР·РґР°С‚СЊ venv РµСЃР»Рё РЅСѓР¶РЅРѕ
uv venv .venv --python 3.10
uv sync

# Р—Р°РїСѓСЃС‚РёС‚СЊ
.\scripts\setup\start-litellm.bat
```

### РўРѕР»СЊРєРѕ Qdrant

```powershell
# РћСЃС‚Р°РЅРѕРІРёС‚СЊ
Get-Process qdrant | Stop-Process -Force

# Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ storage/ РµСЃР»Рё РЅСѓР¶РЅРѕ
# Р—Р°РїСѓСЃС‚РёС‚СЊ
Start-Process '.\scripts\setup\start-qdrant.bat' -WindowStyle Minimized
```

### РўРѕР»СЊРєРѕ СЃРµРєСЂРµС‚С‹ (РµСЃР»Рё keys.txt СѓС‚РµСЂСЏРЅ)

> **Р’РќРРњРђРќРР•:** Р•СЃР»Рё age keys.txt СѓС‚РµСЂСЏРЅ, СЃРµРєСЂРµС‚С‹ РЅРµРІРѕР·РјРѕР¶РЅРѕ РІРѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ.
> РќРµРѕР±С…РѕРґРёРјРѕ СЃРіРµРЅРµСЂРёСЂРѕРІР°С‚СЊ РЅРѕРІС‹Р№ keypair Рё РїРµСЂРµСЃРѕР·РґР°С‚СЊ .secrets.yaml.

```powershell
# Р“РµРЅРµСЂР°С†РёСЏ РЅРѕРІРѕРіРѕ keypair
& 'C:\Tools\age\age\age-keygen.exe' -o "$env:USERPROFILE\.config\sops\age\keys.txt"

# РџРѕР»СѓС‡РёС‚СЊ public key
$pubKey = (& 'C:\Tools\age\age\age-keygen.exe' -y "$env:USERPROFILE\.config\sops\age\keys.txt").Trim()

# РћР±РЅРѕРІРёС‚СЊ .sops.yaml СЃ РЅРѕРІС‹Рј recipient
# РЎРѕР·РґР°С‚СЊ РЅРѕРІС‹Р№ .secrets.yaml
$secrets = @"
LITELLM_API_KEY: sk-$( -join ((48..57)+(97..122) | Get-Random -Count 48 | ForEach-Object {[char]$_}))
OLLAMA_API_BASE: http://127.0.0.1:11434
"@
$secrets | & 'C:\Tools\sops\sops.exe' --encrypt --age "$pubKey" /dev/stdin > .secrets.yaml

# РћР±РЅРѕРІРёС‚СЊ CONTINUE_API_KEY
$decrypted = & 'C:\Tools\sops\sops.exe' --decrypt '.secrets.yaml'
$apiKey = ($decrypted | Select-String 'LITELLM_API_KEY:').ToString() -replace '.*:\s*',''
[Environment]::SetEnvironmentVariable('CONTINUE_API_KEY', $apiKey, 'User')
```