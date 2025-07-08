# llm_utils.py

from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load Gemini API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model configuration
model = genai.GenerativeModel("gemini-2.5-pro")

# Supported feature keys (expand as your DB grows)
FEATURE_KEYS = [
    "is_24h", "has_birthday", "has_breakfast", "has_cashless", "has_dessert",
    "has_order_kiosk", "has_drive_thru", "has_ev", "has_mccafe", "has_mc_delivery",
    "has_suara", "has_wifi"
]

FEATURE_KEY_DESC = {
    "is_24h": "24 hours",
    "has_birthday": "Birthday Party",
    "has_breakfast": "Breakfast",
    "has_cashless": "Cashless Facility",
    "has_dessert": "Dessert Center",
    "has_order_kiosk": "Digital Order Kiosk",
    "has_drive_thru": "Drive-Thru",
    "has_ev": "Electric Vehicle",
    "has_mccafe": "McCafe",
    "has_mc_delivery": "McDelivery",
    "has_suara": "Surau",
    "has_wifi": "WiFi"
}

# Supported city/location keys (extendable in the future)
LOCATION_KEYS = [
    "kuala lumpur", "kl"
    # Add more (e.g. "pj", "petaling jaya") as your DB expands
]

def parse_query_to_feature_and_location(user_query: str):
    """
    Uses Gemini LLM to extract the target feature_key and location (city) from user's query.
    Returns (feature_key, location): both are lowercase, or None if not found.
    Only supports locations in LOCATION_KEYS (default: 'kuala lumpur').
    """
    prompt = (
        "You are a smart assistant for McDonald's outlet search in Malaysia.\n"
        "Extract ONLY the following two things from the user's question:\n"
        "1. Feature key: exactly one from this list: "
        f"{', '.join(FEATURE_KEYS)}\n"
        "2. Location: only one of: 'kuala lumpur', 'kl'.\n"
        "\n"
        "Strict answer format: <feature_key>|<location>\n"
        "Rules:\n"
        "- If the question is about any location NOT in ['kuala lumpur', 'kl'], output just: |\n"
        "- If no valid feature is mentioned, output just: |\n"
        "- If the question is not about McDonald's outlets or irrelevant, output just: |\n"
        "- If location is missing, assume 'kuala lumpur'.\n"
        "- Do NOT explain or repeat the user's question, only output the format.\n"
        "\nExamples:\n"
        "Q: Which outlets operate 24 hours in KL?\nA: is_24h|kuala lumpur\n"
        "Q: Which outlet allows birthday parties in PJ?\nA: |\n"
        "Q: Which outlets in Taiwan operate 24 hours?\nA: |\n"
        "Q: Which McDonald's has WiFi?\nA: has_wifi|kuala lumpur\n"
        "Q: Do any outlets have a playground?\nA: |\n"
        "\n"
        f"User question: {user_query}\n"
        "Answer:"
    )

    try:
        response = model.generate_content(prompt)
        if not response.text:
            return None, None
        # Normalize and split the response like: "is_24h|kuala lumpur"
        answer = response.text.strip().lower().replace(" ", "")
        if "|" not in answer:
            return None, None
        feature_key, location = answer.split("|", 1)
        # Validate feature_key
        feature_key = feature_key if feature_key in FEATURE_KEYS else None
        # Only allow valid locations (fallback to 'kuala lumpur' for unsupported or empty)
        location = location if location in LOCATION_KEYS else "kuala lumpur"
        return feature_key, location
    except Exception as e:
        print("LLM parsing error:", e)
        return None, None

# You can also add a test block for local debugging
if __name__ == "__main__":
    test_queries = [
        "Which outlets operate 24 hours in KL?",
        "Which outlet allows birthday parties in PJ?",
        "Which McDonald's has WiFi?",
        "Do any outlets have a playground?",
        "Which outlets serve ice cream?",
        "Any outlets in Taiwan with McCafe?"
    ]
    for q in test_queries:
        feature, location = parse_query_to_feature_and_location(q)
        print(f"Q: {q}\n -> Feature: {feature}, Location: {location}\n")
