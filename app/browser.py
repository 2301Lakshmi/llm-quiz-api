from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from typing import Dict, Any

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from typing import Dict, Any

async def render_page(url: str, timeout: int = 90000) -> Dict[str, Any]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"], headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=timeout)
        except PlaywrightTimeoutError:
            pass

        html = await page.content()

        # SAFE visible text extraction
        try:
            visible = await page.inner_text("body")
        except:
            visible = ""

        hrefs = await page.eval_on_selector_all(
            "a[href], form[action]", "els => els.map(e => e.href || e.action)"
        )
        scripts = await page.eval_on_selector_all(
            "script", "els => els.map(s => s.innerText || '')"
        )

        await browser.close()
        return {"html": html, "text": visible, "hrefs": hrefs, "scripts": scripts}

