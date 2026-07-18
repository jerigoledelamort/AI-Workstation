# Stop all AI Workstation services
Write-Host "Stopping Open WebUI..." -ForegroundColor Cyan
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "open_webui" } | Stop-Process -Force

Write-Host "Stopping LiteLLM..." -ForegroundColor Cyan
Get-Process -Name "litellm" -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Stopping Qdrant..." -ForegroundColor Cyan
Get-Process -Name "qdrant" -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Stopping Ollama..." -ForegroundColor Cyan
Get-Process -Name "ollama" -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Services stopped" -ForegroundColor Green