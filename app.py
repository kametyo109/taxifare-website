import streamlit as st
import requests


'''
# TaxiFareModel hello
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''

st.title("Taxi Fare Prediction")

# Input fields for user to enter data
pickup_datetime = st.text_input("Pickup DateTime (YYYY-MM-DD HH:MM:SS)", "2013-07-06 17:18:00")
pickup_longitude = st.number_input("Pickup Longitude", -73.950655)
pickup_latitude = st.number_input("Pickup Latitude", 40.783282)
dropoff_longitude = st.number_input("Dropoff Longitude", -73.984365)
dropoff_latitude = st.number_input("Dropoff Latitude", 40.769802)
passenger_count = st.number_input("Passenger Count",min_value=1, max_value=10, value=1)



# Button to trigger prediction
if st.button("Predict Fare"):
    # Prepare the payload for the API request
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    # Make a POST request to the API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json()
        fare = prediction.get('fare', 'N/A')
        st.success(f"Predicted Fare: ${fare}")
    else:
        st.error("Failed to get prediction from API")
