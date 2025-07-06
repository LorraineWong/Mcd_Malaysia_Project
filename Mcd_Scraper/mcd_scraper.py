from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time
import sqlite3
from geocode_utils import geocode_address # Import geocoding utility

DB_PATH = "mcd_outlets.db"

def init_db():
    """
    Initialize the SQLite database and create the outlets table if it does not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outlets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            latitude REAL,
            longitude REAL,
            telephone TEXT,
            waze_link TEXT,
            google_map_link TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_outlet_to_db(outlet):
    """
    Insert an outlet record into the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO outlets (name, address, latitude, longitude, telephone, waze_link, google_map_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        outlet.get("name"),
        outlet.get("address"),
        outlet.get("latitude"),
        outlet.get("longitude"),
        outlet.get("telephone"),
        outlet.get("waze_link"),
        outlet.get("google_map_link")
    ))
    conn.commit()
    conn.close()

def extract_outlets_from_page(html):
    """
    Parse the page HTML and extract all McDonald's outlet information from <script type="application/ld+json"> blocks.
    If latitude/longitude are missing, use geocode_address to get them from the address.
    Always generate map links if possible.
    """
    soup = BeautifulSoup(html, "lxml")
    outlets = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "Restaurant":
                lat = data.get("geo", {}).get("latitude")
                lon = data.get("geo", {}).get("longitude")
                # If coordinates are missing, geocode using address
                if not lat or not lon:
                    lat, lon = geocode_address(data.get("address"))
                # Fallback if still missing (API/network failure)
                lat = lat or ""
                lon = lon or ""
                outlet = {
                    "name": data.get("name"),
                    "address": data.get("address"),
                    "latitude": lat,
                    "longitude": lon,
                    "telephone": data.get("telephone"),
                    "google_map_link": f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else None,
                    "waze_link": f"https://waze.com/ul?ll={lat},{lon}&navigate=yes" if lat and lon else None,
                }
                outlets.append(outlet)
        except Exception as e:
            print("[WARN] JSON parse error or geocode failed:", e)
    return outlets

def main():
    # Initialize DB
    init_db()

    # Setup Chrome driver (not headless for debugging)
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.mcdonalds.com.my/locate-us")

    wait = WebDriverWait(driver, 20)

    # Select "Kuala Lumpur" from the state dropdown
    state_select = wait.until(
        EC.element_to_be_clickable((By.ID, "states"))
    )
    Select(state_select).select_by_visible_text("Kuala Lumpur")

    # Click the "Search Now" button
    search_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "search-now"))
    )
    search_btn.click()

    # Wait for results to load (adjust if network is slow)
    time.sleep(2)

    # Extract outlet info from HTML
    outlets = extract_outlets_from_page(driver.page_source)
    print(f"Found {len(outlets)} outlets in Kuala Lumpur.")

    # Save to database and print
    for outlet in outlets:
        print(outlet)
        save_outlet_to_db(outlet)

    driver.quit()

if __name__ == "__main__":
    main()
