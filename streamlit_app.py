# streamlit_app.py - GEMINI ONLY VERSION
import streamlit as st
from PIL import Image
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🐟 AI Fish Analyzer with Gemini",
    page_icon="🐟",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .analysis-card {
        background-color: #f0f8ff;
        padding: 25px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #1f77b4;
    }
    .gemini-badge {
        background-color: #4285f4;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 5px 0;
    }
    .upload-area {
        border: 2px dashed #ccc;
        padding: 40px;
        text-align: center;
        border-radius: 10px;
        margin: 20px 0;
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

class GeminiFishAnalyzer:
    def __init__(self):
        self.api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    def analyze_image(self, image, context=""):
        """Analyze fish image using Gemini Pro Vision"""
        
        # If no API key, use demo mode
        if not self.api_key or self.api_key == "your_gemini_key_here":
            return {"source": "Demo Mode", "analysis": self._demo_analysis(image, context)}
        
        # Try Gemini API
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro-vision')
            
            prompt = self._create_analysis_prompt(context)
            
            response = model.generate_content([prompt, image])
            return {"source": "Gemini AI", "analysis": response.text}
            
        except Exception as e:
            return {"source": "Gemini API Error", "analysis": self._demo_analysis(image, context, error=str(e))}
    
    def _create_analysis_prompt(self, context):
        """Create a detailed prompt for fish analysis"""
        return f"""
        You are an expert marine biologist with 20 years of experience in fish species identification. 
        Analyze this fish image and provide a comprehensive report.

        USER CONTEXT: {context if context else "No additional context provided"}

        Please provide a detailed analysis covering:

        **SPECIES IDENTIFICATION:**
        - Top 3 most likely species names (common and scientific names)
        - Confidence level for each identification
        - Distinctive features supporting the identification

        **MORPHOLOGICAL ANALYSIS:**
        - Body shape and size characteristics
        - Coloration patterns and markings
        - Fin structure and placement
        - Mouth shape and eye position

        **HABITAT & ECOLOGY:**
        - Most likely natural habitat
        - Geographical distribution
        - Typical depth range
        - Feeding behavior and diet

        **BEHAVIORAL INSIGHTS:**
        - Social behavior (solitary/schooling)
        - Reproductive characteristics
        - Defensive mechanisms

        **CONSERVATION STATUS:**
        - IUCN Red List status if identifiable
        - Threats and conservation efforts

        **INTERESTING FACTS:**
        - Unique biological adaptations
        - Cultural or economic significance
        - Research importance

        If the image quality makes identification difficult, specify what features are unclear and suggest what would help for better identification.

        Provide the analysis in a structured, educational format suitable for both scientists and enthusiasts.
        """
    
    def _demo_analysis(self, image, context, error=None):
        """Enhanced demo analysis when API is not available"""
        if error:
            error_note = f"\n\n**⚠️ API Error:** {error}\n"
        else:
            error_note = "\n\n**💡 Tip:** Add your Gemini API key to unlock real AI analysis!\n"

        return f"""
**🔍 AI FISH SPECIES ANALYSIS REPORT**

{error_note}

**📊 TECHNICAL SPECIFICATIONS**
- **Image Resolution:** {image.size[0]} × {image.size[1]} pixels
- **Color Profile:** {image.mode}
- **Analysis Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **User Context:** {context if context else 'Standard analysis protocol'}

**🐠 DEMO ANALYSIS RESULTS**

**Visual Assessment:**
The uploaded image displays characteristics consistent with teleost fish morphology. Based on general features observable in the demo preview:

**Potential Identification:**
- **Primary Guess:** Tropical reef-associated species
- **Family Likelihood:** Possibly Perciformes or Tetraodontiformes
- **Confidence Level:** Limited (demo mode)

**Observable Features:**
- Body shape suggesting efficient aquatic locomotion
- Coloration patterns typical of coral reef ecosystems
- Fin configuration supporting maneuverability

**Habitat Inference:**
Based on morphological characteristics, likely inhabits:
- Warm tropical waters (24-29°C)
- Coral reef or rocky substrate environments
- Moderate depth ranges (5-30 meters)

**RESEARCH-GRADE ANALYSIS AVAILABLE:**
To obtain precise species identification and detailed biological insights, please configure your Gemini API key.

**Next Steps:**
1. Visit [Google AI Studio](https://aistudio.google.com/) to get your API key
2. Add it to your Streamlit secrets configuration
3. Re-analyze your image for scientific-grade results

**📞 Support:**
This demo showcases the application's capability. Full functionality requires Gemini API integration.
"""

def main():
    st.markdown('<h1 class="main-header">🐟 AI Fish Species Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### *Powered by Google Gemini AI*")
    
    # Initialize analyzer
    analyzer = GeminiFishAnalyzer()
    
    # Sidebar with configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status
        st.subheader("🔑 API Status")
        if analyzer.api_key and analyzer.api_key != "your_gemini_key_here":
            st.success("✅ Gemini API: Connected")
            st.markdown('<div class="gemini-badge">Google Gemini Active</div>', unsafe_allow_html=True)
        else:
            st.warning("🔸 Gemini API: Not configured")
            st.info("Get free API key from [Google AI Studio](https://aistudio.google.com/)")
        
        st.markdown("---")
        
        # Setup Guide
        st.subheader("🚀 Quick Setup")
        st.markdown("""
        **1. Get API Key:**
        - Visit [Google AI Studio](https://aistudio.google.com/)
        - Create free account
        - Generate API key
        
        **2. Configure:**
        Create `.streamlit/secrets.toml`:
        ```toml
        GEMINI_API_KEY = "your_actual_key_here"
        ```
        """)
        
        st.markdown("---")
        
        # App Info
        st.subheader("📊 App Information")
        st.write(f"**Version:** 2.1.0")
        st.write(f"**Last Update:** {datetime.now().strftime('%Y-%m-%d')}")
        st.write("**AI Model:** Gemini Pro Vision")
        st.write("**Framework:** Streamlit")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Fish Image")
        
        uploaded_file = st.file_uploader(
            "Select fish image file", 
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Upload a clear image of a fish for AI analysis"
        )
        
        # Context input
        context = st.text_area(
            "**🎯 Analysis Context**", 
            placeholder="Example: 'Photo from Great Barrier Reef', 'Freshwater aquarium specimen', 'Deep-sea research photo'...",
            height=80
        )
        
        # Analysis options
        st.subheader("🔍 Analysis Mode")
        analysis_mode = st.radio(
            "Select analysis depth:",
            ["Quick Scan", "Detailed Report", "Scientific Grade"],
            help="Choose the level of detail for the analysis"
        )
    
    with col2:
        if uploaded_file is not None:
            try:
                # Open and display image
                image = Image.open(uploaded_file)
                
                st.subheader("🖼️ Image Preview")
                st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_container_width=True)
                
                # Image information
                with st.expander("📐 Image Details", expanded=True):
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.write(f"**Dimensions:** {image.size[0]} × {image.size[1]}")
                        st.write(f"**Format:** {image.format or 'Unknown'}")
                    with col_info2:
                        st.write(f"**Color Mode:** {image.mode}")
                        st.write(f"**File Size:** {len(uploaded_file.getvalue()) // 1024} KB")
                
                # Analyze button
                analyze_clicked = st.button(
                    "🚀 Analyze with Gemini AI", 
                    type="primary", 
                    use_container_width=True,
                    help="Click to analyze the image using Google Gemini AI"
                )
                
                if analyze_clicked:
                    with st.spinner("🔬 Gemini AI is analyzing your image... This may take 10-30 seconds."):
                        result = analyzer.analyze_image(image, context)
                        
                        # Display results
                        st.markdown("---")
                        st.subheader("📋 Analysis Results")
                        
                        # Source indicator
                        if result['source'] == "Gemini AI":
                            st.success("✅ **Analysis Complete using Google Gemini AI**")
                            st.balloon()  # Celebration effect
                        elif result['source'] == "Demo Mode":
                            st.warning("🔸 **Demo Analysis** - Add API key for Gemini AI")
                        else:
                            st.error("❌ **API Error** - Using demo mode")
                        
                        # Results in styled card
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown(result['analysis'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Download results
                        results_text = f"""
AI FISH ANALYSIS REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Source: {result['source']}
Image: {uploaded_file.name}
Analysis Mode: {analysis_mode}
Context: {context}

{result['analysis']}
                        """
                        
                        st.download_button(
                            label="📥 Download Full Report",
                            data=results_text,
                            file_name=f"fish_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
            
            except Exception as e:
                st.error(f"❌ Error processing image: {str(e)}")
                st.info("Please try uploading a different image file.")
        
        else:
            # Welcome message
            st.markdown("""
            <div class="upload-area">
                <h3>👆 Upload Your Fish Image</h3>
                <p>Drag and drop or click to upload a fish photograph</p>
                <p><strong>Gemini AI will analyze:</strong></p>
                <ul style="text-align: left; display: inline-block;">
                    <li>Species identification</li>
                    <li>Habitat information</li>
                    <li>Biological features</li>
                    <li>Conservation status</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Tips section
            with st.expander("💡 Tips for Best Results", expanded=True):
                st.markdown("""
                **📸 Image Quality:**
                - Use high-resolution, clear images
                - Good lighting without shadows
                - Focus on the fish's entire body
                - Multiple angles improve accuracy
                
                **🔬 Scientific Best Practices:**
                - Include scale references if possible
                - Note the geographical location
                - Capture distinctive features clearly
                - Provide context in the description box
                """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 20px;'>
            <p>🐟 AI Fish Species Analyzer | Internship Project | Powered by Google Gemini AI</p>
            <p>🎯 Professional Marine Biology Tool | 📅 Submission Ready</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
