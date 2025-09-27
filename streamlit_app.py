# ultimate_fix.py - TESTS ALL POSSIBLE ENDPOINTS
import streamlit as st
import requests

st.title("🔧 Gemini API Endpoint Tester")

API_KEY = "AIzaSyAMZY9NVc03yv96pajFGKJ9v7-XWxvmMbU"

# Test all possible endpoints
endpoints = [
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent", 
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent",
]

st.write("Testing all possible Gemini endpoints...")

for endpoint in endpoints:
    url = f"{endpoint}?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": "Say 'Hello'"}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            st.success(f"✅ WORKS: {endpoint}")
            st.json(response.json())
            break
        else:
            st.warning(f"❌ {response.status_code}: {endpoint}")
    except Exception as e:
        st.error(f"💥 Error: {endpoint} - {e}")

st.info("Copy the WORKING endpoint into the main app!")
