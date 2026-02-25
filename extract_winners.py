import json

with open('abilities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== RANK 1st ABILITY COMBINATIONS ===')
print()

winners = []

for match in data:
    text = match['text']
    
    if '1st' in text:
        # Find section between 1st and 2nd
        start = text.find('1st')
        end = text.find('2nd') if '2nd' in text else len(text)
        section = text[start:end]
        
        # Split into lines
        lines = section.split('\n')
        
        winner_info = {
            'match_id': match['match_url'].replace('/games/', ''),
            'player': None,
            'hero': None,
            'abilities': []
        }
        
        # Look for player name and hero - they appear after the +/- line
        # Format: 1st, <empty>, rounds, time, W-L, MMR, +/-, <empty>, player_name, hero, abilities
        found_mmr = False
        player_idx = None
        for i, line in enumerate(lines):
            if '+100' in line or '-100' in line or '-80' in line:
                found_mmr = True
            elif found_mmr and line.strip() and not line.startswith('\t'):
                # This should be player name
                player_idx = i
                break
        
        if player_idx is not None:
            winner_info['player'] = lines[player_idx].strip()
            if player_idx + 1 < len(lines):
                winner_info['hero'] = lines[player_idx + 1].strip()
                
                # Get abilities after hero
                abilities = []
                for j in range(player_idx + 2, len(lines)):
                    val = lines[j].strip()
                    if val.isdigit():
                        abilities.append(val)
                    elif val:
                        break
                winner_info['abilities'] = abilities
        
        winners.append(winner_info)
        print(f"Match {winner_info['match_id']}: {winner_info['player']} ({winner_info['hero']}) - {winner_info['abilities']}")

with open('winners.json', 'w', encoding='utf-8') as f:
    json.dump(winners, f, indent=2, ensure_ascii=False)

print(f'\nTotal: {len(winners)} winners')
print('Saved to winners.json')
