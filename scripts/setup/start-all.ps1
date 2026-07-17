# Start all AI Workstation services
Write-Host "Starting Ollama..." -ForegroundColor Cyan
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 3
Write-Host "Starting LiteLLM Proxy..." -ForegroundColor Cyan
Start-Process "D:\Projects\ai\scripts\setup\start-litellm.bat" -WindowStyle Minimized
Start-Sleep -Seconds 10
Write-Host "Services started" -ForegroundColor Green