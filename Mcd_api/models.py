# models.py
from pydantic import BaseModel
from typing import Optional

class Outlet(BaseModel):
    id: int
    name: str
    address: str
    latitude: Optional[float]
    longitude: Optional[float]
    telephone: Optional[str]
    waze_link: Optional[str]
    google_map_link: Optional[str]

