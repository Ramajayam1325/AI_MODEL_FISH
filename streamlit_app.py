# streamlit_app.py with Gemini API (Free)
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure Gemini (Free tier available)
def setup_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if api_key:
        genai.configure(api_key=api_key)
    return api_key

def analyze_with_gemini(image, context=""):
    """Analyze fish image using Gemini Pro Vision"""
    model = genai.GenerativeModel('gemini-pro-vision')
    
    prompt = f"""
    You are a marine biology expert. Analyze this fish image and provide:
    
    1. Possible species identification (top 3 guesses)
    2. Distinctive features observed
    3. Habitat information
    4. Interesting facts
    
    Additional context: {context}
    
    Be scientific but engaging in your response.
    """
    
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Gemini analysis unavailable. Demo mode activated.\nError: {e}"

def main():
    st.title("🐟 AI Fish Species Analyzer (Gemini)")
    
    # API setup
    api_key = setup_gemini()
    
    if not api_key:
        st.info("""
        **Using Demo Mode** - For full functionality:
        1. Get free Gemini API key: https://aistudio.google.com/
        2. Add `GEMINI_API_KEY` to your secrets
        """)
    
    uploaded_file = st.file_uploader("Upload fish image", type=['jpg', 'png', 'jpeg'])
    context = st.text_input("Additional context (optional):")
    
    if uploaded_file and st.button("Analyze"):
        with st.spinner("Analyzing with AI..."):
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            if api_key:
                analysis = analyze_with_gemini(image, context)
            else:
                analysis = demo_analysis(image, context)
            
            st.subheader("🔍 Analysis Results")
            st.write(analysis)

def demo_analysis(image, context):
    """Free demo analysis without API"""
    return f"""
**🐠 Demo Fish Analysis Results**

**Image Analysis:**
- Dimensions: {image.size[0]} × {image.size[1]} pixels
- Color Mode: {image.mode}
- Context: {context if context else 'Not provided'}

**Species Identification:**
Based on visual characteristics, this fish appears to be a tropical species commonly found in coral reef environments.

**Key Features:**
- Vibrant coloration patterns
- Streamlined body shape for efficient swimming
- Adapted for reef habitat navigation

**Habitat Information:**
Likely inhabits warm tropical waters between 24-28°C, commonly found in coral reef ecosystems.

*💡 For accurate species identification, add a free Gemini API key from Google AI Studio.*
"""

if __name__ == "__main__":
    main()
