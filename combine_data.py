import json
import os
from datetime import datetime

def combine_all_data():
    """Combine all data files into a single all_top3_data.json"""
    all_matches = []
    
    if not os.path.exists('data'):
        print("No data directory found")
        return
    
    print("Loading all match data...")
    
    for date_folder in os.listdir('data'):
        date_path = os.path.join('data', date_folder)
        if os.path.isdir(date_path):
            # Look for all match files (both matches.json and matches_part_*.json)
            for file_name in os.listdir(date_path):
                if file_name.startswith('matches') and file_name.endswith('.json'):
                    matches_file = os.path.join(date_path, file_name)
                    if os.path.exists(matches_file):
                        try:
                            with open(matches_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                matches = data.get('matches', [])
                                all_matches.extend(matches)
                                print(f"Loaded {len(matches)} matches from {date_folder}/{file_name}")
                        except Exception as e:
                            print(f"Error loading {matches_file}: {e}")
    
    # Sort by match_id
    all_matches.sort(key=lambda x: x.get('match_id', ''))
    
    # Save combined data
    with open('all_top3_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_matches, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== COMBINED DATA SUMMARY ===")
    print(f"Total matches: {len(all_matches)}")
    print(f"Combined data saved to all_top3_data.json")

def get_data_stats():
    """Get statistics about the data structure"""
    if not os.path.exists('data'):
        print("No data directory found")
        return
    
    total_matches = 0
    dates_with_data = []
    
    for date_folder in os.listdir('data'):
        date_path = os.path.join('data', date_folder)
        if os.path.isdir(date_path):
            matches_file = os.path.join(date_path, 'matches.json')
            if os.path.exists(matches_file):
                try:
                    with open(matches_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        matches_count = len(data.get('matches', []))
                        total_matches += matches_count
                        dates_with_data.append((date_folder, matches_count))
                except Exception as e:
                    print(f"Error loading {matches_file}: {e}")
    
    # Sort by date
    dates_with_data.sort()
    
    print(f"\n=== DATA STRUCTURE SUMMARY ===")
    print(f"Total dates with data: {len(dates_with_data)}")
    print(f"Total matches: {total_matches}")
    print(f"\nMatches by date:")
    for date, count in dates_with_data:
        print(f"  {date}: {count} matches")

if __name__ == "__main__":
    print("=== Data Management Tool ===")
    print("1. Combine all data files")
    print("2. Show data statistics")
    
    choice = input("Choose option (1/2): ").strip()
    
    if choice == "1":
        combine_all_data()
    elif choice == "2":
        get_data_stats()
    else:
        print("Invalid choice")