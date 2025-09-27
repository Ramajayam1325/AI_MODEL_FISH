import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from datetime import datetime

# Page config
st.set_page_config(page_title="🐟 Fish Species Classifier", page_icon="🐟", layout="wide")
st.title("🐟 Fish Species Classifier (4000 Species)")

# Load your trained model
@st.cache_resource
def load_model():
    try:
        # Update this path to your actual model file
        model = tf.keras.models.load_model('fish_species_model.h5')
        return model
    except:
        st.error("Model file not found. Please check the path.")
        return None

model = load_model()

# Preprocess image for your model
def preprocess_image(image):
    image = image.resize((224, 224))  # Adjust to your model's input size
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)

# Class names (update with your 4000 species)
class_names = ["Species_1", "Species_2", "Species_3"]  # Replace with your actual class names

def predict_fish_species(image):
    if model is None:
        return "Model not loaded"
    
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    
    return class_names[predicted_class], confidence

# Main app
uploaded_file = st.file_uploader("📤 Upload Fish Image", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, use_container_width=True)
        st.write(f"**Image:** {uploaded_file.name}")
        st.write(f"**Size:** {image.size[0]} × {image.size[1]} pixels")
    
    with col2:
        if st.button("🔬 Classify Fish Species", type="primary"):
            with st.spinner("Classifying with your trained model..."):
                species, confidence = predict_fish_species(image)
                
                st.success(f"**Predicted Species:** {species}")
                st.success(f"**Confidence:** {confidence:.2%}")
                st.success(f"**Model:** 4000 Species Classifier")

else:
    st.info("👆 Upload a fish image for species classification")

st.markdown("---")
st.write("Trained on 4000 Fish Species · Custom AI Model")
