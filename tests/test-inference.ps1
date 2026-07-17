# AI Workstation Inference Test
# Tests all LiteLLM model aliases

$env:SOPS_AGE_KEY_FILE = "$env:USERPROFILE\.config\sops\age\keys.txt"
$decrypted = & "C:\Tools\sops\sops.exe" --decrypt ".secrets.yaml" 2>&1
$apiKey = ($decrypted | Select-String "LITELLM_API_KEY:").ToString() -replace '.*"([^"]+)".*','$1'

$chatModels = @("chat-low", "chat-medium", "coder-low", "coder-medium")
$embedModels = @("embed-low", "embed-medium")

$pass = 0
$fail = 0

Write-Host "=== Inference Test ===" -ForegroundColor Cyan

foreach ($model in $chatModels) {
    Write-Host -NoNewline "Testing $model... "
    try {
        $body = @{ model = $model; messages = @(@{ role="user"; content="Say OK" }); max_tokens = 10 } | ConvertTo-Json -Depth 3
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:4000/v1/chat/completions" -Method POST -Headers @{ Authorization = "Bearer $apiKey" } -ContentType "application/json" -Body $body -TimeoutSec 120
        Write-Host "PASS ($($r.usage.total_tokens) tokens)" -ForegroundColor Green
        $pass++
    } catch {
        Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red
        $fail++
    }
}

foreach ($model in $embedModels) {
    Write-Host -NoNewline "Testing $model... "
    try {
        $body = @{ model = $model; input = "test embedding" } | ConvertTo-Json -Depth 3
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:4000/v1/embeddings" -Method POST -Headers @{ Authorization = "Bearer $apiKey" } -ContentType "application/json" -Body $body -TimeoutSec 60
        Write-Host "PASS ($($r.data[0].embedding.Count) dims)" -ForegroundColor Green
        $pass++
    } catch {
        Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red
        $fail++
    }
}

Write-Host ""
Write-Host "Total: $pass passed, $fail failed" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Yellow" })
exit $fail