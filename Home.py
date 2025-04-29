import streamlit as st

st.set_page_config(
    page_title="Thailand Trip Companion",
    page_icon="🌴",
    layout="centered"
)

# Header

st.title("🌴 Thailand Trip Companion")
st.write(
    "Planning your perfect trip to Thailand has never been easier. "
    "Our AI-powered application helps you effortlessly create personalized travel experiences, "
    "answer your questions, and collect your valuable feedback."
)

st.markdown("---")

# Sections

st.header("🗨️ Chatbot")
st.page_link("pages/1_🗨️_Chatbot.py", label="Click Here to chatbot")
st.write(
    "Ask any questions about Thailand—culture, customs, local tips, and more. "
    "Our intelligent chatbot is ready to assist you with reliable information."
)

st.header("🗺️ AI-Powered Solo Travel Planner")
st.page_link("pages/2_🗺️_Planner.py", label="Click Here to planner")
st.write(
    "Create a tailored itinerary including attractions, hotels, transportation options, "
    "weather forecasts, and useful travel tips. Let our smart AI crew handle the complexities "
    "and provide you with a detailed, personalized travel handbook."
)

st.header("💬 Feedback")
st.page_link("pages/3_💬_Feedback.py", label="Click Here to feedback")
st.write(
    "Your voice matters! Share your experiences, suggestions, or issues. "
    "Help us improve and ensure every traveler enjoys an exceptional journey."
)

st.markdown("---")

# Footer

st.write("Start exploring now and let our AI make your Thailand adventure unforgettable!")
