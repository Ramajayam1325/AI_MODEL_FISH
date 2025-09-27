import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

st.set_page_config(page_title="🐟 Fish Classifier", page_icon="🐟", layout="wide")
st.title("🐟 Fish Species Classifier (483 Species)")
# Save your class names in a text file 'class_names.txt'
with open('class_names.txt', 'r') as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model('fish_species_model.h5')
        st.success("✅ Model loaded successfully! (483 species)")
        return model
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

model = load_model()

def predict_fish_species(image):
    if model is None:
        return "Model not loaded", 0.0
    
    # Preprocess image - adjust size to match your model's training
    image = image.resize((224, 224))  # Common size, adjust if needed
    img_array = np.array(image) / 255.0
    
    # Convert grayscale to RGB if needed
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    predictions = model.predict(img_array, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class])
    
    # Get species name
    species_name = CLASS_NAMES[predicted_class]
    
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
            with st.spinner("Analyzing with AI model..."):
                species, confidence = predict_fish_species(image)
                
                # Display results
                st.success(f"**Predicted Species:** {species.replace('_', ' ').title()}")
                st.success(f"**Confidence:** {confidence:.2%}")
                st.success(f"**Dataset:** 4396 images, 483 species")

else:
    st.info("👆 Upload a fish image for species classification")

st.markdown("---")
st.write("Trained on 4396 fish images across 483 species")


