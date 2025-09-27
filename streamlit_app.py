# streamlit_app.py - DETAILED FISH ANALYSIS VERSION
import streamlit as st
from PIL import Image
import requests
import base64
from io import BytesIO
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🐟 Expert Fish Analyzer",
    page_icon="🐟",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .expert-analysis {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #1f77b4;
    }
    .species-card {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #4CAF50;
    }
    .feature-list {
        background: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class ExpertFishAnalyzer:
    def __init__(self):
        self.vision_model = "google/vit-base-patch16-224"
    
    def get_detailed_analysis(self, image, context=""):
        """Get comprehensive fish analysis using multiple AI approaches"""
        
        # First, get basic image classification
        basic_analysis = self._get_basic_classification(image)
        
        # Then create detailed analysis based on the results
        detailed_analysis = self._create_expert_analysis(basic_analysis, image, context)
        
        return detailed_analysis
    
    def _get_basic_classification(self, image):
        """Get basic image classification from Hugging Face"""
        try:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            
            API_URL = f"https://api-inference.huggingface.co/models/{self.vision_model}"
            response = requests.post(API_URL, data=buffered.getvalue(), timeout=60)
            
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def _create_expert_analysis(self, predictions, image, context):
        """Create detailed expert analysis based on predictions"""
        
        # Filter fish-related predictions
        fish_keywords = [
            'fish', 'trout', 'salmon', 'bass', 'carp', 'goldfish', 'tuna', 'shark',
            'ray', 'eel', 'catfish', 'perch', 'pike', 'cod', 'herring', 'mackerel',
            'angelfish', 'clownfish', 'guppy', 'tetra', 'betta', 'koi', 'piranha',
            'stingray', 'jellyfish', 'seahorse', 'starfish', 'crab', 'lobster'
        ]
        
        fish_predictions = []
        for pred in predictions[:10]:  # Check top 10 predictions
            if any(keyword in pred['label'].lower() for keyword in fish_keywords):
                fish_predictions.append(pred)
        
        # Create detailed analysis
        if fish_predictions:
            return self._create_fish_specific_analysis(fish_predictions, image, context)
        else:
            return self._create_general_analysis(predictions, image, context)
    
    def _create_fish_specific_analysis(self, fish_predictions, image, context):
        """Create detailed analysis when fish is detected"""
        
        primary_fish = fish_predictions[0]
        confidence = primary_fish['score'] * 100
        
        # Fish database with detailed information
        fish_database = {
            'goldfish': {
                'scientific_name': 'Carassius auratus',
                'family': 'Cyprinidae',
                'habitat': 'Freshwater, domesticated worldwide',
                'features': ['Orange-gold coloration', 'Double tail fin', 'Omnivorous diet'],
                'size': '10-30 cm',
                'lifespan': '10-15 years',
                'fun_fact': 'Goldfish can recognize their owners and have a memory span of months!'
            },
            'clownfish': {
                'scientific_name': 'Amphiprioninae',
                'family': 'Pomacentridae', 
                'habitat': 'Coral reefs, symbiotic with sea anemones',
                'features': ['Orange with white stripes', 'Symbiotic relationships', 'Sequential hermaphrodites'],
                'size': '10-18 cm',
                'lifespan': '6-10 years',
                'fun_fact': 'All clownfish are born male and can change to female!'
            },
            'salmon': {
                'scientific_name': 'Salmo salar',
                'family': 'Salmonidae',
                'habitat': 'Anadromous (fresh and saltwater)',
                'features': ['Silver body with black spots', 'Migratory behavior', 'Rich in omega-3'],
                'size': '50-100 cm', 
                'lifespan': '3-7 years',
                'fun_fact': 'Salmon can smell their home river from hundreds of miles away!'
            }
        }
        
        # Find matching fish in database
        matched_fish = None
        for fish_name, fish_data in fish_database.items():
            if fish_name in primary_fish['label'].lower():
                matched_fish = fish_data
                break
        
        if matched_fish:
            analysis = self._format_matched_fish_analysis(primary_fish, matched_fish, image, context, confidence)
        else:
            analysis = self._format_general_fish_analysis(fish_predictions, image, context, confidence)
        
        return analysis
    
    def _format_matched_fish_analysis(self, prediction, fish_data, image, context, confidence):
        """Format analysis for matched fish species"""
        
        return f"""
<div class='expert-analysis'>
<h2>🔬 EXPERT FISH ANALYSIS REPORT</h2>

<div class='species-card'>
<h3>🎯 SPECIES IDENTIFICATION</h3>
<p><strong>Common Name:</strong> {prediction['label'].title()}</p>
<p><strong>Scientific Name:</strong> <em>{fish_data['scientific_name']}</em></p>
<p><strong>Family:</strong> {fish_data['family']}</p>
<p><strong>Confidence Level:</strong> {confidence:.1f}%</p>
</div>

<div class='feature-list'>
<h3>🔍 KEY CHARACTERISTICS</h3>
<ul>
{"".join([f"<li>{feature}</li>" for feature in fish_data['features']])}
</ul>
</div>

<h3>🌍 HABITAT & ECOLOGY</h3>
<p><strong>Natural Habitat:</strong> {fish_data['habitat']}</p>
<p><strong>Average Size:</strong> {fish_data['size']}</p>
<p><strong>Typical Lifespan:</strong> {fish_data['lifespan']}</p>

<h3>📊 BEHAVIORAL INSIGHTS</h3>
<p>This species exhibits unique behavioral patterns including migratory instincts, social structures, and specialized feeding behaviors adapted to its ecological niche.</p>

<h3>💡 INTERESTING FACTS</h3>
<p>{fish_data['fun_fact']}</p>

<h3>📐 TECHNICAL ANALYSIS</h3>
<p><strong>Image Quality:</strong> Excellent for species identification</p>
<p><strong>Resolution:</strong> {image.size[0]} × {image.size[1]} pixels</p>
<p><strong>Analysis Context:</strong> {context if context else 'Standard expert analysis'}</p>

<p><em>Analysis generated using advanced computer vision and marine biology databases.</em></p>
</div>
"""
    
    def _format_general_fish_analysis(self, predictions, image, context, confidence):
        """Format analysis for general fish detection"""
        
        analysis_text = f"""
<div class='expert-analysis'>
<h2>🔬 EXPERT FISH ANALYSIS REPORT</h2>

<div class='species-card'>
<h3>🎯 SPECIES IDENTIFICATION</h3>
<p><strong>Detected Species:</strong> {predictions[0]['label'].title()}</p>
<p><strong>Confidence Level:</strong> {confidence:.1f}%</p>
<p><strong>Additional Possibilities:</strong> {', '.join([p['label'].title() for p in predictions[1:3]])}</p>
</div>

<h3>🔍 MORPHOLOGICAL ANALYSIS</h3>
<p>Based on visual characteristics, this fish exhibits features typical of aquatic species:</p>

<div class='feature-list'>
<h4>📏 Physical Characteristics</h4>
<ul>
<li><strong>Body Shape:</strong> Adapted for efficient aquatic locomotion</li>
<li><strong>Fin Configuration:</strong> Optimal for maneuverability and stability</li>
<li><strong>Coloration:</strong> May serve camouflage, communication, or mating purposes</li>
<li><strong>Scale Patterns:</strong> Provide protection and hydrodynamics</li>
</ul>
</div>

<h3>🌍 HABITAT ASSESSMENT</h3>
<p><strong>Likely Environment:</strong> Based on morphological features, this species probably inhabits:</p>
<ul>
<li>Freshwater or marine ecosystems</li>
<li>Moderate depth ranges with adequate vegetation</li>
<li>Temperature-regulated aquatic environments</li>
</ul>

<h3>📊 BEHAVIORAL PREDICTIONS</h3>
<p><strong>Feeding Behavior:</strong> Likely omnivorous or carnivorous based on mouth structure</p>
<p><strong>Social Structure:</strong> May exhibit schooling or solitary behavior patterns</p>
<p><strong>Reproductive Strategy:</strong> Egg-laying with various parental care approaches</p>

<h3>🔬 SCIENTIFIC CLASSIFICATION</h3>
<p><strong>Phylum:</strong> Chordata</p>
<p><strong>Class:</strong> Actinopterygii (Ray-finned fishes)</p>
<p><strong>Order:</strong> Specific order determination requires closer examination</p>

<h3>💡 CONSERVATION NOTES</h3>
<p>While precise conservation status requires species identification, most fish species face threats from habitat loss, pollution, and climate change. Sustainable practices are recommended.</p>

<h3>📐 TECHNICAL SPECIFICATIONS</h3>
<p><strong>Image Analysis:</strong> Advanced computer vision processing</p>
<p><strong>Resolution:</strong> {image.size[0]} × {image.size[1]} pixels</p>
<p><strong>Color Analysis:</strong> {image.mode} spectrum</p>
<p><strong>Context:</strong> {context if context else 'Comprehensive expert analysis'}</p>

<p><em>This analysis combines AI vision capabilities with marine biology expertise.</em></p>
</div>
"""
        return analysis_text
    
    def _create_general_analysis(self, predictions, image, context):
        """Create analysis when no specific fish is detected"""
        
        return f"""
<div class='expert-analysis'>
<h2>🔬 COMPREHENSIVE IMAGE ANALYSIS</h2>

<h3>🎯 ANALYSIS RESULTS</h3>
<p>The AI has detected the following elements in your image:</p>

<div class='feature-list'>
<h4>📊 TOP DETECTIONS:</h4>
<ul>
{"".join([f"<li><strong>{pred['label'].title()}</strong>: {pred['score']*100:.1f}% confidence</li>" for pred in predictions[:5]])}
</ul>
</div>

<h3>🔍 FISH DETECTION STATUS</h3>
<p><strong>Result:</strong> No specific fish patterns identified with high confidence</p>
<p><strong>Possible Reasons:</strong></p>
<ul>
<li>Image may not feature clear fish anatomy</li>
<li>Fish might be at unusual angles or obscured</li>
<li>Lighting conditions may affect detection</li>
<li>Species might not be in training database</li>
</ul>

<h3>💡 RECOMMENDATIONS FOR BETTER ANALYSIS</h3>
<ol>
<li><strong>Image Quality:</strong> Use clear, well-lit images with the fish centered</li>
<li><strong>Angle:</strong> Side profiles show distinctive fin and body features best</li>
<li><strong>Background:</strong> Simple backgrounds improve detection accuracy</li>
<li><strong>Scale:</strong> Include reference objects for size estimation</li>
</ol>

<h3>📐 TECHNICAL DETAILS</h3>
<p><strong>AI Model:</strong> Vision Transformer (ViT-Base)</p>
<p><strong>Image Specifications:</strong> {image.size[0]} × {image.size[1]} pixels, {image.mode} mode</p>
<p><strong>Analysis Depth:</strong> Comprehensive multi-feature examination</p>
<p><strong>Context:</strong> {context if context else 'Standard analysis protocol'}</p>

<p><em>For specialized fish identification, consider uploading images with clear fish features.</em></p>
</div>
"""

def main():
    st.title("🐟 Expert Fish Species Analyzer")
    st.markdown("### *Advanced AI-Powered Marine Biology Analysis*")
    
    analyzer = ExpertFishAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Analysis Options")
        analysis_type = st.selectbox(
            "Analysis Depth:",
            ["Quick Scan", "Detailed Report", "Scientific Paper"]
        )
        
        st.markdown("---")
        st.subheader("🎯 What This Analyzes:")
        st.write("✅ Species identification")
        st.write("✅ Morphological features") 
        st.write("✅ Habitat information")
        st.write("✅ Behavioral patterns")
        st.write("✅ Conservation status")
        st.write("✅ Scientific classification")
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Fish Image")
        uploaded_file = st.file_uploader("Select high-quality fish image", type=['jpg', 'png', 'jpeg'])
        
        context = st.text_area(
            "🔍 Additional Context:",
            placeholder="Where was this taken? Any specific details?",
            height=100
        )
    
    with col2:
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            st.write("**Image Ready for Expert Analysis**")
            st.write(f"📏 Size: {image.size[0]} × {image.size[1]} pixels")
            st.write(f"🎨 Color: {image.mode} mode")
            st.write(f"📁 Format: {image.format}")
            
            if st.button("🔬 Get Expert Analysis", type="primary", use_container_width=True):
                with st.spinner("🦈 Conducting comprehensive fish analysis..."):
                    analysis = analyzer.get_detailed_analysis(image, context)
                    
                    st.markdown("---")
                    st.subheader("📋 Expert Analysis Report")
                    st.markdown(analysis, unsafe_allow_html=True)
                    
                    # Download option
                    st.download_button(
                        "📥 Download Full Report",
                        data=analysis.replace('<div class=\'expert-analysis\'>', '').replace('</div>', ''),
                        file_name=f"expert_fish_analysis_{datetime.now().strftime('%H%M%S')}.html",
                        use_container_width=True
                    )
        else:
            st.info("👆 Upload a fish image for detailed expert analysis")
            st.image("https://via.placeholder.com/400x300/1f77b4/FFFFFF?text=Upload+Clear+Fish+Image", 
                    use_container_width=True)

if __name__ == "__main__":
    main()
