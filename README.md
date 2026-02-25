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

If you see "Error loading data. Make sure all_top3_data.json exists.":

1. Make sure you're running the local server: `python -m http.server 8000`
2. Access the site via: `http://localhost:8000/index.html`
3. Don't open `index.html` directly in the browser

The local server is required to avoid CORS (Cross-Origin Resource Sharing) restrictions that prevent browsers from loading local JSON files when opening HTML files directly.