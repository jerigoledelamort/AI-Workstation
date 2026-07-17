# Security

## Authentication

- LiteLLM Proxy: API key (master_key, stored in SOPS-encrypted `.secrets.yaml`)
- Requests without API key are rejected (HTTP 500/401)

## Network Security

- All services bind to `127.0.0.1` only
- 6 Windows Firewall inbound block rules:
  - Port 11434 (Ollama)
  - Port 4000 (LiteLLM)
  - Port 6333, 6334 (Qdrant)
  - Port 8080 (Open WebUI)
  - Port 8000 (MkDocs)

## Secrets Management

- SOPS v3.13.2 + age v1.3.1
- age keypair at `~/.config/sops/age/keys.txt`
- `.sops.yaml` config with age recipient
- `.secrets.yaml` encrypted, gitignored

## Git Hygiene

- `.gitignore`: `.secrets.yaml`, `*.key`, `.env`, `.venv/`, `data/`, `backup/`, `logs/`
- `.gitattributes`: `* text=auto eol=lf`, `*.ps1 eol=crlf`, Git LFS for models