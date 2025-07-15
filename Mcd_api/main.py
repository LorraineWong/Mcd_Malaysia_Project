from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from llm_utils import parse_query_to_feature_and_location, FEATURE_KEY_DESC
from db import get_all_outlets, get_outlet_by_id
from models import Outlet
import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Supported locations (should match LOCATION_KEYS in llm_utils.py)
VALID_LOCATIONS = ["kuala lumpur", "kl"]

app = FastAPI(
    title="🍔 McDonald's Outlets in Kuala Lumpur, Malaysia",
    description="Provides outlet data for McDonald's Kuala Lumpur, Malaysia."
)

# Allow CORS for frontend dev/demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ENV == "production" else ["*"],  # local: all allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the McDonald's Malaysia API!"}

@app.get("/outlets", response_model=list[Outlet])
def list_outlets():
    """Return all outlets (Kuala Lumpur only)"""
    return get_all_outlets()

@app.get("/outlets/{outlet_id}", response_model=Outlet)
def outlet_detail(outlet_id: int):
    """Get details for a single outlet by ID"""
    outlet = get_outlet_by_id(outlet_id)
    if outlet:
        return outlet
    raise HTTPException(status_code=404, detail="Outlet not found")

@app.post("/ask")
async def ask(request: Request):
    """
    LLM-powered search endpoint for natural language queries.
    Extracts feature_key and location, then searches only Kuala Lumpur outlets.
    """
    data = await request.json()
    user_question = data.get("question", "")
    feature_key, location = parse_query_to_feature_and_location(user_question)

    # Standardize location: treat both "kl" and "kuala lumpur" as "kuala lumpur"
    location_norm = (location or "").strip().lower()
    if location_norm in ["kl", "kuala lumpur"]:
        location_norm = "kuala lumpur"

    # Reject ALL not supported locations (not KL) or missing/invalid feature_key
    if (location_norm != "kuala lumpur") or (not feature_key):
        return {
            "feature_key": None,
            "location": location or "",
            "feature_desc": "",
            "outlets": [],
            "msg": (
                "Sorry, I'm only answer about McDonald's outlets in Kuala Lumpur "
                "and supported features (e.g. 24h, WiFi, Drive-Thru). "
                "Try asking about KL (Kuala Lumpur) only."
            )
        }

    outlets = get_all_outlets()
    filtered = [o for o in outlets if o.features and o.features.get(feature_key)]
    names = [o.name for o in filtered]

    return {
        "feature_key": feature_key,
        "location": "kuala lumpur",
        "feature_desc": FEATURE_KEY_DESC.get(feature_key, feature_key),
        "outlets": names,
        "msg": (
            f"Found {len(names)} outlets in Kuala Lumpur with "
            f"{FEATURE_KEY_DESC.get(feature_key, feature_key)}."
            if names else
            f"Sorry, no outlets in Kuala Lumpur found with {FEATURE_KEY_DESC.get(feature_key, feature_key)}."
        )
    }

