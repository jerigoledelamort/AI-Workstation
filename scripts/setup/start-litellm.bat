@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
for /f "delims=" %%i in ('C:\Tools\sops\sops.exe --decrypt D:\Projects\ai\.secrets.yaml') do set %%i
D:\Projects\ai\.venv\Scripts\litellm.exe --config D:\Projects\ai\config\litellm\config.yaml --port 4000 --host 127.0.0.1
