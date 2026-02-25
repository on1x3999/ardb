# AR Parser Website

This website displays match data from the AR (Arena of Valor) game.

## How to Run

### Option 1: Local HTTP Server (Recommended)
1. Open a command prompt in this directory
2. Run: `python -m http.server 8000`
3. Open your browser and go to: `http://localhost:8000/index.html`

### Option 2: Direct File Access (May have CORS issues)
- Open `index.html` directly in your browser (may not work due to CORS restrictions)

## Data Files

- `all_top3_data.json` - Contains all match data (4,100 matches)
- `abilities.json` - Ability information
- `ability_combos.json` - Popular ability combinations
- `leaderboard_data.json` - Leaderboard information

## Features

- View match history with player details
- Filter matches by date
- View player statistics
- See popular ability combinations
- View leaderboard rankings

## Troubleshooting

### Local Development

If you see "Error loading data. Make sure all_top3_data.json exists.":

1. Make sure you're running the local server: `python -m http.server 8000`
2. Access the site via: `http://localhost:8000/index.html`
3. Don't open `index.html` directly in the browser

The local server is required to avoid CORS (Cross-Origin Resource Sharing) restrictions that prevent browsers from loading local JSON files when opening HTML files directly.

### GitHub Pages Deployment

**Issue**: The `all_top3_data.json` file is large (50MB) and tracked with Git LFS, which can cause loading errors on GitHub Pages.

**Solution**: The website now uses a dual-loading approach:

1. **Primary**: Tries to load data from split files in `data/YYYY-MM-DD/matches_part_*.json`
2. **Fallback**: If split files aren't available, falls back to the combined `all_top3_data.json` file

This ensures the site works even if GitHub Pages has issues serving the large combined file. The split files are smaller and more reliable for web serving.

### Data Files

- `all_top3_data.json` - Combined match data (4,100 matches) - tracked with Git LFS
- `data/YYYY-MM-DD/matches_part_*.json` - Split data files for better web performance
- `abilities.json` - Ability information
- `ability_combos.json` - Popular ability combinations
- `leaderboard_data.json` - Leaderboard information
