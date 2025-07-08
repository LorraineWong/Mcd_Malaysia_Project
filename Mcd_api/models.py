from pydantic import BaseModel
from typing import Optional, Dict, Any

class Outlet(BaseModel):
    id: int
    name: str
    address: str
    latitude: Optional[float]
    longitude: Optional[float]
    telephone: Optional[str]
    waze_link: Optional[str]
    google_map_link: Optional[str]
    features: Optional[Dict[str, Any]]  # Dynamic feature map, e.g. {"is_24h": True, "has_wifi": True}
