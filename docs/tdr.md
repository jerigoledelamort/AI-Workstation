# Technology Decisions

| Component | Decision | Alternative |
|-----------|----------|-------------|
| Inference | Ollama | llama.cpp |
| API Gateway | LiteLLM Proxy | — |
| Python env | uv | conda |
| Secrets | SOPS + age | — |
| Vector DB | Qdrant | ChromaDB |
| RAG | LangChain | LlamaIndex |
| Agents | LangGraph | CrewAI |
| Docs | MkDocs Material | — |
| Chat UI | Open WebUI | — |
| MCP | Continue | — |