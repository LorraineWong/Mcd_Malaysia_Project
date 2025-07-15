from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time
import sqlite3
from geocode_utils import geocode_address
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'mcd_outlets.db'))

# Mapping icon filenames (or alt text) to normalized feature keys
ICON_FEATURE_MAP = {
    "24h": "is_24h",
    "birthday": "has_birthday",
    "breakfast": "has_breakfast",
    "cashless": "has_cashless",
    "dessert": "has_dessert",
    "dt": "has_drive_thru",
    "mccafe": "has_mccafe",
    "mcdelivery": "has_mc_delivery",
    "surau": "has_surau",
    "wifi": "has_wifi",
    "kiosk": "has_order_kiosk",
    "ev": "has_ev",
}

def init_db():
    """
    Initialize the SQLite database and create the outlets table if it does not exist.
    Adds a UNIQUE constraint on (name, address) to prevent duplicates.
    Adds a 'features' column for JSON.
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
            google_map_link TEXT,
            features TEXT,  -- Store all feature flags as JSON string
            UNIQUE(name, address)
        )
    """)
    conn.commit()
    conn.close()

def save_outlet_to_db(outlet):
    """
    Insert or update an outlet record by (name, address) to prevent duplicates.
    The 'features' field is saved as JSON string.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    features_json = json.dumps(outlet.get("features", {}))
    cursor.execute("""
        UPDATE outlets SET
            latitude=?,
            longitude=?,
            telephone=?,
            waze_link=?,
            google_map_link=?,
            features=?
        WHERE name=? AND address=?
    """, (
        outlet.get("latitude"),
        outlet.get("longitude"),
        outlet.get("telephone"),
        outlet.get("waze_link"),
        outlet.get("google_map_link"),
        features_json,
        outlet.get("name"),
        outlet.get("address"),
    ))
    if cursor.rowcount == 0:
        cursor.execute("""
            INSERT INTO outlets
            (name, address, latitude, longitude, telephone, waze_link, google_map_link, features)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            outlet.get("name"),
            outlet.get("address"),
            outlet.get("latitude"),
            outlet.get("longitude"),
            outlet.get("telephone"),
            outlet.get("waze_link"),
            outlet.get("google_map_link"),
            features_json,
        ))
    conn.commit()
    conn.close()

def extract_outlets_from_page(html):
    """
    Parse the page HTML and extract all McDonald's outlet information and features.
    - Grabs all feature icons (e.g. 24h, Drive-Thru, WiFi...) using their image filename.
    - Features are stored as a dictionary (e.g. {"is_24h": True, ...})
    """
    soup = BeautifulSoup(html, "lxml")
    outlets = []
    cards = soup.select("div.addressBox")
    for card in cards:
        try:
            # Extract JSON-LD structured data
            ld_json = None
            for script in card.find_all("script", type="application/ld+json"):
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get("@type") == "Restaurant":
                    ld_json = data
                    break
            if not ld_json:
                continue

            # Get coordinates from JSON-LD or use geocoding fallback
            lat = ld_json.get("geo", {}).get("latitude")
            lon = ld_json.get("geo", {}).get("longitude")
            if not lat or not lon:
                lat, lon = geocode_address(ld_json.get("address"))
            lat = lat or ""
            lon = lon or ""

            # Initialize all features to False
            features = {feature: False for feature in ICON_FEATURE_MAP.values()}

            # Update features to True if icon matched
            for img in card.find_all("img", class_="addressIcon"):
                src = img.get("src", "").lower()
                alt = img.get("alt", "").lower()
                for key, feature in ICON_FEATURE_MAP.items():
                    if key in src or key in alt:
                        features[feature] = True

            # Build outlet dictionary
            outlet = {
                "name": ld_json.get("name"),
                "address": ld_json.get("address"),
                "latitude": lat,
                "longitude": lon,
                "telephone": ld_json.get("telephone"),
                "google_map_link": f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else None,
                "waze_link": f"https://waze.com/ul?ll={lat},{lon}&navigate=yes" if lat and lon else None,
                "features": features,  # Store all features here
            }
            outlets.append(outlet)
        except Exception as e:
            print("[WARN] JSON parse error or geocode failed:", e)
    return outlets

def main():
    init_db()
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.mcdonalds.com.my/locate-us")

    wait = WebDriverWait(driver, 20)
    state_select = wait.until(EC.element_to_be_clickable((By.ID, "states")))
    Select(state_select).select_by_visible_text("Kuala Lumpur")

    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "search-now")))
    search_btn.click()
    time.sleep(2) # Allow time for outlet list to load

    outlets = extract_outlets_from_page(driver.page_source)
    print(f"Found {len(outlets)} outlets in Kuala Lumpur.")
    for outlet in outlets:
        print(outlet)
        save_outlet_to_db(outlet)

    driver.quit()

if __name__ == "__main__":
    main()