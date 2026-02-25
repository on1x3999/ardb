from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    with open('matches.json', 'r') as f:
        matches_data = json.load(f)
    
    all_winners = []
    
    # Process first 5 matches
    for player_data in matches_data[:5]:
        for match_url in player_data['matches'][:2]:
            full_url = 'https://www.abilityarena.com' + match_url
            print(f'Processing: {match_url}')
            
            page.goto(full_url)
            page.wait_for_timeout(3000)
            
            # Get all ability images and levels
            imgs = page.query_selector_all('.ability-image')
            levels = page.query_selector_all('.level-icon')
            
            abilities = []
            for i, img in enumerate(imgs):
                alt = img.get_attribute('alt') or ''
                if 'empty' in alt:
                    continue
                
                level = levels[i].inner_text() if i < len(levels) else ''
                
                abilities.append({
                    'ability': alt,
                    'level': level,
                    'image_url': 'https://www.abilityarena.com' + img.get_attribute('src')
                })
            
            # Get winner info from text
            text = page.evaluate('document.body.innerText')
            lines = text.split('\n')
            
            winner_info = {
                'match_id': match_url.replace('/games/', ''),
                'player': 'Unknown',
                'hero': 'Unknown',
                'abilities': abilities[:12]  # First 12 abilities for winner
            }
            
            # Find player name
            for i, line in enumerate(lines):
                if '+100' in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        if lines[j].strip() and not lines[j].startswith('\t'):
                            winner_info['player'] = lines[j].strip()
                            if j+1 < len(lines):
                                winner_info['hero'] = lines[j+1].strip()
                            break
                    break
            
            all_winners.append(winner_info)
            print(f"  Winner: {winner_info['player']} ({winner_info['hero']})")
            print(f"  Abilities: {[(a['ability'][:30], a['level']) for a in winner_info['abilities'][:6]]}")
    
    # Save
    with open('winners_with_images.json', 'w', encoding='utf-8') as f:
        json.dump(all_winners, f, indent=2, ensure_ascii=False)
    
    print(f'\nTotal: {len(all_winners)} matches')
    print('Saved to winners_with_images.json')
