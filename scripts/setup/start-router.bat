@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set SOPS_AGE_KEY_FILE=%USERPROFILE%\.config\sops\age\keys.txt
for /f "delims=" %%i in ('C:\Tools\sops\sops.exe --decrypt D:\Projects\ai\.secrets.yaml') do set %%i
set LITELLM_URL=http://127.0.0.1:4000
set ROUTER_HOST=127.0.0.1
set ROUTER_PORT=4001
D:\Projects\ai\.venv\Scripts\python.exe D:\Projects\ai\scripts\ai\router_proxy.py
