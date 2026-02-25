from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    page.goto('https://www.abilityarena.com/games/8699469162')
    page.wait_for_timeout(5000)
    
    # Get all ability elements
    elems = page.query_selector_all('.ability-image')
    
    results = []
    for img in elems:
        alt = img.get_attribute('alt') or ''
        if 'empty' in alt:
            continue
        
        try:
            parent = img.evaluate('el => el.parentElement')
            if parent:
                level_span = parent.query_selector('.level-icon')
                if level_span:
                    level = level_span.inner_text()
                else:
                    level = ''
                
                is_ult = 'ultimate' in parent.inner_html()
                
                results.append({
                    'ability': alt,
                    'level': level,
                    'is_ultimate': is_ult
                })
        except Exception as e:
            results.append({'ability': alt, 'level': '', 'error': str(e)})
    
    # Print first 12 (for winner)
    print('Winner (1st place) abilities:')
    for r in results[:12]:
        print(f"{r['ability']:45} Level: {r.get('level', ''):3}")
    
    with open('winner_abilities.json', 'w') as f:
        json.dump(results[:12], f, indent=2)
    
    print(f'\nSaved first 12 abilities to winner_abilities.json')
