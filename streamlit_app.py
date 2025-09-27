import streamlit as st
from PIL import Image
import torch
import numpy as np
import os

# ----------------- Load class names -----------------
classes_path = os.path.join(os.path.dirname(__file__), "classes.txt")
with open(classes_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# ----------------- Load TorchScript model -----------------
model_path = os.path.join(os.path.dirname(__file__), "best_fish_model_ts.pt")
device = "cpu"
model = torch.jit.load(model_path, map_location=device)
model.eval()

# ----------------- Image preprocessing -----------------
IMG_SIZE = 128  # your training size
def preprocess(image: Image.Image):
    image = image.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(image).astype(np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))  # HWC -> CHW
    arr = np.expand_dims(arr, axis=0)   # Add batch dim
    return torch.tensor(arr)

# ----------------- Streamlit UI -----------------
st.title("🐟 Fish Species Classifier")
uploaded_file = st.file_uploader("Upload a fish image", type=["jpg","jpeg","png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    x = preprocess(img)
    with torch.no_grad():
        outputs = model(x)
        pred_idx = torch.argmax(outputs, dim=1).item()
    
    st.success(f"Predicted Species: **{classes[pred_idx]}**")
