import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def geocode_address(address):
    """
    Use Google Maps Geocoding API to convert address to (lat, lng)
    """
    if not GOOGLE_API_KEY:
        print("Google API Key not found! Please set GOOGLE_API_KEY in your .env file.")
        return None, None
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_API_KEY}
    resp = requests.get(url, params=params).json()
    if resp.get("results"):
        location = resp["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    print("No geocode result for:", address)
    return None, None

if __name__ == "__main__":
    address = "27 & 28, Jalan Abdul Aziz, 43000, Kajang, Selangor, Malaysia"
    lat, lng = geocode_address(address)
    print(f"Address: {address}\nLatitude: {lat}, Longitude: {lng}")
