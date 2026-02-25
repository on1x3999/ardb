import json

# Fix popular_combos.json
with open('popular_combos.json', 'r') as f:
    combos = json.load(f)

# Normalize and merge duplicates
normalized = {}
for combo in combos:
    # Sort abilities to create a canonical key
    key = tuple(sorted(combo['abilities']))
    if key in normalized:
        normalized[key]['count'] += combo['count']
    else:
        normalized[key] = {'abilities': list(key), 'count': combo['count']}

# Calculate total for percentages
total = sum(c['count'] for c in normalized.values())

# Recalculate percentages and sort by count
result = []
for key, data in normalized.items():
    percent = round((data['count'] / total) * 100, 2)
    result.append({
        'abilities': data['abilities'],
        'count': data['count'],
        'percent': percent
    })

# Sort by count descending
result.sort(key=lambda x: x['count'], reverse=True)

# Save
with open('popular_combos.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"popular_combos.json: {len(combos)} -> {len(result)} combinations")

# Fix ability_combos.json
try:
    with open('ability_combos.json', 'r') as f:
        ability_combos = json.load(f)
    
    fixed_ability_combos = {}
    
    for ability, combos in ability_combos.items():
        normalized = {}
        for combo in combos:
            # Sort abilities but keep the clicked ability in its original position
            # Actually, for combos we should sort all abilities
            key = tuple(sorted(combo['abilities']))
            if key in normalized:
                normalized[key]['count'] += 1
            else:
                normalized[key] = {'abilities': list(key), 'count': 1}
        
        # Convert back to list
        result_list = []
        for key, data in normalized.items():
            result_list.append({
                'abilities': data['abilities'],
                'count': data['count']
            })
        
        # Sort by count
        result_list.sort(key=lambda x: x['count'], reverse=True)
        fixed_ability_combos[ability] = result_list
    
    with open('ability_combos.json', 'w') as f:
        json.dump(fixed_ability_combos, f, indent=2)
    
    print(f"ability_combos.json: fixed {len(fixed_ability_combos)} abilities")
    
except Exception as e:
    print(f"ability_combos.json error: {e}")

print("Done!")
