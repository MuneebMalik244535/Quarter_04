from pydantic import BaseModel
from typing import List

class Itinerary(BaseModel):
    destination: str
    start_date: str
    end_date: str
    activities: List[str]
    flights: List[dict]
    hotels: List[dict]
    weather: str
