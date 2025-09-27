# app.py - Save this as a separate file
import streamlit as st
import torch
import torch.nn.functional as F
from PIL import Image
import tempfile
import os
import matplotlib.pyplot as plt
import numpy as np
from torchvision import transforms

# Suppress the warnings
import warnings
warnings.filterwarnings('ignore')

# Set page config first
st.set_page_config(
    page_title="Fish Species Analyzer",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FishSpeciesClassifier:
    def __init__(self, model_path, classes_file):
        """Initialize the fish species classifier"""
        try:
            self.model = torch.jit.load(model_path, map_location='cpu')
            self.model.eval()
            
            with open(classes_file, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]
            
            self.transform = transforms.Compose([
                transforms.Resize((128, 128)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            
            st.success("✅ Model loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
    
    def predict(self, image):
        """Predict fish species from image"""
        try:
            # Convert to RGB if necessary
            if isinstance(image, np.ndarray):
                image = Image.fromarray(image)
            image = image.convert('RGB')
            
            # Apply transformations
            input_tensor = self.transform(image).unsqueeze(0)
            
            # Prediction
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = F.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
            
            # Get top 5 predictions
            top5_probs, top5_indices = torch.topk(probabilities, 5)
            top5_predictions = [
                (self.classes[i], top5_probs[0][j].item()) 
                for j, i in enumerate(top5_indices[0])
            ]
            
            return {
                'predicted_class': self.classes[predicted_idx.item()],
                'confidence': confidence.item(),
                'top_predictions': top5_predictions,
                'all_probabilities': probabilities[0].numpy()
            }
        except Exception as e:
            st.error(f"❌ Prediction error: {e}")
            return None

def main():
    st.title("🐟 AI Fish Species Analyzer")
    st.markdown("""
    Upload an image of a fish to identify its species using deep learning!
    The model can classify various fish species with high accuracy.
    """)
    
    # Initialize classifier
    classifier = FishSpeciesClassifier("best_fish_model_ts_pt.ipynb", "classes.txt")
    
    # Sidebar
    st.sidebar.title("About")
    st.sidebar.info(
        "This app uses a MobileNetV2 model trained on fish species dataset "
        "to classify fish images. Upload a clear image for best results."
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a fish image", 
        type=['jpg', 'png', 'jpeg'],
        help="Supported formats: JPG, PNG, JPEG"
    )
    
    if uploaded_file is not None:
        # Display image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📷 Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            # Image info
            st.write(f"**Image details:** {image.size[0]}x{image.size[1]} pixels, {image.mode} mode")
        
        with col2:
            st.subheader("🔍 Analysis")
            
            if st.button("Analyze Fish Species", type="primary", use_container_width=True):
                with st.spinner("Analyzing image... This may take a few seconds."):
                    results = classifier.predict(image)
                
                if results:
                    # Display results
                    confidence_percent = results['confidence'] * 100
                    
                    st.success(f"**Prediction:** {results['predicted_class']}")
                    st.metric("Confidence", f"{confidence_percent:.1f}%")
                    
                    # Confidence bar
                    st.progress(results['confidence'])
                    
                    # Top predictions
                    st.subheader("📊 Top 5 Predictions")
                    for i, (species, prob) in enumerate(results['top_predictions']):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{i+1}. {species}**")
                        with col2:
                            st.write(f"{prob*100:.2f}%")
                    
                    # Visualization
                    st.subheader("📈 Prediction Distribution")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    species_names = [pred[0] for pred in results['top_predictions']]
                    probabilities = [pred[1] for pred in results['top_predictions']]
                    
                    bars = ax.barh(species_names, probabilities, color='skyblue')
                    ax.set_xlabel('Probability')
                    ax.set_xlim(0, 1)
                    ax.set_title('Top 5 Predictions')
                    
                    # Add probability labels
                    for bar, prob in zip(bars, probabilities):
                        width = bar.get_width()
                        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                               f'{prob*100:.1f}%', ha='left', va='center')
                    
                    st.pyplot(fig)
                    
                    # Additional information based on confidence
                    if confidence_percent > 80:
                        st.success("✅ High confidence prediction!")
                    elif confidence_percent > 60:
                        st.warning("⚠️ Moderate confidence. Consider uploading a clearer image.")
                    else:
                        st.error("❌ Low confidence. The image might be unclear or contain multiple fish.")

    else:
        # Demo section when no file is uploaded
        st.info("👆 Please upload a fish image to get started!")
        
        # Sample images or instructions
        st.subheader("💡 Tips for best results:")
        st.markdown("""
        - Use clear, well-lit images
        - Focus on the fish as the main subject
        - Avoid blurry or distant shots
        - Single fish per image works best
        - Natural lighting provides better results
        """)

if __name__ == "__main__":
    main()


