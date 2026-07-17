# Update all Ollama models
$models = ollama list 2>&1 | Select-Object -Skip 1
foreach ($line in $models) {
    $name = ($line -split '\s+')[0]
    if ($name) {
        Write-Host "Updating $name..." -ForegroundColor Cyan
        ollama pull $name 2>&1 | Select-Object -Last 1
    }
}
Write-Host "All models updated" -ForegroundColor Green