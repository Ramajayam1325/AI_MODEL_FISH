import streamlit as st
import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2
from PIL import Image

# ----------------- Load Classes -----------------
with open("classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# ----------------- Load Model ------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = mobilenet_v2(weights=None)  # No pretrained weights
num_ftrs = model.classifier[1].in_features
model.classifier[1] = torch.nn.Linear(num_ftrs, len(classes))
model.load_state_dict(torch.load("best_fish_model.pth", map_location=device))
model.eval()
model.to(device)

# ----------------- Transform -------------------
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

# ----------------- Streamlit UI ----------------
st.title("Fish Species Classifier")
st.write("Upload an image of a fish to predict its species.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    x = transform(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(x)
        _, pred = torch.max(outputs, 1)
    
    st.success(f"Predicted Class: {classes[pred.item()]}")
