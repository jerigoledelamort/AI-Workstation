# Start Open WebUI
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"

# Decrypt secrets
$decrypted = & "C:\Tools\sops\sops.exe" --decrypt "D:\Projects\ai\.secrets.yaml" 2>&1
foreach ($line in $decrypted) {
    if ($line -match "^(\w+):\s*(.+)$") {
        Set-Item -Path "env:$($Matches[1])" -Value $Matches[2]
    }
}

$env:OLLAMA_BASE_URL = "http://127.0.0.1:11434"
$env:OPENAI_API_BASE_URL = "http://127.0.0.1:4000/v1"
$env:OPENAI_API_KEY = $env:LITELLM_API_KEY
$env:WEBUI_HOST = "127.0.0.1"
$env:WEBUI_PORT = "8080"
$env:DATA_DIR = "D:\Projects\ai\data\open-webui"

& "D:\Projects\ai\.venv-webui\Scripts\open-webui.exe" serve --host 127.0.0.1 --port 8080