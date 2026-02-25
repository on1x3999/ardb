from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    page.goto('https://www.abilityarena.com/games/8699469162')
    page.wait_for_timeout(5000)
    
    # Get all images
    imgs = page.query_selector_all('img')
    
    # Filter for ability icons
    ability_imgs = []
    for img in imgs:
        src = img.get_attribute('src')
        if src and 'ability_icons' in src:
            ability_imgs.append(src)
    
    print(f'Found {len(ability_imgs)} ability images')
    for i, src in enumerate(ability_imgs[:30]):
        print(f'{i}: {src}')
