import json
import os
import urllib.request

# Create images directory
os.makedirs('images/heroes', exist_ok=True)
os.makedirs('images/abilities', exist_ok=True)

# Load data
with open('winners_final.json', 'r') as f:
    data = json.load(f)

# Collect all unique URLs
hero_urls = set()
ability_urls = set()

for match in data:
    for god in match.get('gods', []):
        # Hero image
        if god.get('image'):
            hero_urls.add(god['image'])
        
        # Ability images
        for abil in god.get('abilities', []):
            if abil.get('image'):
                ability_urls.add(abil['image'])

print(f"Found {len(hero_urls)} hero images and {len(ability_urls)} ability images")

# Download heroes
print("\nDownloading heroes...")
for i, url in enumerate(hero_urls):
    filename = url.split('/')[-1]
    path = f"images/heroes/{filename}"
    if not os.path.exists(path):
        try:
            urllib.request.urlretrieve(url, path)
            print(f"  {i+1}/{len(hero_urls)}: {filename}")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"  {i+1}/{len(hero_urls)}: {filename} (exists)")

# Download abilities
print("\nDownloading abilities...")
for i, url in enumerate(ability_urls):
    filename = url.split('/')[-1]
    path = f"images/abilities/{filename}"
    if not os.path.exists(path):
        try:
            urllib.request.urlretrieve(url, path)
            print(f"  {i+1}/{len(ability_urls)}: {filename}")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"  {i+1}/{len(ability_urls)}: {filename} (exists)")

print("\nDone!")
