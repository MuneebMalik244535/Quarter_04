import google.generativeai as genai
from tools.weather_tool import get_weather
from tools.flight_tool import get_flights
from tools.hotel_tool import get_hotels
import os

genai.configure(api_key="AIzaSyBJnLpWyU94PCrjB4ohXGicDt8yfERDLTc")

model = genai.GenerativeModel("gemini-2.0-flash")

def plan_trip(destination, start_date, end_date, budget, interests):
    weather = get_weather(destination, start_date, end_date)
    flights = get_flights(destination, start_date, end_date)
    hotels = get_hotels(destination, start_date, end_date, budget)

    prompt = f"""
    Plan a trip to {destination} from {start_date} to {end_date}.
    The user's budget is ${budget}.
    Interests: {', '.join(interests)}.

    --- Weather Forecast ---
    {weather}

    --- Flight Options ---
    {flights}

    --- Hotel Options ---
    {hotels}

    Please provide a structured and personalized trip itinerary day-by-day.
    """

    response = model.generate_content(prompt)
    return response.text
