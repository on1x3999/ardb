import urllib.request
import json
import re

# Get player page
url = 'https://www.abilityarena.com/players/76561198194078103'
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')
with urllib.request.urlopen(req, timeout=10) as response:
    html = response.read().decode()
    
# Look for window.__INITIAL_STATE__
match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', html, re.DOTALL)
if match:
    print("Found __INITIAL_STATE__")
    data = json.loads(match.group(1))
    print("Keys:", list(data.keys()))
else:
    print("No __INITIAL_STATE__ found")
    
# Also try different patterns
patterns = [
    r'data-json="([^"]+)"',
    r'window\.data\s*=\s*({.*?})',
    r'window\.initialData\s*=\s*({.*?})',
]

for p in patterns:
    m = re.search(p, html)
    if m:
        print(f"Found pattern: {p}")
