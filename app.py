# Save a beautiful Streamlit app to app.py
import streamlit as st
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("solar_model.pkl", "rb"))

# Page settings
st.set_page_config(page_title="Solar Power Predictor", page_icon="⚡", layout="centered")

# Title
st.markdown("<h1 style='color:#ffa500; text-align:center;'>⚡ Solar Power Prediction (kW)</h1>", unsafe_allow_html=True)
st.write("Enter weather/environmental inputs to estimate average solar power output (in kW over 3 hours).")
st.markdown("---")

# Input fields (11 total, matching model)
col1, col2 = st.columns(2)

with col1:
    distance = st.number_input("🌍 Distance to solar noon", value=0.1)
    temperature = st.number_input("🌡️ Temperature (°C)", value=25.0)
    wind_dir = st.number_input("🧭 Wind Direction (°)", value=180.0)
    wind_speed = st.number_input("💨 Wind Speed (m/s)", value=2.5)

with col2:
    sky_cover = st.selectbox("☁️ Sky Cover (0 = clear → 4 = covered)", [0, 1, 2, 3, 4])
    visibility = st.number_input("🔭 Visibility (km)", value=10.0)
    humidity = st.slider("💧 Humidity (%)", 0, 100, 60)
    avg_wind = st.number_input("🌀 Avg. Wind Speed (3h)", value=2.5)
    pressure = st.number_input("📈 Avg. Pressure (inHg)", value=29.9)


# Predict button
if st.button("⚡ Predict Power (kW)"):
    input_data = np.array([[distance, temperature, wind_dir, wind_speed,
                            sky_cover, visibility, humidity, avg_wind, pressure]])

    # Add 2 default values to make 11 features
    input_data = np.append(input_data, [0.0, 0.0]).reshape(1, -1)

    prediction_joules = model.predict(input_data)[0]
    power_kw = prediction_joules / 10800
    st.success(f"🔋 Estimated Average Power: {power_kw:.4f} kW")
