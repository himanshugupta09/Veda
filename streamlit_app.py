import streamlit as st
import numpy as np
from PIL import Image
import imageio
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os
import google.generativeai as genai
import kerberos
import os
os.environ["KRB5_CONFIG"] = "./config/krb5.conf"
# Get realm from environment variable (if available)
realm = os.environ.get('KERBEROS_REALM')

# If not set, use a default value (replace with a likely default or leave empty)
if not realm:
  realm = 'dev'  # Replace with your expected default realm

username = 'vedji'
kerberos.auth_kerberos_init(f'{username}@{realm}')

# Set Google API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBmFQrGtguWOKEkJlCpeRQFj0LhzE9VnX4"
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    gemi = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Failed to configure Google Generative AI: {e}")
    gemi = None

# Load Background Image
try:
    background_image = Image.open("bgm.jpg")
    st.image(background_image, use_column_width=True)
except FileNotFoundError:
    st.warning("Background image not found. Proceeding without it.")

# Load Trained Model
try:
    model = load_model("plant_model5.h5", compile=False)
except Exception as e:
    st.error(f"Failed to load the model: {e}")
    model = None

# Plant Names
plant_names = [
    "Amaranthus Green", "Amaranthus Red", "Asthma Plant", "Avaram", "Balloon vine",
    "Bellyache bush (Green)", "Benghal dayflower", "Betel Leaves", "Big Caltrops",
    "Black Night Shade", "Black-Honey Shrub", "Bristly Wild Grape", "Butterfly Pea",
    "Cape Gooseberry", "Celery", "Chinese Spinach", "Common Wireweed", "Coriander Leaves",
    "Country Mallow", "Crown flower", "Curry Leaf", "Dwarf Copperleaf (Green)",
    "Dwarf copperleaf (Red)", "False Amarnath", "Fenugreek Leaves", "Giant Pigweed",
    "Gongura", "Green Chireta", "Holy Basil", "Indian CopperLeaf", "Indian Jujube",
    "Indian Sarsaparilla", "Indian Stinging Nettle", "Indian Thornapple", "Indian pennywort",
    "Indian wormwood", "Ivy Gourd", "Kokilaksha", "Lagos Spinach", "Lambs Quarters",
    "Land Caltrops (Bindii)", "Lettuce Tree", "Madagascar Periwinkle", "Madras Pea Pumpkin",
    "Malabar Catmint", "Malabar Spinach (Green)", "Mexican Mint", "Mexican Prickly Poppy",
    "Mint Leaves", "Mountain Knotgrass", "Mustard", "Nalta Jute", "Night blooming Cereus",
    "Palak", "Panicled Foldwing", "Prickly Chaff Flower", "Punarnava", 
    "Purple Fruited Pea Eggplant", "Purple Tephrosia", "Rosary Pea", "Shaggy button weed",
    "Siru Keerai", "Small Water Clover", "Spiderwisp", "Square Stalked Vine",
    "Stinking Passionflower", "Sweet Basil", "Sweet flag", "Tinnevelly Senna",
    "Trellis Vine", "Velvet bean", "Water Spinach", "coatbuttons", "heart-leaved moonseed"
]

# Function to fetch response from Generative AI
def get_response(query):
    if gemi is None:
        return "Generative AI is not configured."
    try:
        response = gemi.generate_content(query)
        return response.text
    except Exception as e:
        return f"Failed to fetch response: {e}"

@st.cache_data(persist=True)
def predict_plant(image_path):
    try:
        # Load and preprocess image
        img = Image.open(image_path)
        img_resized = img.resize((224, 224))
        img_array = img_to_array(img_resized) / 255.0
        img_processed = img_array.reshape((1, 224, 224, 3))
        
        if model is None:
            return {"name": "N/A", "info": "Model not loaded.", "indian_name": "N/A"}
        
        # Predict class
        prediction = model.predict(img_processed)
        predicted_class = np.argmax(prediction)
        predicted_plant_name = plant_names[predicted_class]

        # Fetch plant information
        plant_info = get_response(f"Some detail and ayurvedic use case for {predicted_plant_name}")
        indian_name = get_response(f"Indian name of {predicted_plant_name}")

        return {"name": predicted_plant_name, "info": plant_info, "indian_name": indian_name}
    except Exception as e:
        return {"name": "N/A", "info": f"Error occurred: {e}", "indian_name": "N/A"}

# Streamlit App UI
st.title("Plant Identification App")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    with st.spinner("Predicting..."):
        prediction_details = predict_plant(uploaded_file)
    st.write(f"**Predicted Plant:** {prediction_details['name']}")
    st.write(f"**Indian Name:** {prediction_details['indian_name']}")
    st.write(f"**Details:** {prediction_details['info']}")
