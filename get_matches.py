from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    with open('player_links.json', 'r') as f:
        players = json.load(f)
    
    all_matches = []
    
    for player_url in players[:10]:
        full_url = 'https://www.abilityarena.com' + player_url
        print(f"\nVisiting: {player_url}")
        
        page.goto(full_url)
        page.wait_for_timeout(3000)
        
        # Get match links
        links = page.query_selector_all('a')
        
        player_matches = []
        for l in links:
            href = l.get_attribute('href')
            if href and '/games/' in href:
                player_matches.append(href)
        
        print(f"  Found {len(player_matches)} matches")
        
        # Get player name
        text = page.evaluate('document.body.innerText')
        lines = text.split('\n')
        player_name = lines[0] if lines else 'Unknown'
        
        all_matches.append({
            'player': player_name,
            'url': player_url,
            'matches': player_matches[:10]  # First 10 matches
        })
        
        # Save after each player
        with open('matches.json', 'w') as f:
            json.dump(all_matches, f, indent=2)
    
    print(f"\n\nTotal: {len(all_matches)} players")
    print("Saved to matches.json!")
