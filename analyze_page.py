from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    page.goto('https://www.abilityarena.com/games/8699469162')
    page.wait_for_timeout(5000)
    
    # Get all divs with data attributes
    divs = page.query_selector_all('div')
    
    for d in divs[:100]:
        data = d.get_attribute('data')
        text = d.inner_text()[:100] if d.inner_text() else ''
        if data:
            print(f'Data: {data[:200]}')
            print(f'Text: {text}')
            print('---')
