import os
import json
from typing import Any, Dict, Optional
from app.config import OPENAI_API_KEY
import httpx

# Minimal LLM wrapper using OpenAI REST (works with OPENAI_API_KEY)
# You may replace with official openai python client if preferred.

OPENAI_API_KEY = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "You are a JSON-only data analysis assistant. "
    "Input: a problem description and optionally small CSV/JSON content. "
    "Output STRICTLY: JSON with keys 'type' and 'answer'. "
    "type is one of 'number','string','json','file'. No explanation."
)

async def ask_llm(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 1024) -> Optional[Dict[str, Any]]:
    """
    If OPENAI_API_KEY not set, return None to let solver fallback to built-in handlers.
    """
    if not OPENAI_API_KEY:
        return None

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        j = r.json()
        txt = j["choices"][0]["message"]["content"]
        # Try to parse JSON from the model's output
        try:
            return json.loads(txt)
        except Exception:
            # Try to extract first {...} block
            import re
            m = re.search(r"\{[\s\S]*\}", txt)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception:
                    return None
            return None
