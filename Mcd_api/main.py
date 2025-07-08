# main.py
from fastapi import FastAPI, HTTPException
from db import get_all_outlets, get_outlet_by_id
from models import Outlet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="McDonald's Malaysia Outlets API",
    description="Provides outlet data for McDonald's Malaysia."
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the McDonald's Malaysia API!"}

@app.get("/outlets", response_model=list[Outlet])
def list_outlets():
    return get_all_outlets()

@app.get("/outlets/{outlet_id}", response_model=Outlet)
def outlet_detail(outlet_id: int):
    outlet = get_outlet_by_id(outlet_id)
    if outlet:
        return outlet
    raise HTTPException(status_code=404, detail="Outlet not found")
