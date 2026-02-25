from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    page.goto('https://www.abilityarena.com/games/8699469162')
    page.wait_for_timeout(5000)
    
    # Get all ability images
    imgs = page.query_selector_all('.ability-image')
    
    abilities = []
    for img in imgs:
        src = img.get_attribute('src') or ''
        alt = img.get_attribute('alt') or ''
        
        # Skip empty
        if 'empty' in alt:
            continue
        
        # Find level from parent
        try:
            parent = img.evaluate('el => el.parentElement')
            if parent:
                level_elem = parent.query_selector('.level-icon')
                level = level_elem.inner_text() if level_elem else ''
            else:
                level = ''
        except:
            level = ''
        
        abilities.append({
            'src': src,
            'alt': alt,
            'level': level
        })
    
    # Print first 12 (for 1st place player)
    print('First player abilities:')
    for a in abilities[:12]:
        print(f"Ability: {a['alt']:45} Level: {a['level']}")
    
    # Save to file
    with open('ability_details.json', 'w') as f:
        json.dump(abilities, f, indent=2)
    
    print(f'\nTotal abilities: {len(abilities)}')
    print('Saved to ability_details.json')
