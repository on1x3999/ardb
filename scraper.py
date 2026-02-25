"""
Ability Arena Scraper - Launch Chrome with remote debugging and scrape
"""

from playwright.sync_api import sync_playwright
import subprocess
import json
import time
import os
import sys

def launch_chrome_with_debugging():
    """Launch Chrome with remote debugging port"""
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data", "Default")
    
    # Launch Chrome with remote debugging
    args = [
        chrome_path,
        "--remote-debugging-port=9222",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={user_data_dir}",
        "--new-window",
        "https://www.abilityarena.com/leaderboard"
    ]
    
    print(f"Launching Chrome with remote debugging on port 9222...")
    process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Chrome process started with PID: {process.pid}")
    return process

def scrape():
    """Main scraping function"""
    
    # Launch Chrome
    chrome_process = launch_chrome_with_debugging()
    
    # Wait for Chrome to start
    print("Waiting for Chrome to start...")
    time.sleep(5)
    
    with sync_playwright() as p:
        print("Connecting to Chrome...")
        
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("Connected to Chrome!")
            
            contexts = browser.contexts
            if contexts:
                context = contexts[0]
                pages = context.pages
                if pages:
                    page = pages[0]
                else:
                    page = context.new_page()
            else:
                context = browser.new_context()
                page = context.new_page()
            
            print(f"\nPage URL: {page.url}")
            print(f"Page title: {page.title}")
            
            print("\nWaiting for content to load...")
            time.sleep(15)
            
            # Get page content
            text = page.evaluate("document.body.innerText")
            print(f"Body text length: {len(text)}")
            
            print("\n" + "="*50)
            print("Page content:")
            print("="*50)
            print(text[:8000])
            print("="*50)
            
            # Find player links
            player_links = page.query_selector_all("a[href*='/players/']")
            print(f"\nFound {len(player_links)} player links")
            
            players_data = []
            for link in player_links[:10]:
                href = link.get_attribute("href")
                try:
                    name = link.inner_text().strip()
                except:
                    name = ""
                if href:
                    players_data.append({
                        'url': href,
                        'name': name
                    })
                    print(f"  - {name}: {href}")
            
            with open("leaderboard_data.json", "w", encoding="utf-8") as f:
                json.dump(players_data, f, indent=2)
            print(f"\nSaved {len(players_data)} players to leaderboard_data.json")
            
            print("\nScraping complete!")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                browser.close()
            except:
                pass
    
    # Don't close Chrome - let user continue using it
    print("\nChrome is still running. You can continue browsing manually.")

def main():
    print("=" * 50)
    print("Ability Arena Scraper")
    print("=" * 50)
    scrape()

if __name__ == "__main__":
    main()
