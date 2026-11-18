import os
import time
from playwright.sync_api import sync_playwright

def inspect():
    screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "live_browser_screenshots"))
    os.makedirs(screenshot_dir, exist_ok=True)

    console_logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: console_logs.append(f"ERROR: {err}"))

        url = "http://localhost:5173/"
        print(f"Loading {url}...")
        page.goto(url, wait_until="load")
        time.sleep(1.5)

        # 1. Hero
        page.screenshot(path=os.path.join(screenshot_dir, "01_hero.png"))

        # Scroll positions
        sections = [
            ("section-formula", "02_formula.png"),
            ("section-band-1", "03_band1.png"),
            ("section-band-2", "04_band2.png"),
            ("section-band-3", "05_band3.png"),
            ("section-band-4", "06_band4.png"),
            ("section-chamber", "07_chamber.png"),
            ("section-radar-duel", "08_radar_duel.png"),
            ("section-shortlist", "09_shortlist.png"),
            ("section-war-room", "10_war_room.png"),
            ("section-sources-methodology", "11_sources.png")
        ]

        for sec_id, filename in sections:
            page.evaluate(f"document.getElementById('{sec_id}').scrollIntoView()")
            time.sleep(1.0)
            page.screenshot(path=os.path.join(screenshot_dir, filename))
            print(f"Captured {filename}")

        # Check Chamber pillars hover/click
        page.evaluate("document.getElementById('section-chamber').scrollIntoView()")
        time.sleep(1.0)
        # click first pillar or simulate click on canvas
        page.mouse.click(720, 500)
        time.sleep(0.5)
        page.screenshot(path=os.path.join(screenshot_dir, "07b_chamber_clicked.png"))

        # Open Present Mode
        page.evaluate("document.getElementById('btn-open-deck').click()")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(screenshot_dir, "12_present_deck_slide1.png"))

        page.click("#deck-btn-next")
        time.sleep(0.3)
        page.screenshot(path=os.path.join(screenshot_dir, "12_present_deck_slide2.png"))

        browser.close()

    print("\nConsole logs during live browsing:")
    for l in console_logs:
        print(" ", l)

if __name__ == "__main__":
    inspect()

