import os
from playwright.sync_api import sync_playwright

VIEWPORTS = [
    {"name": "mobile_390x844", "width": 390, "height": 844},
    {"name": "tablet_portrait_768x1024", "width": 768, "height": 1024},
    {"name": "tablet_landscape_1024x768", "width": 1024, "height": 768},
    {"name": "desktop_1440x900", "width": 1440, "height": 900},
    {"name": "desktop_large_1920x1080", "width": 1920, "height": 1080},
]

SECTIONS = [
    {"id": "hero", "selector": "#section-hero"},
    {"id": "chamber", "selector": "#section-chamber"},
    {"id": "radar", "selector": "#section-radar-duel"},
    {"id": "shortlist", "selector": "#section-shortlist"},
    {"id": "simulator", "selector": "#section-war-room"},
    {"id": "sources", "selector": "#section-sources-methodology"}
]

os.makedirs("qa_screenshots/baseline", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for vp in VIEWPORTS:
        print(f"Capturing baseline for {vp['name']}...")
        page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
        page.goto("http://localhost:5173", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Hide global floating header to prevent ghost artifacts
        page.evaluate("""() => {
            const hud = document.querySelector('.hud-header');
            if (hud) hud.style.display = 'none';
        }""")

        for sec in SECTIONS:
            loc = page.locator(sec["selector"])
            if loc.count() > 0:
                loc.scroll_into_view_if_needed()
                page.wait_for_timeout(600)
                out_path = f"qa_screenshots/baseline/{sec['id']}_{vp['name']}.png"
                loc.screenshot(path=out_path)
        
        page.close()
    browser.close()

print("All baseline captures completed!")
