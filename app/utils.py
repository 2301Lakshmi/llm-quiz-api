import re
from typing import Optional
import httpx
from app.config import HTTP_TIMEOUT

def extract_submit_url(text: str, html: str, hrefs: list) -> Optional[str]:
    # check hrefs first
    if hrefs:
        for u in hrefs:
            if u and ("submit" in u or "answer" in u or "upload" in u):
                return u
    # fallback: search in html or visible text
    m = re.search(r"https?://[^\s'\"<>]+/submit[^\s'\"<>]*", html + "\n" + text)
    if m:
        return m.group(0)
    m2 = re.search(r"https?://[^\s'\"<>]+/(?:api|quiz|answer)[^\s'\"<>]*", html + "\n" + text)
    if m2:
        return m2.group(0)
    return None

def find_data_urls(html: str) -> list:
    # find links to csv/pdf/json/xlsx
    urls = re.findall(r"https?://[^\s'\"<>]+(?:\.csv|\.json|\.pdf|\.xlsx|\.xls)", html)
    return urls

async def download_bytes(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.content

def mask_secret(payload: dict) -> dict:
    out = dict(payload)
    if "secret" in out:
        out["secret"] = "****"
    return out
