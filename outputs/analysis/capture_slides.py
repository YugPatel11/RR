from playwright.sync_api import sync_playwright
import os

html_path = 'file:///' + os.path.abspath('outputs/index.html').replace('\\', '/')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 720})
    page.goto(html_path)
    page.wait_for_timeout(1000)

    # Open presentation mode
    page.keyboard.press('p')
    page.wait_for_timeout(500)
    page.screenshot(path='outputs/presentation_slide1.png')

    # Go to slide 4 (Batters)
    page.keyboard.press('ArrowRight')
    page.keyboard.press('ArrowRight')
    page.keyboard.press('ArrowRight')
    page.wait_for_timeout(400)
    page.screenshot(path='outputs/presentation_slide4.png')

    browser.close()
    print("Saved presentation slide screenshots!")

