# AI Workstation Security Audit
# Run: powershell -File tests/test-security.ps1

$pass = 0
$fail = 0
$results = @()

function Check($name, $condition) {
    if ($condition) {
        $script:pass++
        $script:results += "[PASS] $name"
    } else {
        $script:fail++
        $script:results += "[FAIL] $name"
    }
}

Write-Host "=== AI Workstation Security Audit ===" -ForegroundColor Cyan

# 1. Ollama localhost-only
$ollamaHost = [Environment]::GetEnvironmentVariable("OLLAMA_HOST", "User")
Check "Ollama bind to localhost" ($ollamaHost -match "127\.0\.0\.1")

# 2. Firewall rules
$rules = Get-NetFirewallRule -DisplayName "Block-Ollama-Inbound","Block-LiteLLM-Inbound","Block-Qdrant-REST-Inbound","Block-Qdrant-gRPC-Inbound","Block-OpenWebUI-Inbound","Block-MkDocs-Inbound" -ErrorAction SilentlyContinue
Check "Firewall: 6 inbound block rules" ($rules.Count -eq 6)

# 3. LiteLLM auth
try {
    $body = @{ model = "chat-low"; messages = @(@{ role="user"; content="test" }) } | ConvertTo-Json -Depth 3
    Invoke-RestMethod -Uri "http://127.0.0.1:4000/v1/chat/completions" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 5
    Check "LiteLLM rejects unauthenticated requests" $false
} catch {
    Check "LiteLLM rejects unauthenticated requests" $true
}

# 4. SOPS encrypted
$encrypted = (Get-Content ".secrets.yaml" -TotalCount 1) -match "ENC"
Check "Secrets encrypted (SOPS)" $encrypted

# 5. age key exists
$ageKey = Test-Path "$env:USERPROFILE\.config\sops\age\keys.txt"
Check "age keypair exists" $ageKey

# 6. Gitignore
Check ".secrets.yaml in .gitignore" ([bool](git check-ignore .secrets.yaml 2>$null))
Check "*.key in .gitignore" ([bool](git check-ignore test.key 2>$null))
Check ".env in .gitignore" ([bool](git check-ignore .env 2>$null))

# 7. LiteLLM health
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:4000/health/liveliness" -Method GET -TimeoutSec 5
    Check "LiteLLM proxy healthy" ($health -match "alive")
} catch {
    Check "LiteLLM proxy healthy" $false
}

# 8. Ollama health
try {
    $ollamaHealth = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method GET -TimeoutSec 5
    Check "Ollama healthy" ($ollamaHealth.models.Count -gt 0)
} catch {
    Check "Ollama healthy" $false
}

# Results
Write-Host ""
foreach ($r in $results) {
    if ($r -match "PASS") { Write-Host $r -ForegroundColor Green }
    else { Write-Host $r -ForegroundColor Red }
}
Write-Host ""
Write-Host "Total: $pass passed, $fail failed" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Yellow" })
exit $fail