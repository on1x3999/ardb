import json
import urllib.request
import urllib.error
import time
import os
from datetime import datetime

def fetch_json(url, retries=5, delay=2):
    """Fetch JSON with retry logic"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"    Attempt {attempt+1}/{retries} failed: {str(e)[:50]}")
            if attempt < retries - 1:
                time.sleep(delay)
    return None

def fetch_leaderboard():
    """Fetch leaderboard to get all players"""
    url = "https://www.abilityarena.com/api/leaderboard?limit=100"
    data = fetch_json(url)
    return data if data else []

def fetch_player_games(steam_id):
    """Get all games for a player"""
    url = f"https://www.abilityarena.com/api/players/{steam_id}/games"
    data = fetch_json(url)
    return data if data else []

def fetch_match_details(match_id):
    """Get full match details"""
    url = f"https://www.abilityarena.com/api/games/{match_id}"
    return fetch_json(url)

def extract_top3_players(match_data):
    """Extract top 3 players from match data"""
    top_3 = []
    for player in match_data.get('players', []):
        place = player.get('place')
        if place in [1, 2, 3]:
            # Extract hero data
            heroes = []
            for hero in player.get('heroes', []):
                hero_name = hero.get('hero_name', '').replace('npc_dota_hero_', '')
                abilities = []
                for abil in hero.get('abilities', []):
                    abilities.append({
                        'name': abil.get('ability_name'),
                        'level': abil.get('ability_level'),
                        'icon': abil.get('icon'),
                        'is_ultimate': abil.get('is_ultimate', False)
                    })
                heroes.append({
                    'name': hero_name,
                    'tier': hero.get('tier'),
                    'abilities': abilities
                })

            top_3.append({
                'place': place,
                'username': player.get('username'),
                'god': player.get('god'),
                'heroes': heroes
            })

    return top_3

def get_match_date(match_data):
    """Extract date from match data"""
    # Try to get date from match metadata
    start_time = match_data.get('start_time')
    if start_time:
        try:
            # Convert timestamp to date
            dt = datetime.fromtimestamp(start_time)
            return dt.strftime('%Y-%m-%d')
        except:
            pass
    
    # Fallback to current date
    return datetime.now().strftime('%Y-%m-%d')

def load_existing_data():
    """Load all existing match data from data directory"""
    existing_data = {}
    existing_match_ids = set()
    
    if not os.path.exists('data'):
        return existing_data, existing_match_ids
    
    for date_folder in os.listdir('data'):
        date_path = os.path.join('data', date_folder)
        if os.path.isdir(date_path):
            matches_file = os.path.join(date_path, 'matches.json')
            if os.path.exists(matches_file):
                try:
                    with open(matches_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for match in data.get('matches', []):
                            match_id = match.get('match_id')
                            if match_id:
                                existing_match_ids.add(match_id)
                                existing_data[match_id] = match
                except Exception as e:
                    print(f"Error loading {matches_file}: {e}")
    
    print(f"Loaded {len(existing_data)} existing matches")
    return existing_data, existing_match_ids

def save_matches_by_date(new_matches):
    """Save new matches grouped by date"""
    if not new_matches:
        return
    
    # Group matches by date
    matches_by_date = {}
    for match in new_matches:
        date = match.get('date', datetime.now().strftime('%Y-%m-%d'))
        if date not in matches_by_date:
            matches_by_date[date] = []
        matches_by_date[date].append(match)
    
    # Save each date's matches
    for date, matches in matches_by_date.items():
        date_folder = os.path.join('data', date)
        os.makedirs(date_folder, exist_ok=True)
        
        matches_file = os.path.join(date_folder, 'matches.json')
        
        # Load existing matches for this date if any
        existing_matches = []
        if os.path.exists(matches_file):
            try:
                with open(matches_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_matches = existing_data.get('matches', [])
            except:
                pass
        
        # Combine and save
        all_matches = existing_matches + matches
        data_to_save = {
            'date': date,
            'matches': all_matches
        }
        
        with open(matches_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(matches)} matches for {date}")

def fetch_all_matches():
    """Fetch all match data for top 3 players with incremental updates"""
    
    # Load existing data
    existing_data, existing_match_ids = load_existing_data()
    
    # First get leaderboard
    print("Fetching leaderboard...")
    players = fetch_leaderboard()
    print(f"Found {len(players)} players")

    # For each player, get their games
    new_matches = []
    processed_match_ids = set()  # Avoid duplicates
    total_games = 0
    games_since_last_save = 0

    for i, player in enumerate(players):
        username = player.get('username', 'Unknown')
        steam_id = player.get('steam_id')

        if not steam_id:
            continue

        print(f"\n[{i+1}/{len(players)}] {username} (steam: {steam_id})")

        # Get player's games
        games = fetch_player_games(steam_id)
        print(f"  Found {len(games)} games")

        # Process each game - get full details
        for game in games:
            match_id = game.get('game_id')
            if not match_id:
                continue

            # Skip if already exists
            if match_id in existing_match_ids or match_id in processed_match_ids:
                continue

            if total_games >= 10000:
                print(f"\nReached limit of 10000 matches!")
                break

            print(f"    Fetching match {match_id}...")

            # Get full match details
            match_data = fetch_match_details(match_id)
            if not match_data:
                print(f"      Failed to fetch match")
                continue

            # Get top 3 players
            top_3 = extract_top3_players(match_data)

            if top_3:
                # Get match date
                match_date = get_match_date(match_data)
                
                new_match = {
                    'match_id': match_id,
                    'date': match_date,
                    'players': top_3
                }
                
                new_matches.append(new_match)
                processed_match_ids.add(match_id)
                total_games += 1
                games_since_last_save += 1
                print(f"      Got top {len(top_3)} players")

                # Save every 50 games
                if games_since_last_save >= 50:
                    save_matches_by_date(new_matches[-50:])
                    games_since_last_save = 0

            # Rate limiting to avoid timeouts
            time.sleep(0.5)

        if total_games >= 10000:
            break

        # Save progress after each player
        if new_matches:
            save_matches_by_date(new_matches[-50:])
        print(f"  >>> Progress tracked: {len(existing_data) + len(new_matches)} total matches after player {i+1}")

    # Save final result
    if new_matches:
        save_matches_by_date(new_matches)
    
    print(f"\n\n=== FINAL ===")
    print(f"Total matches: {len(existing_data) + len(new_matches)}")
    print(f"New matches added: {len(new_matches)}")
    print(f"Existing matches preserved: {len(existing_data)}")

def combine_all_data():
    """Combine all data files into a single all_top3_data.json"""
    all_matches = []
    
    if not os.path.exists('data'):
        print("No data directory found")
        return
    
    for date_folder in os.listdir('data'):
        date_path = os.path.join('data', date_folder)
        if os.path.isdir(date_path):
            matches_file = os.path.join(date_path, 'matches.json')
            if os.path.exists(matches_file):
                try:
                    with open(matches_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_matches.extend(data.get('matches', []))
                except Exception as e:
                    print(f"Error loading {matches_file}: {e}")
    
    # Sort by match_id or date
    all_matches.sort(key=lambda x: x.get('match_id', ''))
    
    with open('all_top3_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_matches, f, indent=2, ensure_ascii=False)
    
    print(f"Combined {len(all_matches)} matches into all_top3_data.json")

if __name__ == "__main__":
    fetch_all_matches()
    # Uncomment to combine data after scraping
    # combine_all_data()