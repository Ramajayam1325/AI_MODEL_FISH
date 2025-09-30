import streamlit as st
from PIL import Image
import requests
import json
import base64
from io import BytesIO
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🐟 Fish Analyzer Pro",
    page_icon="🐟",
    layout="wide"
)

st.title("🐟 AI Fish Species Analyzer Pro")
st.markdown("### *Powered by Google Gemini AI*")

class GeminiFishAnalyzer:
    def __init__(self):
        self.api_key = st.secrets.get("GEMINI_API_KEY", "")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent"
    
    def analyze_fish_image(self, image, context=""):
        """Analyze fish image using Gemini Pro Vision"""
        if not self.api_key:
            return "❌ API key not configured", 0.0
        
        try:
            # Convert image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            url = f"{self.base_url}?key={self.api_key}"
            
            prompt = self._create_analysis_prompt(context)
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_base64
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result['candidates'][0]['content']['parts'][0]['text']
                return analysis_text, True
            else:
                return f"❌ API Error: {response.status_code}", False
                
        except Exception as e:
            return f"❌ Error: {str(e)}", False
    
    def _create_analysis_prompt(self, context):
        return f"""
        You are Dr. Marina Biologist, an expert marine biologist with 25 years of experience.
        
        Analyze this fish image and provide a comprehensive scientific report.
        
        USER CONTEXT: {context if context else "No additional context provided"}
        
        Please provide detailed analysis covering:
        
        **SPECIES IDENTIFICATION**
        - Most likely species (common and scientific names)
        - Confidence level and reasoning
        - Alternative possibilities
        
        **MORPHOLOGICAL ANALYSIS**
        - Body shape and size characteristics
        - Coloration patterns and distinctive markings
        - Fin structure and special adaptations
        - Mouth shape and eye position
        
        **HABITAT & ECOLOGY**
        - Natural habitat type (coral reef, freshwater, deep sea, etc.)
        - Geographical distribution range
        - Typical depth and water conditions
        - Feeding behavior and diet
        
        **BEHAVIORAL CHARACTERISTICS**
        - Social structure (solitary, schooling, etc.)
        - Reproductive behavior
        - Defensive mechanisms
        
        **CONSERVATION STATUS**
        - IUCN Red List status if identifiable
        - Major threats and conservation efforts
        
        **INTERESTING FACTS**
        - Unique biological adaptations
        - Cultural or economic significance
        
        Be scientific but engaging. If identification is uncertain, explain what features are visible and what would help with better identification.
        
        Format the response with clear section headings and bullet points for readability.
        """

# Initialize analyzer
analyzer = GeminiFishAnalyzer()

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if analyzer.api_key:
        st.success("✅ Gemini API: Configured")
    else:
        st.error("❌ Gemini API: Not configured")
        st.info("Add GEMINI_API_KEY to .streamlit/secrets.toml")
    
    st.markdown("---")
    st.subheader("🔧 Features")
    st.write("✅ Real AI analysis")
    st.write("✅ Species identification")
    st.write("✅ Habitat information")
    st.write("✅ Professional reporting")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Fish Image")
    
    uploaded_file = st.file_uploader(
        "Choose a fish image",
        type=['jpg', 'jpeg', 'png'],
        help="Select a clear, well-lit fish image"
    )
    
    context = st.text_area(
        "🔍 Analysis Context",
        placeholder="Where was this photo taken? Any specific details?",
        height=80
    )

with col2:
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Image info
        with st.expander("📐 Image Details"):
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**Size:** {image.size[0]} × {image.size[1]}")
                st.write(f"**Format:** {image.format}")
            with col_info2:
                st.write(f"**Mode:** {image.mode}")
                st.write(f"**Type:** {'Color' if image.mode == 'RGB' else 'Grayscale'}")
        
        # Analyze button
        if st.button("🚀 Analyze with Gemini AI", type="primary", use_container_width=True):
            with st.spinner("🔬 Gemini AI is analyzing your image..."):
                analysis, success = analyzer.analyze_fish_image(image, context)
                
                st.markdown("---")
                st.subheader("📋 Analysis Results")
                
                if success:
                    st.success("✅ Gemini AI Analysis Complete!")
                    st.balloon()
                else:
                    st.error("❌ Analysis Failed")
                
                st.markdown(analysis)
                
                # Download results
                results_text = f"""
Fish Analysis Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Source: Google Gemini AI
Image: {uploaded_file.name}
Context: {context}

{analysis}
"""
                st.download_button(
                    "📥 Download Report",
                    data=results_text,
                    file_name=f"gemini_fish_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True
                )
    
    else:
        st.info("👆 Upload a fish image for AI analysis")
        st.image("https://via.placeholder.com/400x300/1f77b4/FFFFFF?text=Upload+Fish+Image", 
                use_container_width=True)

st.markdown("---")
st.write("Powered by Google Gemini AI • Professional Marine Biology Analysis")
