# test_new_key.py
import streamlit as st
import requests

st.title("🔧 Testing New API Key")

API_KEY = "AIzaSyAyvuF6iyBERQjvbs7AsgKW-ekdVI18DrA"

# Test multiple endpoints
endpoints = [
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
]

for endpoint in endpoints:
    url = f"{endpoint}?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": "Say 'API is working!' in one word."}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ SUCCESS with {endpoint}")
            st.write("Response:", result['candidates'][0]['content']['parts'][0]['text'])
            break
        else:
            st.warning(f"❌ {response.status_code} with {endpoint}")
    except Exception as e:
        st.error(f"💥 Error with {endpoint}: {e}")
