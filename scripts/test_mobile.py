import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 390, 'height': 844})
        page = await context.new_page()

        print('Navigating on mobile...')
        await page.goto('http://localhost:5173/', wait_until='networkidle')
        await asyncio.sleep(2)

        # Scroll down to chamber
        await page.evaluate("const el = document.getElementById('section-chamber'); if (el) el.scrollIntoView();")
        await asyncio.sleep(1.5)
        await page.screenshot(path='redesign_screenshots/chamber_mobile_390.png')
        print('Captured chamber_mobile_390.png')

        await browser.close()

asyncio.run(run())

