# streamlit_app.py - COMPLETE FREE VERSION
import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="🐟 Free AI Fish Analyzer",
    page_icon="🐟",
    layout="wide"
)

class FreeFishAnalyzer:
    def __init__(self):
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", "")
        self.huggingface_key = st.secrets.get("HUGGINGFACE_API_KEY", "")
    
    def analyze_image(self, image, context=""):
        """Try multiple free APIs in sequence"""
        
        # Try Gemini first
        if self.gemini_key:
            result = self._try_gemini(image, context)
            if "Error" not in result:
                return {"source": "Gemini AI", "analysis": result}
        
        # Try Hugging Face next
        if self.huggingface_key:
            result = self._try_huggingface(image, context)
            if "Error" not in result:
                return {"source": "Hugging Face", "analysis": result}
        
        # Fallback to demo analysis
        return {"source": "Demo Mode", "analysis": self._demo_analysis(image, context)}
    
    def _try_gemini(self, image, context):
        """Try Google Gemini API"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            model = genai.GenerativeModel('gemini-pro-vision')
            
            prompt = f"""
            As a marine biology expert, analyze this fish image:
            
            CONTEXT: {context}
            
            Provide:
            1. Species identification attempts
            2. Distinctive features
            3. Habitat information
            4. Interesting facts
            
            Be scientific but engaging.
            """
            
            response = model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _try_huggingface(self, image, context):
        """Try Hugging Face API"""
        try:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
            headers = {"Authorization": f"Bearer {self.huggingface_key}"}
            
            response = requests.post(API_URL, headers=headers, data=img_str)
            predictions = response.json()
            
            return f"Image classification: {predictions[:3]}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _demo_analysis(self, image, context):
        """Free demo analysis"""
        return f"""
**🔍 AI Fish Analysis (Demo Mode)**

**📊 Image Details:**
- Resolution: {image.size[0]} × {image.size[1]} pixels
- Color Mode: {image.mode}
- Context: {context if context else 'Not provided'}

**🐠 Preliminary Analysis:**
This image appears to show a fish species with characteristics suitable for detailed AI analysis. 

**💡 To enhance accuracy:**
1. **Get free API keys:**
   - Gemini: https://aistudio.google.com/ (Recommended)
   - Hugging Face: https://huggingface.co/settings/tokens

2. **Add keys to your Streamlit secrets**

3. **Upload clear, well-lit fish images**

**🎯 This demo shows the complete functionality - adding API keys will enable real AI analysis!**
"""

def main():
    st.title("🐟 AI Fish Species Analyzer")
    st.markdown("### *Free & Open Source Version*")
    
    analyzer = FreeFishAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Setup Guide")
        st.markdown("""
        **Free API Keys:**
        1. **Gemini**: [Google AI Studio](https://aistudio.google.com/)
        2. **Hugging Face**: [HF Settings](https://huggingface.co/settings/tokens)
        
        **Add to `.streamlit/secrets.toml`:**
        ```toml
        GEMINI_API_KEY = "your_key_here"
        HUGGINGFACE_API_KEY = "your_key_here"
        ```
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("📤 Upload Fish Image", type=['jpg', 'png', 'jpeg'])
        context = st.text_area("📝 Additional Context", placeholder="Where was this taken? Any specific details?")
    
    with col2:
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🚀 Analyze with AI", type="primary"):
                with st.spinner("Analyzing image..."):
                    result = analyzer.analyze_image(image, context)
                    
                    st.success(f"Analysis complete! (Source: {result['source']})")
                    st.markdown("---")
                    st.subheader("🔍 Analysis Results")
                    st.write(result['analysis'])
        
        else:
            st.info("👆 Upload a fish image to get started!")

if __name__ == "__main__":
    main()
