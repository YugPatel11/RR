import os
import time
import threading
import http.server
import socketserver
from playwright.sync_api import sync_playwright

PORT = 8089
DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def start_server():
    try:
        with ThreadedTCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print("Server notice:", e)

def run_qa():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "qa_screenshots"))
    os.makedirs(screenshot_dir, exist_ok=True)

    console_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ============================================================
        # 1. Desktop Standard Test (1440x900)
        # ============================================================
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("console", lambda msg: console_errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ["error"] else None)
        page.on("pageerror", lambda err: console_errors.append(f"PAGE ERROR: {err}"))

        url = f"http://localhost:{PORT}/index.html"
        print(f"Navigating to {url} (1440x900)...")
        page.goto(url, wait_until="load")
        time.sleep(1.2)

        # A. Jump to Sources & Methodology
        print("Testing jump to Sources & Methodology...")
        page.click("#btn-jump-sources")
        time.sleep(1.5)

        # Verify Reconciliation Numbers
        rec_text = page.locator(".rnc-text").inner_text()
        print(f"Reconciliation Text: {rec_text[:70]}...")
        assert "199,208" in rec_text, "Missing 199,208 balls in reconciliation narrative"
        assert "200,999" in rec_text, "Missing 200,999 raw count in reconciliation"
        assert "38" in rec_text, "Missing 38 super over count in reconciliation"
        assert "1,753" in rec_text or "1753" in rec_text, "Missing 1,753 no-results in reconciliation"

        # Verify Unverified Assumptions Callout
        ucc_text = page.locator(".unverified-callout-card").inner_text()
        assert "157" in ucc_text, "Missing 157 Cr salary cap callout"
        assert "45" in ucc_text, "Missing 45 Cr starting purse assumption callout"
        assert "retention" in ucc_text.lower(), "Missing pending retention list callout"

        # Verify Table Rows
        table_rows = page.locator(".sources-table tbody tr").count()
        print(f"Verified {table_rows} player rows in sources table.")
        assert table_rows == 20, f"Expected 20 player rows, found {table_rows}"

        # Verify Credits Grid
        credits_count = page.locator(".credit-card").count()
        print(f"Verified {credits_count} creative credits cards.")
        assert credits_count >= 20, f"Expected at least 20 credit cards, found {credits_count}"

        page.screenshot(path=os.path.join(screenshot_dir, "desktop_sources_methodology_1440x900.png"))
        print("Saved desktop_sources_methodology_1440x900.png")

        # B. Test Low-Power Toggle
        print("Testing Low-Power Toggle...")
        btn_power = page.locator("#btn-low-power")
        btn_power.click()
        time.sleep(0.3)
        body_class = page.eval_on_selector("body", "el => el.className")
        assert "low-power-mode" in body_class, "low-power-mode class missing on body"
        btn_power.click() # toggle back

        # C. Test Present Mode (16:9 Deck)
        print("Testing Present Mode (16:9 Slide Deck)...")
        page.click("#btn-open-deck")
        time.sleep(0.5)

        # Check Active State
        modal_active = page.eval_on_selector("#present-deck-modal", "el => el.classList.contains('active')")
        assert modal_active, "Present deck modal did not open"

        # Slide 1: Pressure Definition
        slide1_title = page.locator(".deck-slide-title").inner_text()
        print(f"Slide 1 Title: {slide1_title}")
        assert "Pressure Definition" in slide1_title

        # Advance through slides
        page.click("#deck-btn-next") # Slide 2
        time.sleep(0.3)
        slide2_title = page.locator(".deck-slide-title").inner_text()
        print(f"Slide 2 Title: {slide2_title}")
        assert "Performance Measurement" in slide2_title

        page.click("#deck-btn-next") # Slide 3
        time.sleep(0.3)
        slide3_title = page.locator(".deck-slide-title").inner_text()
        print(f"Slide 3 Title: {slide3_title}")
        assert "Fair Comparisons" in slide3_title

        page.click("#deck-btn-next") # Slide 4
        time.sleep(0.3)
        slide4_title = page.locator(".deck-slide-title").inner_text()
        print(f"Slide 4 Title: {slide4_title}")
        assert "Evidence for the Top 10" in slide4_title
        page.screenshot(path=os.path.join(screenshot_dir, "desktop_present_deck_slide4_1440x900.png"))
        print("Saved desktop_present_deck_slide4_1440x900.png")

        page.click("#deck-btn-next") # Slide 5
        time.sleep(0.3)
        slide5_title = page.locator(".deck-slide-title").inner_text()
        print(f"Slide 5 Title: {slide5_title}")
        assert "Reliability & Limitations" in slide5_title

        counter_text = page.locator("#deck-counter").inner_text()
        print(f"Counter Text: {counter_text}")
        assert "5 of 5" in counter_text

        # Close Deck via ESC
        page.keyboard.press("Escape")
        time.sleep(0.4)
        modal_active_after_esc = page.eval_on_selector("#present-deck-modal", "el => el.classList.contains('active')")
        assert not modal_active_after_esc, "Present deck modal failed to close via Escape"
        page.close()

        # ============================================================
        # 2. Large Desktop Test (1920x1080)
        # ============================================================
        print("Testing Large Desktop (1920x1080)...")
        page_large = browser.new_page(viewport={"width": 1920, "height": 1080})
        page_large.goto(url, wait_until="load")
        time.sleep(1.0)

        page_large.click("#btn-open-deck")
        time.sleep(0.5)
        page_large.screenshot(path=os.path.join(screenshot_dir, "desktop_present_deck_1920x1080.png"))
        print("Saved desktop_present_deck_1920x1080.png")
        page_large.keyboard.press("Escape")
        time.sleep(0.3)

        page_large.click("#btn-jump-sources")
        time.sleep(1.2)
        page_large.screenshot(path=os.path.join(screenshot_dir, "desktop_sources_methodology_1920x1080.png"))
        print("Saved desktop_sources_methodology_1920x1080.png")
        page_large.close()

        # ============================================================
        # 3. Mobile Test (390x844)
        # ============================================================
        print("Testing Mobile (390x844)...")
        page_mobile = browser.new_page(viewport={"width": 390, "height": 844})
        page_mobile.goto(url, wait_until="load")
        time.sleep(1.0)

        # On mobile, use smooth scroll to sources or click jump button if visible
        page_mobile.evaluate("window.scrollTo(0, document.getElementById('section-sources-methodology').offsetTop)")
        time.sleep(1.0)
        page_mobile.screenshot(path=os.path.join(screenshot_dir, "mobile_sources_methodology_390x844.png"))
        print("Saved mobile_sources_methodology_390x844.png")

        # Open Present Deck
        page_mobile.evaluate("document.getElementById('btn-open-deck').click()")
        time.sleep(0.5)
        page_mobile.screenshot(path=os.path.join(screenshot_dir, "mobile_present_deck_390x844.png"))
        print("Saved mobile_present_deck_390x844.png")
        page_mobile.close()

        browser.close()

    print("\n--- QA REPORT ---")
    print(f"Total Console Errors: {len(console_errors)}")
    for err in console_errors:
        print("  -", err)
    
    assert len(console_errors) == 0, f"Found {len(console_errors)} console errors!"
    print("ALL PHASE 7 VERIFICATION CHECKS PASSED WITH 0 CONSOLE ERRORS!")

if __name__ == "__main__":
    run_qa()
