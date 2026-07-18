# Start all AI Workstation services
Write-Host "Starting Ollama..." -ForegroundColor Cyan
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 3

Write-Host "Starting Qdrant..." -ForegroundColor Cyan
Start-Process "D:\Projects\ai\scripts\setup\start-qdrant.bat" -WindowStyle Minimized
Start-Sleep -Seconds 3

Write-Host "Starting LiteLLM Proxy..." -ForegroundColor Cyan
Start-Process "D:\Projects\ai\scripts\setup\start-litellm.bat" -WindowStyle Minimized
Start-Sleep -Seconds 10

Write-Host "Starting Open WebUI..." -ForegroundColor Cyan
Start-Process "D:\Projects\ai\scripts\setup\start-webui.bat" -WindowStyle Minimized
Start-Sleep -Seconds 5

Write-Host "Services started" -ForegroundColor Green
Write-Host "  Ollama:     http://127.0.0.1:11434"
Write-Host "  Qdrant:     http://127.0.0.1:6333"
Write-Host "  LiteLLM:    http://127.0.0.1:4000"
Write-Host "  Open WebUI: http://127.0.0.1:8080"