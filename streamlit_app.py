import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models

st.set_page_config(page_title="🐟 Fish Classifier", page_icon="🐟", layout="wide")
st.title("🐟 Fish Species Classifier")

# Load PyTorch model
@st.cache_resource
def load_model():
    try:
        # Create model architecture (same as your training)
        model = models.resnet50(pretrained=False)
        model.fc = torch.nn.Linear(model.fc.in_features, 483)  # 483 species
        
        # Load weights
        model.load_state_dict(torch.load('fish_model.pth', map_location='cpu'))
        model.eval()
        st.success("✅ PyTorch model loaded!")
        return model
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

model = load_model()

def predict_fish(image):
    if model is None:
        return "Model not available", 0.0
    
    # Preprocess for PyTorch
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    image_tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        predicted_class = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_class].item()
    
    species_name = f"Species_{predicted_class}"  # Replace with your class names
    return species_name, confidence

# Rest of your app...
