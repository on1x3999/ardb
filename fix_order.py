import json

# Read source data with original order (2000 matches)
with open('all_top3_data.json', 'r', encoding='utf-8') as f:
    matches = json.load(f)

# Extract first 4 abilities from each match (in original order)
combos_data = []
for match in matches:
    for player in match['players']:
        for hero in player.get('heroes', []):
            abilities = [a['name'] for a in hero['abilities'][:4]]
            if len(abilities) == 4:
                combos_data.append(abilities)

# Group by sorted abilities (for deduplication) but keep first order found
normalized = {}
for combo in combos_data:
    key = tuple(sorted(combo))
    if key not in normalized:
        # Keep original order (first found)
        normalized[key] = {'abilities': combo, 'count': 1}
    else:
        normalized[key]['count'] += 1

# Calculate total for percentages
total = sum(c['count'] for c in normalized.values())

# Build result
result = []
for key, data in normalized.items():
    percent = round((data['count'] / total) * 100, 2)
    result.append({
        'abilities': data['abilities'],  # Keep original order
        'count': data['count'],
        'percent': percent
    })

# Sort by count descending
result.sort(key=lambda x: x['count'], reverse=True)

# Save top 100
with open('popular_combos.json', 'w') as f:
    json.dump(result[:100], f, indent=2)

print(f"Generated {len(result)} unique combinations")
print(f"Total combos processed: {len(combos_data)}")

# Show first few
for i, r in enumerate(result[:5]):
    print(f"{i+1}. {r['abilities']} - {r['count']} ({r['percent']}%)")
