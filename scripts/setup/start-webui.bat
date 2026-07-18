@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
for /f "delims=" %%i in ('C:\Tools\sops\sops.exe --decrypt D:\Projects\ai\.secrets.yaml') do set %%i
set OLLAMA_BASE_URL=http://127.0.0.1:11434
set OPENAI_API_BASE_URL=http://127.0.0.1:4000/v1
set OPENAI_API_KEY=%LITELLM_API_KEY%
set WEBUI_HOST=127.0.0.1
set WEBUI_PORT=8080
set DATA_DIR=D:\Projects\ai\data\open-webui
D:\Projects\ai\.venv-webui\Scripts\open-webui.exe serve --host 127.0.0.1 --port 8080