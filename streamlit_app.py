# streamlit_app.py - CORRECTED VERSION
import streamlit as st
from PIL import Image
import requests
import json
import base64
from io import BytesIO
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🐟 AI Fish Analyzer - Gemini Powered",
    page_icon="🐟",
    layout="wide"
)

st.title("🐟 AI Fish Species Analyzer")
st.markdown("### *Powered by Google Gemini AI*")

class CorrectGeminiAnalyzer:
    def __init__(self):
        self.api_key = "AIzaSyAMZY9NVc03yv96pajFGKJ9v7-XWxvmMbU"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
        self.is_connected = False
        self._test_connection()
    
    def _test_connection(self):
        """Test connection with correct endpoint"""
        try:
            url = f"{self.base_url}?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Just respond with the word 'Connected' and nothing else."
                    }]
                }]
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.is_connected = True
                st.success("✅ Gemini API Connected Successfully!")
            else:
                st.error(f"❌ API Error {response.status_code}: {response.text}")
                # Try alternative endpoint
                self._try_alternative_endpoint()
                
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
    
    def _try_alternative_endpoint(self):
        """Try alternative endpoint"""
        try:
            alt_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Test connection"
                    }]
                }]
            }
            
            response = requests.post(alt_url, json=payload, timeout=10)
            if response.status_code == 200:
                self.is_connected = True
                self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
                st.success("✅ Connected using alternative endpoint!")
            else:
                st.error(f"❌ Alternative endpoint also failed: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ Alternative endpoint failed: {e}")
    
    def analyze_image(self, image, context=""):
        """Analyze image using Gemini"""
        if not self.is_connected:
            return self._demo_analysis(image, context)
        
        try:
            # Convert image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            url = f"{self.base_url}?key={self.api_key}"
            
            prompt = self._create_prompt(context)
            
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
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    analysis_text = result['candidates'][0]['content']['parts'][0]['text']
                    return {"source": "Gemini AI", "analysis": analysis_text, "success": True}
                else:
                    return {"source": "API Response Error", "analysis": self._demo_analysis(image, context), "success": False}
            else:
                return {"source": f"API Error {response.status_code}", "analysis": self._demo_analysis(image, context), "success": False}
                
        except Exception as e:
            return {"source": f"Error: {str(e)}", "analysis": self._demo_analysis(image, context), "success": False}
    
    def _create_prompt(self, context):
        return f"""
        You are an expert marine biologist. Analyze this fish image and provide a comprehensive report.

        USER CONTEXT: {context if context else "No additional context provided"}

        Please provide detailed analysis covering:

        1. **SPECIES IDENTIFICATION:**
           - Most likely species (common and scientific names)
           - Confidence level and reasoning
           - Alternative possibilities

        2. **MORPHOLOGICAL FEATURES:**
           - Body shape and size characteristics
           - Coloration patterns and markings
           - Fin structure and special adaptations

        3. **HABITAT & ECOLOGY:**
           - Natural habitat type
           - Geographical distribution
           - Behavioral characteristics

        4. **INTERESTING FACTS:**
           - Unique biological features
           - Conservation status if known
           - Scientific significance

        Be scientific but engaging. If identification is uncertain, explain what features are visible and what would help with better identification.
        """
    
    def _demo_analysis(self, image, context):
        """Enhanced demo analysis"""
        return f"""
**🔍 AI FISH ANALYSIS REPORT**

**📊 IMAGE TECHNICAL DETAILS**
- **Resolution:** {image.size[0]} × {image.size[1]} pixels
- **Color Mode:** {image.mode}
- **Analysis Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **User Context:** {context if context else 'Standard analysis'}

**🐠 PRELIMINARY ASSESSMENT**

Based on the image characteristics, this fish exhibits features commonly found in aquatic species. The visible morphology suggests adaptations for efficient swimming and survival in specific aquatic environments.

**🔬 OBSERVABLE CHARACTERISTICS:**
- Body shape suitable for aquatic locomotion
- Fin configuration supporting mobility
- Coloration patterns that may serve ecological functions

**🌍 HABITAT INFERENCE:**
The morphological features suggest adaptation to aquatic environments, possibly:
- Freshwater or marine habitats
- Tropical or temperate zones based on general characteristics
- Specific depth ranges based on body structure

**💡 ENHANCEMENT NOTES:**
*This analysis demonstrates the application's capability. With proper API configuration, the system would provide precise species identification using advanced AI analysis.*

**🎯 NEXT STEPS FOR RESEARCH-GRADE ANALYSIS:**
1. Ensure correct API endpoint configuration
2. Verify network connectivity
3. Check for any API usage limits or restrictions
"""

# Initialize analyzer
analyzer = CorrectGeminiAnalyzer()

# Display status
if analyzer.is_connected:
    st.success("🎉 Ready to analyze fish images!")
else:
    st.warning("🔸 Using demo mode - API connection issues")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader("Choose fish image", type=['jpg', 'jpeg', 'png'])
    
    context = st.text_area("Additional context:", placeholder="Where was this taken? Any details?")
    
    if uploaded_file:
        st.info("Image ready for analysis!")

with col2:
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("🚀 Analyze with AI", type="primary", use_container_width=True):
            with st.spinner("🔬 AI is analyzing your image..."):
                result = analyzer.analyze_image(image, context)
                
                st.markdown("---")
                st.subheader("📋 Analysis Results")
                
                if result['success']:
                    st.success("✅ AI Analysis Complete!")
                else:
                    st.warning("⚠️ Using enhanced demo analysis")
                
                st.markdown(result['analysis'])
                
                # Download option
                results_text = f"""
Fish Analysis Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Status: {'AI Analysis' if result['success'] else 'Demo Mode'}
Source: {result['source']}

{result['analysis']}
"""
                st.download_button(
                    "📥 Download Report",
                    data=results_text,
                    file_name=f"fish_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True
                )
    else:
        st.info("👆 Upload a fish image to begin analysis")

# Debug information
with st.expander("🔧 Technical Details"):
    st.write("**API Key:**", analyzer.api_key[:10] + "..." if analyzer.api_key else "Not set")
    st.write("**Endpoint:**", analyzer.base_url)
    st.write("**Connection Status:**", "Connected" if analyzer.is_connected else "Failed")
    st.write("**Last Check:**", datetime.now().strftime("%H:%M:%S"))

st.markdown("---")
st.markdown("*AI Fish Species Analyzer - Internship Project*")
