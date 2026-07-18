# AI Workstation Health Check
$services = @(
    @{ Name="Ollama"; Url="http://127.0.0.1:11434/api/tags" },
    @{ Name="LiteLLM"; Url="http://127.0.0.1:4000/health/liveliness" },
    @{ Name="Qdrant"; Url="http://127.0.0.1:6333/healthz" },
    @{ Name="Router"; Url="http://127.0.0.1:4001/health" },
    @{ Name="Open WebUI"; Url="http://127.0.0.1:8080/health" }
)
$allOk = $true
foreach ($s in $services) {
    try {
        $r = Invoke-RestMethod -Uri $s.Url -Method GET -TimeoutSec 5
        Write-Host "[OK] $($s.Name)" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] $($s.Name)" -ForegroundColor Red
        $allOk = $false
    }
}
if ($allOk) { Write-Host "`nAll services healthy" -ForegroundColor Green; exit 0 }
else { Write-Host "`nSome services down" -ForegroundColor Red; exit 1 }