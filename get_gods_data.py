from playwright.sync_api import sync_playwright
import json
import re

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    page.goto('https://www.abilityarena.com/games/8699469162')
    page.wait_for_timeout(5000)
    
    # Get all hero images
    all_imgs = page.query_selector_all('img')
    
    hero_imgs = []
    for img in all_imgs:
        src = img.get_attribute('src') or ''
        alt = img.get_attribute('alt') or ''
        if 'heroes' in src:
            hero_imgs.append({'src': src, 'alt': alt})
    
    print(f'Found {len(hero_imgs)} hero images')
    for i, h in enumerate(hero_imgs[:10]):
        print(f'{i}: {h["alt"]} - {h["src"]}')
    
    # Get all ability images
    ability_imgs = page.query_selector_all('.ability-image')
    level_elems = page.query_selector_all('.level-icon')
    
    print(f'\nFound {len(ability_imgs)} ability images')
    print(f'Found {len(level_elems)} level elements')
    
    # The structure should be: for each player, 3 heroes with 4 abilities each = 12 abilities
    # Let's see if we can group them
    
    # Save raw data
    data = {
        'heroes': hero_imgs[:20],
        'total_ability_images': len(ability_imgs),
        'total_level_elements': len(level_elems)
    }
    
    with open('debug_gods.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print('\nSaved to debug_gods.json')
