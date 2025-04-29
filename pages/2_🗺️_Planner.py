import os
import streamlit as st
import pandas as pd
from datetime import date

import utils
from src.planner.flow import SoloTravelPlannerFlow

st.set_page_config(
    page_title="Thailand Trip Companion",
    page_icon="🌴",
    layout="centered"
)

conn = utils.connect_to_postgres()
option_passport = utils.get_list_passport(conn)
option_airport = utils.get_list_airport(conn)
option_time = ("00:00 - 05:59", "06:00 - 11:59", "12:00 - 17:59", "18:00 - 23:59")

st.title("🗺️ AI-Powered Solo Travel Planner")

st.header("Passport", divider="blue")

pp = st.selectbox(
    "Country/Territory of Passport:",
    options=option_passport,
    index=None,
    placeholder="Select Passport",
)

st.header("Arrival", divider="blue")

ad = st.date_input("Date:", value=date.today(), key="Arrival Date", min_value=date.today())
at = st.selectbox("Time:", index=None, options=option_time, key="Arrival Time")
ac = st.selectbox(
    "From (Airport):",
    options=option_airport,
    index=None,
    placeholder="Select Airport",
    key="Depart From"
)

st.header("Return", divider="blue")

rd = st.date_input("Date:", value=None, key="Return Date", min_value=ad)
rt = st.selectbox("Time:", index=None, options=option_time, key="Return Time")
rc = st.selectbox(
    "To (Airport):",
    options=option_airport,
    index=None,
    placeholder="Select Airport",
    key="Return To"
)

st.header("Budget", divider="blue")

fb = st.number_input("Flight Budget (USD) - per flight", value=None, placeholder="flight budget...")
hb = st.number_input("Hotel Budget (USD) - per night", value=None, placeholder="hotel budget...")

st.header("Why Thailand?", divider="blue")

interest = st.text_area(
    "Your interest in Thailand:",
    value=None,
    placeholder="Places, Authentic Food, Historical Museum, ...",
    key="interest"
)

_, middle, _ = st.columns(3)
is_make_plan = middle.button("Make a Plan", icon="📝", use_container_width=True)

if is_make_plan:
    st.header("Plan", divider="green")
    with st.spinner("Waiting for planner...", show_time=True):
        inputs = {
            "passport": pp,
            "arr_date": ad.strftime("%Y-%m-%d"),
            "arr_time": at,
            "dep_from": ac,
            "ret_date": rd.strftime("%Y-%m-%d"),
            "ret_time": rt,
            "ret_to": rc,
            "fli_budget": fb,
            "hot_budget": hb,
            "interest": interest,
        }
        
        try:
            html_travel_handbook = SoloTravelPlannerFlow().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")

    # Show HTML Handbook
    html_file = "result/travel_handbook.html"
    if os.path.exists(html_file):
        st.write("Travel Handbook:")

        with open(html_file, "r") as hf:
            html_travel_handbook = hf.read()
        st.download_button(
            label="Full-screen Handbook",
            data=html_travel_handbook,
            file_name=html_file,
            icon="📖",
        )

        st.components.v1.html(html_travel_handbook, scrolling=True, height=600)

    # Upload all planner files
    utils.upload_planner_files_to_blob()

