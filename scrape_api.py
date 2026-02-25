import json
import urllib.request
import urllib.error

def fetch_match(match_id):
    url = f"https://www.abilityarena.com/api/games/{match_id}"
    try:
        with urllib.request.urlopen(url, timeout=100) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {match_id}: {e}")
        return None

# Load matches
with open('matches.json', 'r') as f:
    matches_data = json.load(f)

all_matches = []
count = 0

for player_data in matches_data[:5]:
    for match_url in player_data['matches'][:2]:
        match_id = match_url.replace('/games/', '')
        print(f"Fetching match {match_id}...")
        
        data = fetch_match(match_id)
        if not data:
            continue
        
        # Find winner (place == 1)
        winner = None
        for player in data.get('players', []):
            if player.get('place') == 1:
                winner = player
                break
        
        if not winner:
            print(f"  No winner found")
            continue
        
        # Build winner data
        winner_info = {
            'match_id': match_id,
            'winner': winner.get('username'),
            'god': winner.get('god'),
            'gods': []
        }
        
        # Process heroes
        for hero in winner.get('heroes', []):
            hero_name = hero.get('hero_name', '').replace('npc_dota_hero_', '')
            
            # Get abilities
            abilities = []
            for abil in hero.get('abilities', []):
                abilities.append({
                    'name': abil.get('ability_name'),
                    'level': str(abil.get('ability_level')),
                    'icon': abil.get('icon'),
                    'is_ultimate': abil.get('is_ultimate', False)
                })
            
            winner_info['gods'].append({
                'name': hero_name,
                'tier': hero.get('tier'),
                'abilities': abilities
            })
        
        all_matches.append(winner_info)
        print(f"  Winner: {winner_info['winner']} ({winner_info['god']})")
        print(f"  Heroes: {len(winner_info['gods'])}")
        
        count += 1
        if count >= 10:
            break
    
    if count >= 10:
        break

# Save
with open('winners_api.json', 'w', encoding='utf-8') as f:
    json.dump(all_matches, f, indent=2, ensure_ascii=False)

print(f"\nTotal: {len(all_matches)} matches saved to winners_api.json")
