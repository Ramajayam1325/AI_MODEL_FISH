import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models

st.set_page_config(page_title="🐟 Fish Classifier", page_icon="🐟", layout="wide")
st.title("🐟 Fish Species Classifier")

# Load PyTorch model with weights_only=False
@st.cache_resource
def load_model():
    try:
        # Create model architecture
        model = models.resnet50(pretrained=False)
        model.fc = torch.nn.Linear(model.fc.in_features, 483)  # 483 species
        
        # Load weights with weights_only=False
        model.load_state_dict(torch.load('fish_model.pth', map_location='cpu', weights_only=False))
        model.eval()
        st.success("✅ PyTorch model loaded!")
        return model
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

model = load_model()

# Rest of your code...
else:
    st.error("❌ Model file 'fish_model.pth' not found")
    model = None

# Your class names (use first few for testing)
CLASS_NAMES = ['Istiophorus_platypterus', 'acanthaluteres_brownii', 'acanthaluteres_spilomelanurus', 
               'acanthaluteres_vittiger', 'acanthistius_cinctus']  # Add more as needed

def predict_fish_species(image):
    if model is None:
        return "Model not available", 0.0
    
    # Preprocess image
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    predictions = model.predict(img_array, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class])
    
    species_name = CLASS_NAMES[predicted_class % len(CLASS_NAMES)]
    
    return species_name, confidence

# Main app
uploaded_file = st.file_uploader("📤 Upload Fish Image", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, use_container_width=True)
        st.write(f"**Size:** {image.size[0]} × {image.size[1]} pixels")
    
    with col2:
        if st.button("🔬 Classify Species", type="primary"):
            with st.spinner("Classifying..."):
                species, confidence = predict_fish_species(image)
                st.success(f"**Species:** {species}")
                st.success(f"**Confidence:** {confidence:.2%}")

st.markdown("---")
st.write("Using your trained fish species model")
