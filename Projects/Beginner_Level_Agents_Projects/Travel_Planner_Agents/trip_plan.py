# models/trip_plan.py
from pydantic import BaseModel
from typing import List


class TravelPlan(BaseModel):
    destination: str
    days: int
    activities: List[str]
    estimated_budget: float
    weather_forecast: str
    flight_options: List[str]
    hotel_options: List[str]
