## streamlit_app.py
import streamlit as st
import requests
import json
from PIL import Image
import io

# Page config
st.set_page_config(page_title="AI Fish Analyzer", page_icon="🐟")

class DeepSeekAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
    
    def analyze_fish_image(self, image_info, user_context=""):
        """Analyze fish image using DeepSeek API"""
        
        prompt = f"""
        You are a marine biologist specializing in fish species identification.
        
        IMAGE INFORMATION:
        - Dimensions: {image_info['width']}x{image_info['height']} pixels
        - Color mode: {image_info['mode']}
        - User context: {user_context if user_context else 'No additional context provided'}
        
        Please provide a comprehensive analysis covering:
        1. **Possible species identification** (top 3 guesses with confidence levels)
        2. **Key identifying features** (body shape, coloration, fins, etc.)
        3. **Habitat and distribution**
        4. **Interesting facts or behaviors**
        5. **Conservation status** (if known)
        
        Be scientific but engaging. If identification is uncertain, mention what additional information would help.
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert marine biologist with extensive knowledge of fish species worldwide."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"API Error: {str(e)}"

def main():
    st.title("🐟 AI Fish Species Analyzer")
    
    # Initialize API (check if key exists)
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    
    if not api_key:
        st.warning("🔑 Please add your DeepSeek API key to continue")
        st.info("""
        **How to get your API key:**
        1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
        2. Sign up and verify your account
        3. Go to API Management
        4. Create a new API key
        5. Add it to your Streamlit secrets
        """)
        return
    
    analyzer = DeepSeekAPI(api_key)
    
    # File upload
    uploaded_file = st.file_uploader("Upload a fish image", type=['jpg', 'png', 'jpeg'])
    user_context = st.text_area("Additional context (optional):", placeholder="Where was this photo taken? Any specific details?")
    
    if uploaded_file and st.button("Analyze Fish"):
        with st.spinner("Analyzing image with DeepSeek AI..."):
            try:
                # Open and analyze image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Basic image info
                image_info = {
                    'width': image.size[0],
                    'height': image.size[1],
                    'mode': image.mode,
                    'format': image.format
                }
                
                # Get AI analysis
                analysis = analyzer.analyze_fish_image(image_info, user_context)
                
                # Display results
                st.subheader("🔍 AI Analysis Results")
                st.write(analysis)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
