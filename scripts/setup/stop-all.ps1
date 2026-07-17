# Stop all AI Workstation services
Write-Host "Stopping LiteLLM..." -ForegroundColor Cyan
Get-Process -Name "litellm" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Stopping Ollama..." -ForegroundColor Cyan
Get-Process -Name "ollama" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Services stopped" -ForegroundColor Green