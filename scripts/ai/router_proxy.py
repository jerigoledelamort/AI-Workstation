# -*- coding: utf-8 -*-
"""
AI Workstation Router Proxy.

Sits between Cline (or any OpenAI-compatible client) and LiteLLM.
Exposes smart model aliases that auto-route based on task complexity.

Architecture:
    Cline (4001) -> Router Proxy -> LiteLLM (4000) -> Ollama (11434)

Models exposed:
    auto           - Automatic complexity-based routing
    preset-light   - Always coder-low  (qwen2.5-coder:7b)
    preset-medium  - Always coder-medium (deepseek-coder-v2:lite)
    preset-heavy   - Always coder-high  (qwen3-coder:30b)
    coder-low      - Passthrough to LiteLLM
    coder-medium   - Passthrough to LiteLLM
    coder-high     - Passthrough to LiteLLM
    chat-low       - Passthrough to LiteLLM
    chat-medium    - Passthrough to LiteLLM
    chat-high      - Passthrough to LiteLLM
"""

import re
import os
import sys
import json
import time
import logging
from typing import Optional

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import uvicorn

# --- Configuration ---

LITELLM_URL = os.environ.get("LITELLM_URL", "http://127.0.0.1:4000")
ROUTER_PORT = int(os.environ.get("ROUTER_PORT", "4001"))
ROUTER_HOST = os.environ.get("ROUTER_HOST", "127.0.0.1")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")

# Model mapping: alias -> LiteLLM model
MODEL_MAP = {
    "preset-light": "coder-low",
    "preset-medium": "coder-medium",
    "preset-heavy": "coder-high",
    "auto": None,  # Determined dynamically
    # Passthrough aliases
    "coder-low": "coder-low",
    "coder-medium": "coder-medium",
    "coder-high": "coder-high",
    "chat-low": "chat-low",
    "chat-medium": "chat-medium",
    "chat-high": "chat-high",
}

# --- Complexity Analysis ---

HEAVY_KEYWORDS = [
    "refactor", "architecture", "design", "rewrite", "migrate", "restructure",
    "optimize", "performance", "scalab", "concurrent", "async", "thread",
    "database schema", "migration", "overhaul", "redesign", "complete",
    "implement entire", "build from scratch", "full stack", "end to end",
]

MEDIUM_KEYWORDS = [
    "fix", "implement", "add", "create", "update", "modify", "debug",
    "error", "exception", "handle", "validate", "parse", "convert",
    "extract", "generate", "configure", "setup", "install", "deploy",
    "test", "unit test", "integration", "endpoint", "api", "route",
]

LIGHT_KEYWORDS = [
    "rename", "comment", "format", "lint", "typo", "import", "log",
    "print", "console", "simple", "quick", "small",
]


def analyze_complexity(messages: list) -> str:
    """
    Analyze message content and return complexity level: 'heavy', 'medium', 'light'.

    Heuristics:
    1. Keyword matching (strong signal)
    2. Total content length (context size)
    3. Code block count (more code = more complex)
    4. Number of files mentioned
    """
    full_text = ""
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    full_text += part.get("text", "")
        else:
            full_text += str(content)

    text_lower = full_text.lower()
    total_chars = len(full_text)

    code_blocks = len(re.findall(r"```\w*", full_text))
    file_refs = len(re.findall(r"[\w/\\]+\.\w{1,5}[\s,)]", full_text))

    score = 0

    # Keyword scoring
    for kw in HEAVY_KEYWORDS:
        if kw in text_lower:
            score += 3
    for kw in MEDIUM_KEYWORDS:
        if kw in text_lower:
            score += 1
    for kw in LIGHT_KEYWORDS:
        if kw in text_lower:
            score -= 1

    # Content length scoring
    if total_chars > 10000:
        score += 4
    elif total_chars > 5000:
        score += 2
    elif total_chars > 2000:
        score += 1

    # Code block scoring
    score += min(code_blocks * 2, 6)

    # File reference scoring
    score += min(file_refs, 3)

    if score >= 6:
        return "heavy"
    elif score >= 2:
        return "medium"
    else:
        return "light"


def select_model(requested_model: str, messages: list) -> str:
    """Select the actual LiteLLM model based on requested alias and content."""
    if requested_model == "auto":
        complexity = analyze_complexity(messages)
        model_map = {
            "heavy": "coder-high",
            "medium": "coder-medium",
            "light": "coder-low",
        }
        selected = model_map[complexity]
        logger.info(f"AUTO ROUTE: complexity={complexity} -> model={selected}")
        return selected

    if requested_model in MODEL_MAP and MODEL_MAP[requested_model]:
        return MODEL_MAP[requested_model]

    return requested_model


# --- Logging ---

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("router")

try:
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(
        os.path.join(log_dir, "router.log"), encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)
except Exception:
    pass


# --- FastAPI App ---

app = FastAPI(title="AI Workstation Router", version="1.0.0")


@app.get("/v1/models")
@app.get("/models")
async def list_models():
    """Return available models (OpenAI-compatible)."""
    models = [
        {"id": "auto", "object": "model", "owned_by": "router"},
        {"id": "preset-light", "object": "model", "owned_by": "router"},
        {"id": "preset-medium", "object": "model", "owned_by": "router"},
        {"id": "preset-heavy", "object": "model", "owned_by": "router"},
        {"id": "coder-low", "object": "model", "owned_by": "litellm"},
        {"id": "coder-medium", "object": "model", "owned_by": "litellm"},
        {"id": "coder-high", "object": "model", "owned_by": "litellm"},
        {"id": "chat-low", "object": "model", "owned_by": "litellm"},
        {"id": "chat-medium", "object": "model", "owned_by": "litellm"},
        {"id": "chat-high", "object": "model", "owned_by": "litellm"},
    ]
    return {"object": "list", "data": models}


@app.get("/health")
@app.get("/health/liveliness")
async def health():
    return {"status": True, "router": "alive"}


@app.post("/v1/chat/completions")
@app.post("/chat/completions")
async def chat_completions(request: Request):
    """Forward chat completion request to LiteLLM with model routing."""
    body = await request.json()

    requested_model = body.get("model", "auto")
    messages = body.get("messages", [])

    actual_model = select_model(requested_model, messages)
    body["model"] = actual_model

    stream = body.get("stream", False)
    logger.info(
        f"REQUEST model={requested_model} -> {actual_model} | "
        f"messages={len(messages)} | stream={stream}"
    )

    headers = {"Content-Type": "application/json"}
    if LITELLM_API_KEY:
        headers["Authorization"] = f"Bearer {LITELLM_API_KEY}"

    url = f"{LITELLM_URL}/v1/chat/completions"

    if stream:
        async def stream_generator():
            start = time.time()
            try:
                async with httpx.AsyncClient(timeout=300.0) as client:
                    async with client.stream(
                        "POST", url, json=body, headers=headers
                    ) as response:
                        if response.status_code != 200:
                            error_body = await response.aread()
                            logger.error(
                                f"STREAM ERROR {response.status_code}: {error_body[:200]}"
                            )
                            yield f"data: {json.dumps({'error': {'message': error_body.decode('utf-8', errors='replace')[:500], 'code': response.status_code}})}\n\n"
                            return

                        async for line in response.aiter_lines():
                            if line:
                                yield f"{line}\n\n"
            except Exception as e:
                logger.error(f"STREAM EXCEPTION: {e}")
                yield f"data: {json.dumps({'error': {'message': str(e)}})}\n\n"
            finally:
                elapsed = time.time() - start
                logger.info(f"STREAM DONE in {elapsed:.1f}s")

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accelerate-Buffering": "no",
            },
        )
    else:
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(url, json=body, headers=headers)

            elapsed = time.time() - start
            logger.info(f"RESPONSE {response.status_code} in {elapsed:.1f}s")

            if response.status_code != 200:
                return JSONResponse(
                    status_code=response.status_code,
                    content=response.json(),
                )

            result = response.json()
            if "model" in result:
                result["router"] = {
                    "requested": requested_model,
                    "selected": actual_model,
                    "elapsed_s": round(elapsed, 2),
                }
            return result
        except httpx.TimeoutException:
            logger.error("TIMEOUT after 300s")
            raise HTTPException(status_code=504, detail="LiteLLM timeout (300s)")
        except Exception as e:
            logger.error(f"ERROR: {e}")
            raise HTTPException(status_code=502, detail=str(e))


@app.api_route(
    "/v1/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
)
@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
)
async def passthrough(path: str, request: Request):
    """Pass through any other API calls to LiteLLM."""
    url = f"{LITELLM_URL}/{path}"
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)

    body = await request.body()

    query_params = str(request.query_params)
    if query_params:
        url = f"{url}?{query_params}"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.request(
            request.method, url, content=body, headers=headers
        )

    content_type = response.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        return JSONResponse(status_code=response.status_code, content=response.json())
    return JSONResponse(status_code=response.status_code, content=response.text)


if __name__ == "__main__":
    # Decrypt API key from SOPS if not set
    if not LITELLM_API_KEY:
        try:
            import subprocess
            sops_path = r"C:\Tools\sops\sops.exe"
            secrets_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "..", "..", ".secrets.yaml"
            )
            result = subprocess.run(
                [sops_path, "--decrypt", secrets_path],
                capture_output=True, text=True, timeout=10,
            )
            for line in result.stdout.splitlines():
                if line.startswith("LITELLM_API_KEY:"):
                    LITELLM_API_KEY = line.split(":", 1)[1].strip()
                    os.environ["LITELLM_API_KEY"] = LITELLM_API_KEY
                    break
        except Exception as e:
            logger.warning(f"Could not decrypt SOPS: {e}")

    logger.info(f"Starting Router Proxy on {ROUTER_HOST}:{ROUTER_PORT}")
    logger.info(f"LiteLLM backend: {LITELLM_URL}")
    logger.info(f"API key: {'set' if LITELLM_API_KEY else 'NOT SET'}")
    logger.info("Models: auto, preset-light, preset-medium, preset-heavy, + passthrough")

    uvicorn.run(
        app,
        host=ROUTER_HOST,
        port=ROUTER_PORT,
        log_level="info",
        access_log=False,
    )
