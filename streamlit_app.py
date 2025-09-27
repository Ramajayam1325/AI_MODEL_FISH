import os
import onnxruntime as ort

MODEL_PATH = os.path.join(os.path.dirname(__file__), "fish_model.onnx")

session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image

# Load ONNX model
MODEL_PATH = "fish_model.onnx"
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

# Define image size (match your training size, e.g., 224x224 for MobileNet)
IMG_SIZE = 224

# Example: load class names
CLASSES = ["class1", "class2", "class3"]  # replace with your real fish species

def preprocess(image: Image.Image):
    image = image.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(image).astype(np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))  # HWC → CHW
    arr = np.expand_dims(arr, axis=0)   # Add batch dimension
    return arr

def predict(image: Image.Image):
    arr = preprocess(image)
    inputs = {session.get_inputs()[0].name: arr}
    preds = session.run(None, inputs)[0]
    probs = np.exp(preds) / np.sum(np.exp(preds))  # softmax
    idx = np.argmax(probs)
    return CLASSES[idx], probs[0][idx]

st.title("🐟 Fish Species Classifier (ONNX)")

uploaded = st.file_uploader("Upload a fish image", type=["jpg", "jpeg", "png"])
if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    label, confidence = predict(image)
    st.success(f"Prediction: {label} ({confidence*100:.2f}%)")

