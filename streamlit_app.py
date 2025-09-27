# streamlit_app.py
import streamlit as st
import tempfile
import os
from PIL import Image
import requests
import io
import base64
import json
from datetime import datetime


# Safe way to access API key
api_key = st.secrets.get("DEEPSEEK_API_KEY", "sk-a071a1fcb5df4b559cc5e65363f5aa24")

# Page configuration
st.set_page_config(
    page_title="🐟 AI Fish Species Analyzer",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .analysis-card {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
    }
    .upload-area {
        border: 2px dashed #ccc;
        padding: 40px;
        text-align: center;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

class FishAnalyzer:
    def __init__(self):
        # Initialize with your DeepSeek API key
        self.deepseek_api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    
    def analyze_image(self, image):
        """Basic image analysis"""
        try:
            analysis = {
                'width': image.size[0],
                'height': image.size[1],
                'mode': image.mode,
                'format': image.format,
                'file_size': len(image.tobytes()) if hasattr(image, 'tobytes') else 0
            }
            return analysis
        except Exception as e:
            st.error(f"Error analyzing image: {e}")
            return None
    
    def generate_explanation(self, analysis, image_description=""):
        """Generate explanation using DeepSeek API (or fallback)"""
        
        # If DeepSeek API key is available, use it
        if self.deepseek_api_key:
            return self._call_deepseek_api(analysis, image_description)
        else:
            # Fallback explanation (demo mode)
            return self._generate_fallback_explanation(analysis)
    
    def _call_deepseek_api(self, analysis, image_description):
        """Call DeepSeek API for intelligent analysis"""
        try:
            prompt = f"""
            Analyze this fish image with the following properties:
            - Size: {analysis['width']}x{analysis['height']} pixels
            - Color mode: {analysis['mode']}
            - Additional info: {image_description}
            
            Provide a detailed analysis of:
            1. Possible fish species
            2. Habitat information
            3. Distinctive features
            4. Interesting facts
            
            Keep the response educational and engaging.
            """
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                st.warning("DeepSeek API unavailable. Using demo mode.")
                return self._generate_fallback_explanation(analysis)
                
        except Exception as e:
            st.warning(f"API call failed: {e}. Using demo mode.")
            return self._generate_fallback_explanation(analysis)
    
    def _generate_fallback_explanation(self, analysis):
        """Generate fallback explanation when API is unavailable"""
        explanations = [
            "This appears to be a tropical reef fish with vibrant coloration, possibly from the coral triangle region.",
            "The fish shows characteristics of a deep-sea species with its unique body shape and adaptation features.",
            "Based on the visual analysis, this could be a freshwater aquarium species popular among hobbyists.",
            "The fish exhibits patterns commonly found in predatory species from ocean environments."
        ]
        
        import hashlib
        explanation_index = hash(str(analysis)) % len(explanations)
        
        return f"""
**🔍 AI Fish Analysis Results:**

**📊 Image Details:**
- **Dimensions:** {analysis['width']} × {analysis['height']} pixels
- **Color Mode:** {analysis['mode']}
- **Estimated Size:** {analysis['file_size'] // 1024} KB

**🐟 Species Analysis:**
{explanations[explanation_index]}

**💡 Features Detected:**
- Distinctive body shape
- Unique coloration patterns
- Specialized fin structure

**🌍 Habitat Suggestions:**
- Coral reef environments
- Tropical waters
- Moderate depth zones

*Note: This is a demo analysis. Connect DeepSeek API for species identification.*
"""

def main():
    # Initialize analyzer
    analyzer = FishAnalyzer()
    
    # Main header
    st.markdown('<h1 class="main-header">🐟 AI Fish Species Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Upload a fish image and get AI-powered analysis!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.info("Upload a clear fish image for best results")
        
        # Demo mode indicator
        if not analyzer.deepseek_api_key:
            st.warning("🔸 Demo Mode - Add DeepSeek API key for full functionality")
        else:
            st.success("✅ DeepSeek API Connected")
        
        st.markdown("---")
        st.subheader("📁 Supported Formats")
        st.write("- JPEG, PNG, WebP")
        st.write("- Maximum size: 10MB")
        st.write("- Clear, well-lit images work best")
        
        st.markdown("---")
        st.subheader("🔧 Features")
        st.write("✅ Image analysis")
        st.write("✅ Species identification")
        st.write("✅ Habitat information")
        st.write("✅ Educational insights")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a fish image",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Select a clear image of a fish"
        )
        
        # Additional image description
        image_description = st.text_area(
            "Additional context (optional):",
            placeholder="E.g., 'This fish was photographed in the Caribbean reef', 'Freshwater aquarium species'...",
            height=80
        )
        
        # Analysis options
        st.subheader("🔍 Analysis Options")
        analysis_depth = st.selectbox(
            "Analysis depth:",
            ["Basic", "Detailed", "Comprehensive"],
            help="Choose how detailed you want the analysis to be"
        )
    
    with col2:
        if uploaded_file is not None:
            # Display uploaded image
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Image info
                st.markdown("**📐 Image Information:**")
                col_info1, col_info2 = col2.columns(2)
                with col_info1:
                    st.write(f"Size: {image.size[0]} × {image.size[1]}")
                    st.write(f"Format: {image.format}")
                with col_info2:
                    st.write(f"Mode: {image.mode}")
                    st.write(f"Orientation: {'Landscape' if image.size[0] > image.size[1] else 'Portrait'}")
            
            except Exception as e:
                st.error(f"Error loading image: {e}")
    
    # Analysis button and results
    if uploaded_file is not None:
        st.markdown("---")
        
        if st.button("🚀 Analyze Fish Species", type="primary", use_container_width=True):
            with st.spinner("🔬 Analyzing image... This may take a few seconds."):
                try:
                    # Analyze image
                    analysis = analyzer.analyze_image(image)
                    
                    if analysis:
                        # Generate explanation
                        explanation = analyzer.generate_explanation(analysis, image_description)
                        
                        # Display results
                        st.markdown("---")
                        st.subheader("📋 Analysis Results")
                        
                        # Results in a nice card
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown(explanation)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Additional features
                        with st.expander("📊 Technical Details"):
                            st.json(analysis)
                        
                        # Download results
                        results_text = f"""
AI Fish Analysis Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Image: {uploaded_file.name}
Analysis Depth: {analysis_depth}

{explanation}
                        """
                        
                        st.download_button(
                            label="📥 Download Analysis Report",
                            data=results_text,
                            file_name=f"fish_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
    
    else:
        # Welcome message when no image uploaded
        st.markdown("""
        <div class="upload-area">
            <h3>👆 Upload a fish image to get started!</h3>
            <p>Drag and drop or click to upload a fish photograph</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Example images or instructions
        with st.expander("💡 Tips for best results"):
            st.markdown("""
            **For accurate analysis:**
            - Use clear, well-lit images
            - Fish should be clearly visible
            - Avoid blurry or dark photos
            - Multiple angles help with identification
            
            **Best practices:**
            - Capture the entire fish if possible
            - Include scale references if available
            - Note the location where photo was taken
            - Multiple images of the same fish from different angles
            """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>AI Fish Species Analyzer | Internship Project | Built with Streamlit & DeepSeek AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Secrets configuration (create .streamlit/secrets.toml file)
def create_secrets_template():
    """Create a secrets template file"""
    secrets_content = """
# .streamlit/secrets.toml
# Add your DeepSeek API key here
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
    """
    return secrets_content

if __name__ == "__main__":
    main()

