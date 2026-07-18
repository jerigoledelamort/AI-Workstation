# Start all AI Workstation services (Task Scheduler compatible)
$ErrorActionPreference = 'SilentlyContinue'
$logFile = 'D:\Projects\ai\logs\autostart.log'

function Log($msg) {
    $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $line = "[$ts] $msg"
    Add-Content -Path $logFile -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue
}

Log '=== AI Workstation AutoStart ==='

# 1. Ollama
Log 'Starting Ollama...'
$proc = Start-Process 'ollama' -ArgumentList 'serve' -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 3
if ($proc -and -not $proc.HasExited) {
    Log "Ollama started (PID $($proc.Id))"
} else {
    Log 'ERROR: Ollama failed to start'
}

# 2. Qdrant
Log 'Starting Qdrant...'
$proc = Start-Process 'C:\Tools\qdrant\qdrant.exe' -ArgumentList '--config-path', 'D:\Projects\ai\config\qdrant\qdrant.yaml' -WindowStyle Hidden -WorkingDirectory 'C:\Tools\qdrant' -PassThru
Start-Sleep -Seconds 3
if ($proc -and -not $proc.HasExited) {
    Log "Qdrant started (PID $($proc.Id))"
} else {
    Log 'ERROR: Qdrant failed to start'
}

# 3. LiteLLM Proxy
Log 'Starting LiteLLM Proxy...'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"

$decrypted = & 'C:\Tools\sops\sops.exe' --decrypt 'D:\Projects\ai\.secrets.yaml' 2>&1
foreach ($line in $decrypted) {
    if ($line -match '^(\w+):\s*(.+)$') {
        Set-Item -Path "env:$($Matches[1])" -Value $Matches[2]
    }
}
Log 'Secrets decrypted'

$proc = Start-Process 'D:\Projects\ai\.venv\Scripts\litellm.exe' -ArgumentList '--config', 'D:\Projects\ai\config\litellm\config.yaml', '--port', '4000', '--host', '127.0.0.1' -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 10
if ($proc -and -not $proc.HasExited) {
    Log "LiteLLM started (PID $($proc.Id))"
} else {
    Log 'ERROR: LiteLLM failed to start'
}


# 4. Router Proxy (auto-routing for Cline)
Log 'Starting Router Proxy...'
$proc = Start-Process 'D:\Projects\ai\scripts\setup\start-router.bat' -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 5
if ($proc -and -not $proc.HasExited) {
    Log "Router Proxy started (PID $($proc.Id))"
} else {
    Log 'ERROR: Router Proxy failed to start'
}

# 5. Open WebUI (via .bat wrapper for reliable env vars)
Log 'Starting Open WebUI...'
$proc = Start-Process 'D:\Projects\ai\scripts\setup\start-webui.bat' -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 30
if ($proc -and -not $proc.HasExited) {
    Log "Open WebUI started (PID $($proc.Id))"
} else {
    Log 'ERROR: Open WebUI failed to start'
}

# Verify
Log 'Verifying services...'
$services = @(
    @{Name='Ollama'; Url='http://127.0.0.1:11434/api/tags'},
    @{Name='LiteLLM'; Url='http://127.0.0.1:4000/health/liveliness'},
    @{Name='Qdrant'; Url='http://127.0.0.1:6333/healthz'},
    @{Name='Router'; Url='http://127.0.0.1:4001/health'}
    @{Name='Open WebUI'; Url='http://127.0.0.1:8080/health'}
)
foreach ($s in $services) {
    try {
        Invoke-RestMethod -Uri $s.Url -Method GET -TimeoutSec 10 | Out-Null
        Log "[OK] $($s.Name)"
    } catch {
        Log "[FAIL] $($s.Name)"
    }
}
Log '=== AutoStart complete ==='
