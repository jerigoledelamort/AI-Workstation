"""Agent workflow using LangGraph + Ollama.

A simple agent that can answer questions using tool calling.
"""

import os
import subprocess
import sys

def load_api_key():
    sops_exe = r"C:\Tools\sops\sops.exe"
    os.environ["SOPS_AGE_KEY_FILE"] = os.path.expanduser(r"~\.config\sops\age\keys.txt")
    result = subprocess.run([sops_exe, "--decrypt", ".secrets.yaml"], capture_output=True, text=True, cwd=r"D:\Projects\ai")
    for line in result.stdout.splitlines():
        if line.startswith("LITELLM_API_KEY:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            os.environ["LITELLM_API_KEY"] = val
            return val
    return None

load_api_key()

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

@tool
def echo(text: str) -> str:
    """Echo back the input text."""
    return f"Echo: {text}"

llm = ChatOllama(base_url="http://127.0.0.1:11434", model="qwen3:8b")
tools = [calculate, echo]

agent = create_react_agent(llm, tools)

def run_agent(question: str):
    """Run the agent with a question."""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    for msg in result["messages"]:
        print(f"[{msg.type}] {msg.content}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/rag/agent_workflow.py \"question\"")
        sys.exit(1)
    run_agent(sys.argv[1])