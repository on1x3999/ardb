import json
import os
from datetime import datetime

def migrate_existing_data_split():
    """Migrate existing all_top3_data.json to new structure with split files"""
    
    # Check if old file exists
    if not os.path.exists('all_top3_data.json'):
        print("No existing all_top3_data.json found")
        return
    
    print("Loading existing all_top3_data.json...")
    
    # Load existing data
    with open('all_top3_data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    print(f"Loaded {len(existing_data)} matches from existing file")
    
    # Group matches by date (using current date as fallback)
    matches_by_date = {}
    
    for match in existing_data:
        # Try to get date from match metadata, use current date if not available
        match_date = match.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if match_date not in matches_by_date:
            matches_by_date[match_date] = []
        
        matches_by_date[match_date].append(match)
    
    # Save to new structure with split files (50 matches per file)
    total_saved = 0
    
    for date, matches in matches_by_date.items():
        date_folder = os.path.join('data', date)
        os.makedirs(date_folder, exist_ok=True)
        
        # Split matches into chunks of 50
        chunk_size = 50
        for i in range(0, len(matches), chunk_size):
            chunk = matches[i:i + chunk_size]
            chunk_number = i // chunk_size + 1
            
            # Create filename with chunk number
            if len(matches) <= chunk_size:
                # If only one chunk, use simple name
                matches_file = os.path.join(date_folder, 'matches.json')
            else:
                # If multiple chunks, number them
                matches_file = os.path.join(date_folder, f'matches_part_{chunk_number}.json')
            
            # Check if file already exists
            existing_matches = []
            if os.path.exists(matches_file):
                try:
                    with open(matches_file, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                        existing_matches = existing_data.get('matches', [])
                except:
                    pass
            
            # Combine and save
            all_matches = existing_matches + chunk
            data_to_save = {
                'date': date,
                'chunk': chunk_number if len(matches) > chunk_size else 1,
                'total_chunks': (len(matches) + chunk_size - 1) // chunk_size,
                'matches': all_matches
            }
            
            with open(matches_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            
            total_saved += len(chunk)
            print(f"Saved {len(chunk)} matches to {os.path.basename(matches_file)} for {date}")
    
    print(f"\n=== MIGRATION COMPLETE ===")
    print(f"Total matches migrated: {total_saved}")
    print(f"Data saved to data/ directory with split files")
    
    # Create backup
    backup_name = f"all_top3_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.rename('all_top3_data.json', backup_name)
    print(f"Original file backed up as: {backup_name}")

def check_migration():
    """Check if migration was successful"""
    if not os.path.exists('data'):
        print("No data directory found - migration not needed")
        return False
    
    total_matches = 0
    dates_count = 0
    files_count = 0
    
    for date_folder in os.listdir('data'):
        date_path = os.path.join('data', date_folder)
        if os.path.isdir(date_path):
            dates_count += 1
            for file_name in os.listdir(date_path):
                if file_name.startswith('matches') and file_name.endswith('.json'):
                    files_count += 1
                    matches_file = os.path.join(date_path, file_name)
                    try:
                        with open(matches_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            total_matches += len(data.get('matches', []))
                    except Exception as e:
                        print(f"Error checking {matches_file}: {e}")
    
    print(f"\n=== MIGRATION STATUS ===")
    print(f"Dates with data: {dates_count}")
    print(f"Total files: {files_count}")
    print(f"Total matches: {total_matches}")
    
    return total_matches > 0

if __name__ == "__main__":
    print("=== Data Migration Tool (Split Files) ===")
    print("This will migrate your existing all_top3_data.json to the new structure")
    print("The original file will be backed up")
    print("Matches will be split into files of 50 matches each")
    
    if os.path.exists('all_top3_data.json'):
        confirm = input("Proceed with migration? (y/n): ").strip().lower()
        if confirm == 'y':
            migrate_existing_data_split()
        else:
            print("Migration cancelled")
    else:
        print("No existing all_top3_data.json found")
        check_migration()