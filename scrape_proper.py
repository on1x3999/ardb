from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    page = context.pages[0]
    
    with open('matches.json', 'r') as f:
        matches_data = json.load(f)
    
    all_matches = []
    
    # Process first 5 matches (2 each player)
    count = 0
    for player_data in matches_data[:5]:
        for match_url in player_data['matches'][:2]:
            full_url = 'https://www.abilityarena.com' + match_url
            print(f'Processing: {match_url}')
            
            page.goto(full_url)
            page.wait_for_timeout(3000)
            
            # Get page text for winner info
            text = page.evaluate('document.body.innerText')
            lines = text.split('\n')
            
            # Find winner (Rank 1st)
            winner_name = ''
            winner_god = ''
            for i, line in enumerate(lines):
                if '+100' in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        if lines[j].strip() and not lines[j].startswith('\t'):
                            winner_name = lines[j].strip()
                            if j+1 < len(lines):
                                winner_god = lines[j+1].strip()
                            break
                    break
            
            # Get all hero and ability images
            all_imgs = page.query_selector_all('img')
            
            heroes = []
            abilities = []
            
            for img in all_imgs:
                src = img.get_attribute('src') or ''
                alt = img.get_attribute('alt') or ''
                
                if '/images/heroes/' in src:
                    hero_name = src.replace('/images/heroes/', '').replace('.png', '').replace('npc_dota_hero_', '')
                    heroes.append({
                        'name': hero_name,
                        'image': 'https://www.abilityarena.com' + src
                    })
                elif '/images/ability_icons/' in src and alt and 'empty' not in alt:
                    abilities.append({
                        'name': alt,
                        'image': 'https://www.abilityarena.com' + src
                    })
            
            # Get level elements
            level_elems = page.query_selector_all('.level-icon')
            levels = [elem.inner_text() for elem in level_elems]
            
            # 5 gods per player, 4 abilities each = 20 abilities
            gods_data = []
            
            # Take first 5 heroes for winner (20 abilities)
            winner_gods = heroes[:5]
            winner_abilities = abilities[:20]
            
            for god_idx in range(5):
                god_name = winner_gods[god_idx]['name'] if god_idx < len(winner_gods) else 'unknown'
                god_image = winner_gods[god_idx]['image'] if god_idx < len(winner_gods) else ''
                
                # Get 4 abilities for this god
                god_abilities = []
                for abil_idx in range(4):
                    abil_idx_global = god_idx * 4 + abil_idx
                    if abil_idx_global < len(winner_abilities):
                        abil = winner_abilities[abil_idx_global]
                        level = levels[abil_idx_global] if abil_idx_global < len(levels) else '0'
                        god_abilities.append({
                            'name': abil['name'],
                            'level': level,
                            'image': abil['image']
                        })
                
                gods_data.append({
                    'name': god_name,
                    'image': god_image,
                    'abilities': god_abilities
                })
            
            match_info = {
                'match_id': match_url.replace('/games/', ''),
                'winner': winner_name,
                'god': winner_god,
                'gods': gods_data
            }
            
            all_matches.append(match_info)
            print(f"  Winner: {winner_name} ({winner_god})")
            print(f"  Gods: {[g['name'] for g in gods_data]}")
            
            count += 1
            if count >= 10:
                break
        
        if count >= 10:
            break
    
    # Save
    with open('winners_final.json', 'w', encoding='utf-8') as f:
        json.dump(all_matches, f, indent=2, ensure_ascii=False)
    
    print(f'\nTotal: {len(all_matches)} matches saved')
    print('Saved to winners_final.json')
