import streamlit as st
import requests
from PIL import Image
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Website configuration
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
local_css("style.css")

# Load and display a banner image


# Title
st.title("🚖 The Taxifare Meter")

# Instruction
st.markdown("""
Welcome to the Taxi Fare Prediction app. Enter the details below to get an estimated fare for your trip.
""")

url = 'https://taxifare.lewagon.ai/predict'

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Input fields for user to enter data
pickup_datetime = st.text_input("Pickup DateTime (YYYY-MM-DD HH:MM:SS)", current_time)
passenger_count = st.selectbox("Passenger Count", range(1, 11), index=0)

# Create Folium map for both pickup and dropoff locations
st.markdown("### Select Pickup and Dropoff Locations")
combined_map = folium.Map(location=[40.783282, -73.950655], zoom_start=12)
combined_map.add_child(folium.LatLngPopup())

# Draw a marker for pickup and dropoff points if they have been selected
pickup_coords = st.session_state.get('pickup_coords', None)
dropoff_coords = st.session_state.get('dropoff_coords', None)

if pickup_coords:
    folium.Marker(pickup_coords, tooltip="Pickup Location", icon=folium.Icon(color="green")).add_to(combined_map)

if dropoff_coords:
    folium.Marker(dropoff_coords, tooltip="Dropoff Location", icon=folium.Icon(color="red")).add_to(combined_map)

map_data = st_folium(combined_map, height=300, width=600)

# Check for map click events
if map_data and map_data["last_clicked"]:
    if "pickup_coords" not in st.session_state:
        st.session_state.pickup_coords = (map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"])
    elif "dropoff_coords" not in st.session_state:
        st.session_state.dropoff_coords = (map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"])

pickup_longitude = st.session_state.pickup_coords[1] if "pickup_coords" in st.session_state else -73.950655
pickup_latitude = st.session_state.pickup_coords[0] if "pickup_coords" in st.session_state else 40.783282
dropoff_longitude = st.session_state.dropoff_coords[1] if "dropoff_coords" in st.session_state else -73.984365
dropoff_latitude = st.session_state.dropoff_coords[0] if "dropoff_coords" in st.session_state else 40.769802

# Button to trigger prediction
if st.button("Predict Fare"):
    if not ("pickup_coords" in st.session_state and "dropoff_coords" in st.session_state):
        st.error("Please select both pickup and dropoff locations on the map.")
    else:
        # Prepare the payload for the API request
        params = {
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count
        }

        # Make a GET request to the API
        response = requests.get(url, params=params)

        if response.status_code == 200:
            prediction = response.json()
            fare = prediction.get('fare', 'N/A')
            st.success(f"Predicted Fare: ${fare}")
        else:
            st.error("Failed to get prediction from API")


image = Image.open('banner.jpg')  # Make sure you have a banner.jpg in the same directory
st.image(image, use_column_width=True)
