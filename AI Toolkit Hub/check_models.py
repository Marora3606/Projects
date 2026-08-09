#!/usr/bin/env python3
"""Test which NVIDIA NIM chat models actually work with your API key.

Sends a 1-token request to each candidate model and reports pass/fail.
Cost is negligible (max_tokens=1), and the whole run takes ~2-3 minutes.

Usage:
    cd "~/Desktop/projects/AI Toolkit Hub"
    python3 check_models.py

Output: a WORKING list you can paste straight into pages/5_Chatbot.py
"""

import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
TIMEOUT_S = 25

# Only text chat models. Embedding, vision-only, reranker, safety-guard,
# reward and translation models are excluded — they don't serve /chat/completions.
CANDIDATES = [
    "01-ai/yi-large",
    "ai21labs/jamba-1.5-large-instruct",
    "databricks/dbrx-instruct",
    "deepseek-ai/deepseek-v4-flash-0731",
    "google/gemma-2b",
    "google/gemma-3-4b-it",
    "google/gemma-3-12b-it",
    "google/gemma-4-31b-it",
    "ibm/granite-3.0-3b-a800m-instruct",
    "ibm/granite-3.0-8b-instruct",
    "meta/llama-3.1-8b-instruct",
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.2-1b-instruct",
    "meta/llama-3.2-3b-instruct",
    "meta/llama-3.3-70b-instruct",
    "microsoft/phi-3.5-moe-instruct",
    "minimaxai/minimax-m3",
    "mistralai/mistral-7b-instruct-v0.3",
    "mistralai/mistral-large",
    "mistralai/mistral-large-2-instruct",
    "mistralai/mistral-nemotron",
    "mistralai/mixtral-8x22b-v0.1",
    "moonshotai/kimi-k2.6",
    "nv-mistralai/mistral-nemo-12b-instruct",
    "nvidia/llama-3.1-nemotron-51b-instruct",
    "nvidia/llama-3.1-nemotron-70b-instruct",
    "nvidia/llama-3.1-nemotron-nano-8b-v1",
    "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "nvidia/nemotron-3-nano-30b-a3b",
    "nvidia/nemotron-3-super-120b-a12b",
    "nvidia/nemotron-mini-4b-instruct",
    "nvidia/nvidia-nemotron-nano-9b-v2",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "stepfun-ai/step-3.7-flash",
    "z-ai/glm-5.2",
    "zyphra/zamba2-7b-instruct",
]


def load_api_key() -> str:
    """Read OPENAI_API_KEY out of .streamlit/secrets.toml."""
    path = pathlib.Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"
    if not path.is_file():
        sys.exit(f"secrets.toml not found at {path}")
    match = re.search(r'OPENAI_API_KEY\s*=\s*"([^"]+)"', path.read_text(encoding="utf-8"))
    if not match:
        sys.exit("OPENAI_API_KEY not found in secrets.toml")
    return match.group(1)


def test_model(model: str, api_key: str) -> tuple[bool, str]:
    """Send a minimal request. Returns (works, detail)."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 1,
    }).encode("utf-8")

    request = urllib.request.Request(
        BASE_URL,
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S):
            return True, "ok"
    except urllib.error.HTTPError as e:
        # 404 = not available to this account, 400 = wrong params for this model,
        # 429 = rate limited (model may actually be fine — rerun later)
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, type(e).__name__


def main() -> int:
    api_key = load_api_key()
    working, broken = [], []

    print(f"Testing {len(CANDIDATES)} chat models...\n")
    for i, model in enumerate(CANDIDATES, 1):
        ok, detail = test_model(model, api_key)
        mark = "✅" if ok else "❌"
        print(f"  [{i:2}/{len(CANDIDATES)}] {mark} {model:<48} {detail}")
        (working if ok else broken).append(model)
        time.sleep(0.4)  # be polite to the API

    print(f"\n{'=' * 70}")
    print(f"WORKING: {len(working)}   FAILED: {len(broken)}")
    print("=" * 70)

    if working:
        print("\nPaste this into pages/5_Chatbot.py as your model list:\n")
        print("available_models = [")
        for m in working:
            print(f'    "{m}",')
        print("]")

    if broken:
        print(f"\nNot available on your account ({len(broken)}):")
        for m in broken:
            print(f"  - {m}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
