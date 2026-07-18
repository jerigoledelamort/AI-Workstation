@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
D:\Projects\ai\.venv-mcp\Scripts\python.exe D:\Projects\ai\tools\ghidramcp\bridge_mcp_ghidra.py --transport sse --mcp-host 127.0.0.1 --mcp-port 8081 --ghidra-server http://127.0.0.1:8080/
