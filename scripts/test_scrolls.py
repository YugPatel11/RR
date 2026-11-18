import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        print('Navigating to http://localhost:5173/ ...')
        await page.goto('http://localhost:5173/', wait_until='networkidle')
        await asyncio.sleep(2)

        # Test at key scroll positions across the 2000vh track
        scroll_positions = [0, 3500, 6000, 9000, 12500, 15500, 17000]
        for scroll_y in scroll_positions:
            await page.evaluate(f'window.scrollTo(0, {scroll_y})')
            await asyncio.sleep(1.2)
            prog = await page.evaluate("() => document.getElementById('meter-val') ? document.getElementById('meter-val').textContent : ''")
            await page.screenshot(path=f'redesign_screenshots/scroll_{scroll_y}_p{prog.replace(".", "_")}.png')
            print(f'Captured scroll_{scroll_y} at progress {prog}')

        print('Total console errors:', len(console_errors))
        if console_errors:
            print('Errors:', console_errors)

        await browser.close()

asyncio.run(run())
