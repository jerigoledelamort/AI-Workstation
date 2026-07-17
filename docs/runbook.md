# Runbook

## Daily Operations

### Start all services

```powershell
.\scripts\setup\start-all.ps1
```

### Stop all services

```powershell
.\scripts\setup\stop-all.ps1
```

### Health check

```powershell
.\scripts\monitoring\health-check.ps1
```

### VRAM/RAM monitor

```powershell
.\scripts\monitoring\vram-check.ps1
```

### Security audit

```powershell
.\tests\test-security.ps1
```

### Update models

```powershell
.\scripts\maintenance\update-models.ps1
```

### Backup

```powershell
.\scripts\backup\backup.ps1
```

## API Usage

### Chat completion

```bash
curl http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"chat-low","messages":[{"role":"user","content":"Hello"}]}'
```

### List models

```bash
curl http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer $LITELLM_API_KEY"
```

## Troubleshooting

### LiteLLM not starting
- Check `logs/litellm-stderr.log`
- Ensure `PYTHONUTF8=1` is set
- Verify API key loaded from SOPS

### Ollama not responding
- Check `OLLAMA_HOST=127.0.0.1:11434`
- Verify process: `Get-Process ollama`

### Models not loading
- Check VRAM: `nvidia-smi`
- Check disk space on model storage drive