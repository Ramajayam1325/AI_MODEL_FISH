import streamlit as st
from PIL import Image
import torchvision.transforms as transforms
import torch

# ----------------- Load class names -----------------
with open("classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# ----------------- Load TorchScript model -----------------
device = "cpu"
model = torch.jit.load("best_fish_model_ts.pt", map_location=device)
model.eval()

# ----------------- Image transform -----------------
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ----------------- Streamlit UI -----------------
st.title("🐟 Fish Species Classifier")
st.write("Upload an image of a fish and I’ll predict its species!")

uploaded_file = st.file_uploader("Choose a fish image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess
    x = transform(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(x)
        _, pred = torch.max(outputs, 1)

    st.success(f"Predicted Class: **{classes[pred.item()]}**")
