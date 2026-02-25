from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    # Get all links
    links = page.query_selector_all('a')
    print(f"Found {len(links)} total links")
    
    player_links = []
    for l in links:
        href = l.get_attribute('href')
        if href and '/players/' in href:
            player_links.append(href)
            print(f"Player: {href}")
    
    print(f"\nTotal player links: {len(player_links)}")
    
    # Save
    with open('player_links.json', 'w') as f:
        json.dump(player_links[:10], f, indent=2)
    print("Saved!")
