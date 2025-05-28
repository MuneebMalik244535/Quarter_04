import streamlit as st
from multi_agents.main_agent import plan_trip
from dotenv import load_dotenv
import os

load_dotenv()

st.title("🌍 AI Travel Planner (Gemini)")

destination = st.text_input("Enter destination")
start_date = st.date_input("Start date")
end_date = st.date_input("End date")
budget = st.number_input("Budget ($)", value=1000)
interests = st.multiselect("Your interests", ["Adventure", "Culture", "Nature", "Relaxation", "Food"])

if st.button("Plan My Trip"):
    with st.spinner("Planning your trip with Gemini AI..."):
        result = plan_trip(destination, str(start_date), str(end_date), budget, interests)
        st.markdown("## 🗺️ Your Itinerary")
        st.write(result)
