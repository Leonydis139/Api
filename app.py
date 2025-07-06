import streamlit as st
import requests
import os

# Set page config
st.set_page_config(page_title="QuantumRequest v2 Dashboard", page_icon="⚛️", layout="wide")

st.title("⚛️ QuantumRequest v2 Dashboard")

# Sidebar
st.sidebar.header("🔑 API Configuration")

# API Base URL and Key from environment variables or user input
API_URL = st.sidebar.text_input("Quantum API URL", os.getenv("QUANTUM_API_URL", "https://api-8lyl.onrender.com/quantum"))
API_KEY = st.sidebar.text_input("Quantum API Key", os.getenv("QUANTUM_API_KEY", ""), type="password")

# Display status
if API_KEY:
    st.sidebar.success("API Key Loaded ✅")
else:
    st.sidebar.warning("No API Key ⚠️")

# Form for Quantum Request
st.header("📤 Send Quantum Request")

with st.form(key='quantum_form'):
    intent = st.text_input("Intent", "refreshSession")
    user_id = st.number_input("User ID", min_value=1, value=1)
    cache_keys = st.text_area("Cache Keys (comma separated)", "profile,permissions")
    requested_components = st.text_area("Requested Components (comma separated)", "profile,permissions,notifications")
    submit_button = st.form_submit_button(label="Send Request")

if submit_button:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "intent": intent,
        "userId": user_id,
        "cacheKeys": [key.strip() for key in cache_keys.split(",") if key.strip()],
        "requestedComponents": [comp.strip() for comp in requested_components.split(",") if comp.strip()]
    }

    if not API_KEY or not API_URL:
        st.error("❌ Please provide both the API URL and API Key.")
    else:
        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                st.success("✅ Quantum Request Successful")
                st.json(response.json())
            elif response.status_code == 401:
                st.error("🚫 Unauthorized: Invalid API Key")
            else:
                st.error(f"⚠️ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.exception(e)

st.markdown("---")
st.caption("QuantumRequest Client © 2025")
