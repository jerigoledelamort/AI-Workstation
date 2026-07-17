# List models for cleanup review
Write-Host "Installed Ollama models:" -ForegroundColor Cyan
ollama list 2>&1
Write-Host "`nTo remove a model: ollama rm <model-name>" -ForegroundColor Yellow