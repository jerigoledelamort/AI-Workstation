# Stop all AI Workstation services
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "Stopping Router Proxy..." -ForegroundColor Cyan
Get-Process | Where-Object { # Stop all AI Workstation services
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "Stopping Open WebUI..." -ForegroundColor Cyan
Get-Process | Where-Object { $_.Path -match 'open-webui' -or $_.ProcessName -match 'open-webui' } | Stop-Process -Force

Write-Host "Stopping LiteLLM..." -ForegroundColor Cyan
Get-Process -Name 'litellm' -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process | Where-Object { $_.Path -match 'litellm' } | Stop-Process -Force

Write-Host "Stopping Qdrant..." -ForegroundColor Cyan
Get-Process -Name 'qdrant' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Stopping Ollama..." -ForegroundColor Cyan
Get-Process -Name 'ollama*' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Services stopped" -ForegroundColor Green
.ProcessName -eq 'python' -and # Stop all AI Workstation services
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "Stopping Open WebUI..." -ForegroundColor Cyan
Get-Process | Where-Object { $_.Path -match 'open-webui' -or $_.ProcessName -match 'open-webui' } | Stop-Process -Force

Write-Host "Stopping LiteLLM..." -ForegroundColor Cyan
Get-Process -Name 'litellm' -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process | Where-Object { $_.Path -match 'litellm' } | Stop-Process -Force

Write-Host "Stopping Qdrant..." -ForegroundColor Cyan
Get-Process -Name 'qdrant' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Stopping Ollama..." -ForegroundColor Cyan
Get-Process -Name 'ollama*' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Services stopped" -ForegroundColor Green
.Path -match '\.venv\\' -and (Get-CimInstance Win32_Process -Filter "ProcessId=$(# Stop all AI Workstation services
$ErrorActionPreference = 'SilentlyContinue'

Write-Host "Stopping Open WebUI..." -ForegroundColor Cyan
Get-Process | Where-Object { $_.Path -match 'open-webui' -or $_.ProcessName -match 'open-webui' } | Stop-Process -Force

Write-Host "Stopping LiteLLM..." -ForegroundColor Cyan
Get-Process -Name 'litellm' -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process | Where-Object { $_.Path -match 'litellm' } | Stop-Process -Force

Write-Host "Stopping Qdrant..." -ForegroundColor Cyan
Get-Process -Name 'qdrant' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Stopping Ollama..." -ForegroundColor Cyan
Get-Process -Name 'ollama*' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Services stopped" -ForegroundColor Green
.Id)").CommandLine -match 'router_proxy' } | Stop-Process -Force

Write-Host "Stopping Open WebUI..." -ForegroundColor Cyan
Get-Process | Where-Object { $_.Path -match 'open-webui' -or $_.ProcessName -match 'open-webui' } | Stop-Process -Force

Write-Host "Stopping LiteLLM..." -ForegroundColor Cyan
Get-Process -Name 'litellm' -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process | Where-Object { $_.Path -match 'litellm' } | Stop-Process -Force

Write-Host "Stopping Qdrant..." -ForegroundColor Cyan
Get-Process -Name 'qdrant' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Stopping Ollama..." -ForegroundColor Cyan
Get-Process -Name 'ollama*' -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Services stopped" -ForegroundColor Green
