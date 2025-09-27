# streamlit_app_fixed.py
import streamlit as st
import torch
import torch.nn as nn
from torchvision.models import mobilenet_v2
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from torchvision import transforms
import os

# Set page config
st.set_page_config(
    page_title="Fish Species Analyzer",
    page_icon="🐟",
    layout="wide"
)

class FishSpeciesClassifier:
    def __init__(self):
        """Initialize the fish species classifier with multiple loading options"""
        self.model = None
        self.classes = []
        
        # Try different loading methods
        self._try_load_model()
    
    def _try_load_model(self):
        """Try different methods to load the model"""
        loading_methods = [
            self._load_torchscript_model,
            self._load_pytorch_model,
            self._create_demo_model
        ]
        
        for method in loading_methods:
            if self.model is not None:
                break
            try:
                method()
            except Exception as e:
                st.warning(f"⚠️ {method.__name__} failed: {e}")
                continue
        
        # Load classes
        self._load_classes()
    
    def _load_torchscript_model(self):
        """Try loading TorchScript model"""
        model_files = ["best_fish_model_ts.pt", "fish_model_correct.pt", "model.pt"]
        
        for model_file in model_files:
            if os.path.exists(model_file):
                st.info(f"🔧 Loading TorchScript model: {model_file}")
                self.model = torch.jit.load(model_file, map_location='cpu')
                self.model.eval()
                st.success(f"✅ TorchScript model loaded from {model_file}")
                return
        
        st.warning("📭 No TorchScript model files found")
        raise FileNotFoundError("No TorchScript model files available")
    
    def _load_pytorch_model(self):
        """Try loading regular PyTorch model"""
        weight_files = ["fish_model_weights.pth", "model_weights.pth", "best_model.pth"]
        
        for weight_file in weight_files:
            if os.path.exists(weight_file):
                st.info(f"🔧 Loading PyTorch model: {weight_file}")
                
                # Create model architecture
                model = mobilenet_v2(weights=None)
                model.classifier[1] = nn.Linear(model.classifier[1].in_features, 10)
                
                # Load weights
                model.load_state_dict(torch.load(weight_file, map_location='cpu'))
                model.eval()
                
                # Convert to evaluation mode
                self.model = model
                st.success(f"✅ PyTorch model loaded from {weight_file}")
                return
        
        st.warning("📭 No PyTorch weight files found")
        raise FileNotFoundError("No PyTorch weight files available")
    
    def _create_demo_model(self):
        """Create a demo model if no saved models exist"""
        st.info("🎭 Creating demo model for testing...")
        
        # Create a simple model
        model = mobilenet_v2(weights='IMAGENET1K_V1')
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, 10)
        model.eval()
        
        self.model = model
        st.success("✅ Demo model created successfully")
        
        # Save it for future use
        torch.save(model.state_dict(), "demo_model_weights.pth")
        st.info("💾 Demo model saved as 'demo_model_weights.pth'")
    
    def _load_classes(self):
        """Load class labels"""
        class_files = ["classes.txt", "class_labels.txt", "labels.txt"]
        
        for class_file in class_files:
            if os.path.exists(class_file):
                try:
                    with open(class_file, 'r') as f:
                        self.classes = [line.strip() for line in f.readlines()]
                    st.success(f"✅ Classes loaded from {class_file}")
                    return
                except Exception as e:
                    st.warning(f"⚠️ Error loading {class_file}: {e}")
        
        # Create demo classes if no file exists
        self.classes = [
            "Rainbow Trout", "Clownfish", "Goldfish", "Salmon", "Tuna",
            "Bass", "Carp", "Catfish", "Pufferfish", "Angelfish"
        ]
        st.warning("📝 Using demo class labels")
    
    def predict(self, image):
        """Predict fish species from image"""
        if self.model is None:
            return {"error": "Model not available", "success": False}
        
        try:
            # Convert and preprocess image
            if isinstance(image, np.ndarray):
                image = Image.fromarray(image)
            image = image.convert('RGB')
            
            # Transformations
            transform = transforms.Compose([
                transforms.Resize((128, 128)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            
            input_tensor = transform(image).unsqueeze(0)
            
            # Handle different model types
            if isinstance(self.model, torch.jit.ScriptModule):
                # TorchScript model
                outputs = self.model(input_tensor)
            else:
                # Regular PyTorch model
                with torch.no_grad():
                    outputs = self.model(input_tensor)
            
            # Process results
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
            # Get top predictions
            top_k = min(5, len(self.classes))
            top_probs, top_indices = torch.topk(probabilities, top_k)
            
            top_predictions = [
                (self.classes[i], top_probs[0][j].item()) 
                for j, i in enumerate(top_indices[0])
            ]
            
            return {
                'predicted_class': self.classes[predicted_idx.item()],
                'confidence': confidence.item(),
                'top_predictions': top_predictions,
                'success': True
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}

def main():
    st.title("🐟 AI Fish Species Analyzer")
    st.markdown("Upload a fish image to identify its species!")
    
    # Display current files
    with st.expander("📁 Current Directory Files"):
        files = [f for f in os.listdir('.') if f.endswith(('.pt', '.pth', '.txt'))]
        if files:
            st.write("Model-related files found:")
            for file in files:
                st.write(f" - `{file}`")
        else:
            st.write("No model files found.")
    
    # Initialize classifier
    classifier = FishSpeciesClassifier()
    
    # File upload section
    st.subheader("📤 Upload Fish Image")
    uploaded_file = st.file_uploader(
        "Choose a fish image", 
        type=['jpg', 'png', 'jpeg']
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📷 Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            st.write(f"**Image size:** {image.size[0]}x{image.size[1]} pixels")
        
        with col2:
            st.subheader("🔍 Analysis")
            
            if st.button("Analyze Fish Species", type="primary", use_container_width=True):
                with st.spinner("Analyzing image..."):
                    results = classifier.predict(image)
                
                if results.get('success', False):
                    confidence = results['confidence']
                    
                    st.success(f"**Prediction:** {results['predicted_class']}")
                    st.metric("Confidence", f"{confidence*100:.1f}%")
                    
                    # Display top predictions
                    st.subheader("📊 Top Predictions")
                    for i, (species, prob) in enumerate(results['top_predictions']):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.write(f"**{i+1}. {species}**")
                        with col_b:
                            st.write(f"{prob*100:.2f}%")
                
                else:
                    st.error(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
    
    else:
        st.info("👆 Upload a fish image to analyze its species!")
        
        # Instructions
        st.subheader("💡 Getting Started:")
        st.markdown("""
        1. **Upload a fish image** using the file uploader above
        2. **Click 'Analyze Fish Species'** to get predictions
        3. **View the results** including confidence scores
        """)

if __name__ == "__main__":
    main()
