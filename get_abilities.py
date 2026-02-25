from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    with open('matches.json', 'r') as f:
        matches_data = json.load(f)
    
    all_abilities = []
    
    # Get first 5 matches from top players
    count = 0
    for player_data in matches_data[:10]:
        for match_url in player_data['matches'][:2]:  # First 2 matches per player
            full_url = 'https://www.abilityarena.com' + match_url
            print(f"\nVisiting: {match_url}")
            
            page.goto(full_url)
            page.wait_for_timeout(3000)
            
            # Get all text content
            text = page.evaluate('document.body.innerText')
            
            # Look for rank 1st player info
            rank_1_info = ""
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if '1st' in line or '1' in line:
                    # Get context around it
                    start = max(0, i-3)
                    end = min(len(lines), i+5)
                    rank_1_info = '\n'.join(lines[start:end])
                    break
            
            all_abilities.append({
                'match_url': match_url,
                'player': player_data['player'],
                'text': text[:5000]
            })
            
            print(f"  Saved ({len(text)} chars)")
            count += 1
            
            if count >= 20:  # Limit to 20 matches
                break
        
        if count >= 20:
            break
    
    # Save
    with open('abilities.json', 'w', encoding='utf-8') as f:
        json.dump(all_abilities, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nTotal: {len(all_abilities)} matches saved!")
    print("Saved to abilities.json")
