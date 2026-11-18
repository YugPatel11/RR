import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    os.makedirs('redesign_screenshots', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Test (1440x900)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        print('Navigating to http://localhost:5173/ ...')
        await page.goto('http://localhost:5173/', wait_until='networkidle')
        await asyncio.sleep(2)

        # Scroll to sections and capture
        sections = [
            ('chamber', '#section-chamber'),
            ('radar', '#section-radar-duel'),
            ('shortlist_bento', '#section-shortlist'),
            ('warroom_simulator', '#section-war-room'),
            ('sources_pipeline', '#section-sources-methodology'),
            ('faq', '#section-warroom-faq'),
            ('executive_cta_footer', '#section-executive-cta')
        ]

        for name, selector in sections:
            el = await page.query_selector(selector)
            if el:
                await el.scroll_into_view_if_needed()
                await asyncio.sleep(1.2)
                await page.screenshot(path=f'redesign_screenshots/desktop_{name}.png')
                print(f'Captured desktop_{name}.png')

        # Test Shortlist Table toggle
        btn_table = await page.query_selector('#btn-view-table')
        if btn_table:
            await btn_table.click()
            await asyncio.sleep(0.5)
            await page.screenshot(path='redesign_screenshots/desktop_shortlist_table.png')
            print('Captured desktop_shortlist_table.png')

        # Test Sources Tab 2 (Registry)
        tab_reg = await page.query_selector('[data-tab="tab-registry"]')
        if tab_reg:
            await tab_reg.click()
            await asyncio.sleep(0.5)
            await page.screenshot(path='redesign_screenshots/desktop_sources_registry.png')
            print('Captured desktop_sources_registry.png')

        await context.close()

        # 2. Mobile Test (390x844 - iPhone 14)
        mobile_context = await browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
        mobile_page = await mobile_context.new_page()
        mobile_errors = []
        mobile_page.on("console", lambda msg: mobile_errors.append(msg.text) if msg.type == "error" else None)
        mobile_page.on("pageerror", lambda err: mobile_errors.append(str(err)))

        await mobile_page.goto('http://localhost:5173/', wait_until='networkidle')
        await asyncio.sleep(2)

        for name, selector in sections:
            el = await mobile_page.query_selector(selector)
            if el:
                await el.scroll_into_view_if_needed()
                await asyncio.sleep(1.0)
                await mobile_page.screenshot(path=f'redesign_screenshots/mobile_{name}.png')
                print(f'Captured mobile_{name}.png')

        await mobile_context.close()
        await browser.close()

        print('=== TEST REPORT ===')
        print(f'Desktop Console Errors: {len(console_errors)}')
        if console_errors:
            for err in console_errors:
                print('  Desktop Error:', err)
        print(f'Mobile Console Errors: {len(mobile_errors)}')
        if mobile_errors:
            for err in mobile_errors:
                print('  Mobile Error:', err)

asyncio.run(run())

