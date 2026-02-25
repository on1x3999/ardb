import json

# Read source data with original order (2000 matches)
with open('all_top3_data.json', 'r', encoding='utf-8') as f:
    matches = json.load(f)

# Build ability combos - for each ability, find combos that include it
ability_combos = {}

for match in matches:
    for player in match['players']:
        for hero in player.get('heroes', []):
            abilities = [a['name'] for a in hero['abilities'][:4]]
            if len(abilities) != 4:
                continue
            
            # For each ability in the combo, add this combo
            for ability in abilities:
                if ability not in ability_combos:
                    ability_combos[ability] = []
                ability_combos[ability].append(abilities)

# Now deduplicate each ability's combos, keeping original order
fixed = {}
for ability, combos in ability_combos.items():
    normalized = {}
    for combo in combos:
        key = tuple(sorted(combo))
        if key not in normalized:
            normalized[key] = {'abilities': combo, 'count': 1}
        else:
            normalized[key]['count'] += 1
    
    # Convert to list and sort
    result_list = []
    for key, data in normalized.items():
        result_list.append({
            'abilities': data['abilities'],
            'count': data['count']
        })
    
    # Sort by count descending
    result_list.sort(key=lambda x: x['count'], reverse=True)
    fixed[ability] = result_list

# Save
with open('ability_combos.json', 'w') as f:
    json.dump(fixed, f, indent=2)

print(f"Fixed {len(fixed)} abilities")
print(f"Example - spectre_haunt combos: {len(fixed.get('custom_spectre_haunt', []))}")
