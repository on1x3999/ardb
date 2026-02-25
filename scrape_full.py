import json
import urllib.request
import urllib.error
import time
import os

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

def fetch_all_matches():
    """Fetch all match data for top 3 players"""

    # Load existing data if available
    existing_data = []
    existing_match_ids = set()
    if os.path.exists('all_top3_data.json'):
        print("Loading existing match data...")
        try:
            with open('all_top3_data.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            existing_match_ids = {match['match_id'] for match in existing_data}
            print(f"Loaded {len(existing_data)} existing matches")
        except Exception as e:
            print(f"Error loading existing data: {e}")
            existing_data = []
            existing_match_ids = set()

    # First get leaderboard
    print("Fetching leaderboard...")
    players = fetch_leaderboard()
    print(f"Found {len(players)} players")

    # For each player, get their games
    new_match_data = []
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
                new_match_data.append({
                    'match_id': match_id,
                    'players': top_3
                })
                processed_match_ids.add(match_id)
                total_games += 1
                games_since_last_save += 1
                print(f"      Got top {len(top_3)} players")

                # Save every 100 games
                if games_since_last_save >= 100:
                    # Combine existing and new data
                    combined_data = existing_data + new_match_data
                    with open('all_top3_data.json', 'w', encoding='utf-8') as f:
                        json.dump(combined_data, f, indent=2, ensure_ascii=False)
                    print(f"  >>> Saved progress: {len(combined_data)} total matches after {total_games} games")
                    games_since_last_save = 0

            # Rate limiting to avoid timeouts
            time.sleep(0.5)

        if total_games >= 10000:
            break

        # Save progress after each player (now just for tracking)
        combined_data = existing_data + new_match_data
        with open('all_matches_progress.json', 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        print(f"  >>> Progress tracked: {len(combined_data)} total matches after player {i+1}")

    # Save final result
    final_data = existing_data + new_match_data
    with open('all_top3_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    print(f"\n\n=== FINAL ===")
    print(f"Total matches: {len(final_data)}")
    print(f"New matches added: {len(new_match_data)}")
    print(f"Existing matches preserved: {len(existing_data)}")
    print(f"Final save to all_top3_data.json")

if __name__ == "__main__":
    fetch_all_matches()