from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:5173')
    page.wait_for_timeout(2000)
    
    page.evaluate('''() => {
        const hud = document.querySelector('.hud-header');
        if (hud) hud.style.display = 'none';
    }''')
    
    sec = page.locator('#section-sources-methodology')
    sec.scroll_into_view_if_needed()
    page.wait_for_timeout(1000)
    sec.screenshot(path='qa_screenshots/sources_desktop_1440.png')
    
    # Click Tab 2
    tabs = page.locator('.sources-tab-btn')
    tabs.nth(1).click()
    page.wait_for_timeout(500)
    sec.screenshot(path='qa_screenshots/sources_registry_desktop_1440.png')
    
    # Mobile
    m_page = browser.new_page(viewport={'width': 390, 'height': 844})
    m_page.goto('http://localhost:5173')
    m_page.wait_for_timeout(2000)
    m_page.evaluate('''() => {
        const hud = document.querySelector('.hud-header');
        if (hud) hud.style.display = 'none';
    }''')
    m_sec = m_page.locator('#section-sources-methodology')
    m_sec.scroll_into_view_if_needed()
    m_page.wait_for_timeout(1000)
    m_sec.screenshot(path='qa_screenshots/sources_mobile_390.png')
    
    browser.close()
print('Sources screenshots captured!')

