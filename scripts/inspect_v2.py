import asyncio
from playwright.async_api import async_playwright
import os

os.makedirs('redesign_screenshots', exist_ok=True)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop 1440x900
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)

        print('Navigating to http://localhost:5173/ ...')
        await page.goto('http://localhost:5173/', wait_until='networkidle')
        await asyncio.sleep(2)

        # 01 Hero
        await page.screenshot(path='redesign_screenshots/01_hero_1440.png')
        print('Captured 01_hero_1440.png')

        # 02 Formula (scroll ~800px)
        await page.evaluate('window.scrollTo(0, 800)')
        await asyncio.sleep(1)
        await page.screenshot(path='redesign_screenshots/02_formula_1440.png')
        print('Captured 02_formula_1440.png')

        # 03 Band 1 (scroll ~1800px)
        await page.evaluate('window.scrollTo(0, 1800)')
        await asyncio.sleep(1)
        await page.screenshot(path='redesign_screenshots/03_band1_1440.png')
        print('Captured 03_band1_1440.png')

        # 04 Band 2 (scroll ~2800px)
        await page.evaluate('window.scrollTo(0, 2800)')
        await asyncio.sleep(1)
        await page.screenshot(path='redesign_screenshots/04_band2_1440.png')
        print('Captured 04_band2_1440.png')

        # 05 Band 3 (scroll ~3800px)
        await page.evaluate('window.scrollTo(0, 3800)')
        await asyncio.sleep(1)
        await page.screenshot(path='redesign_screenshots/05_band3_1440.png')
        print('Captured 05_band3_1440.png')

        # 06 Band 4 (scroll ~4800px)
        await page.evaluate('window.scrollTo(0, 4800)')
        await asyncio.sleep(1)
        await page.screenshot(path='redesign_screenshots/06_band4_1440.png')
        print('Captured 06_band4_1440.png')

        # 07 Chamber of 10 Pillars (scroll into chamber ~5800px)
        await page.evaluate("document.getElementById('section-chamber').scrollIntoView()")
        await asyncio.sleep(2)
        await page.screenshot(path='redesign_screenshots/07_chamber_1440.png')
        print('Captured 07_chamber_1440.png')

        # 07b Chamber Bowlers Toggle
        await page.click('#btn-toggle-bowlers')
        await asyncio.sleep(1.5)
        await page.screenshot(path='redesign_screenshots/07b_chamber_bowlers_1440.png')
        print('Captured 07b_chamber_bowlers_1440.png')

        # 08 Radar Duel
        await page.evaluate("document.getElementById('section-radar-duel').scrollIntoView()")
        await asyncio.sleep(1.5)
        await page.screenshot(path='redesign_screenshots/08_radar_duel_1440.png')
        print('Captured 08_radar_duel_1440.png')

        # 09 Shortlist Table
        await page.evaluate("document.getElementById('section-shortlist').scrollIntoView()")
        await asyncio.sleep(1.5)
        await page.screenshot(path='redesign_screenshots/09_shortlist_1440.png')
        print('Captured 09_shortlist_1440.png')

        # 2. Mobile 390x844
        m_context = await browser.new_context(viewport={'width': 390, 'height': 844})
        m_page = await m_context.new_page()
        await m_page.goto('http://localhost:5173/', wait_until='networkidle')
        await asyncio.sleep(2)

        await m_page.screenshot(path='redesign_screenshots/mobile_01_hero.png')
        print('Captured mobile_01_hero.png')

        await m_page.evaluate("document.getElementById('section-chamber').scrollIntoView()")
        await asyncio.sleep(1.5)
        await m_page.screenshot(path='redesign_screenshots/mobile_07_chamber.png')
        print('Captured mobile_07_chamber.png')

        await browser.close()
        print('Console errors encountered:', console_errors)

asyncio.run(run())

