import streamlit as st
import numpy as np
from PIL import Image
import imageio
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import threading
import time
import base64
from PIL import Image
import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyBmFQrGtguWOKEkJlCpeRQFj0LhzE9VnX4"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
gemi = genai.GenerativeModel('gemini-pro')



def get_response(query):
    response = gemi.generate_content(query)
    return response.text


# Read the background image
background_image = Image.open("F:\IT_IV_pro\Code\\bgm.jpg")

# Display the image using st.image
st.image(background_image)

model = load_model("F:\IT_IV_pro\Code\plant_model5.h5",compile=False)
plant_names = [
    "Amaranthus Green",
    "Amaranthus Red",
    "Asthma Plant",
    "Avaram",
    "Balloon vine",
    "Bellyache bush (Green)",
    "Benghal dayflower",
    "Betel Leaves",
    "Big Caltrops",
    "Black Night Shade",
    "Black-Honey Shrub",
    "Bristly Wild Grape",
    "Butterfly Pea",
    "Cape Gooseberry",
    "Celery",
    "Chinese Spinach",
    "Common Wireweed",
    "Coriander Leaves",
    "Country Mallow",
    "Crown flower",
    "Curry Leaf",
    "Dwarf Copperleaf (Green)",
    "Dwarf copperleaf (Red)",
    "False Amarnath",
    "Fenugreek Leaves",
    "Giant Pigweed",
    "Gongura",
    "Green Chireta",
    "Holy Basil",
    "Indian CopperLeaf",
    "Indian Jujube",
    "Indian Sarsaparilla",
    "Indian Stinging Nettle",
    "Indian Thornapple",
    "Indian pennywort",
    "Indian wormwood",
    "Ivy Gourd",
    "Kokilaksha",
    "Lagos Spinach",
    "Lambs Quarters",
    "Land Caltrops (Bindii)",
    "Lettuce Tree",
    "Madagascar Periwinkle",
    "Madras Pea Pumpkin",
    "Malabar Catmint",
    "Malabar Spinach (Green)",
    "Mexican Mint",
    "Mexican Prickly Poppy",
    "Mint Leaves",
    "Mountain Knotgrass",
    "Mustard",
    "Nalta Jute",
    "Night blooming Cereus",
    "Palak",
    "Panicled Foldwing",
    "Prickly Chaff Flower",
    "Punarnava",
    "Purple Fruited Pea Eggplant",
    "Purple Tephrosia",
    "Rosary Pea",
    "Shaggy button weed",
    "Siru Keerai",
    "Small Water Clover",
    "Spiderwisp",
    "Square Stalked Vine",
    "Stinking Passionflower",
    "Sweet Basil",
    "Sweet flag",
    "Tinnevelly Senna",
    "Trellis Vine",
    "Velvet bean",
    "Water Spinach",
    "coatbuttons",
    "heart-leaved moonseed",
]
# Function to read and display GIF frames
def animate_background():
    #background_image = Image.open("F:\IT_IV_pro\Code\\background.gif")

    # Continuously display the image
    
    #Read the GIF animation
    reader = imageio.get_reader("F:\IT_IV_pro\Code\\new.gif")

    # Get duration metadata
    duration = reader.get_meta_data()["duration"]

    # Check if single frame
    if isinstance(duration, int) or duration == 1:
        # Single frame GIF, display once
        frame = reader.get_next_data()
        frame_image = Image.fromarray(frame)
        st.image(frame_image, use_column_width=True)
        return

    # Multi-frame GIF, loop through frames
    for i, frame in enumerate(reader):
        # Convert frame to PIL Image format
        frame_image = Image.fromarray(frame)
        st.image(frame_image, use_column_width=True)

        # Adjust delay between frames
        time.sleep(reader.get_meta_data()["duration"][i] / 1000)

#animate_background()

# Start background animation in a separate thread
# thread = threading.Thread(target=animate_background)
# thread.daemon = True
# thread.start()

@st.cache_data(persist=True)
def predict_plant(image_path):
    # Load image
    img = Image.open(image_path)
    img_resized = img.resize((224, 224))
    img_array = img_to_array(img_resized)
    img_normalized = img_array / 255.0
    img_processed = img_normalized.reshape((224, 224, 3))

    prediction = model.predict(np.array([img_processed]))

    # Get predicted class index
    predicted_class = np.argmax(prediction)

    predicted_plant_name = plant_names[predicted_class]

    # Fetch plant information
    plant_info = get_response('Some detail and ayurvedic use case for {plant_name}'.format(plant_name=predicted_plant_name))
    indian_name = get_response('Indian name of {plant_name}'.format(plant_name=predicted_plant_name))

    # Return prediction details
    return {"name": predicted_plant_name, "info": plant_info, "indian_name": indian_name}


st.title("Plant Identification App")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if(st.button("Show Image")):
    st.image(uploaded_file,width=4,use_column_width=True)

if uploaded_file is not None:
    # Show loading GIF while prediction is ongoing
    with st.spinner("Predicting..."):
        prediction_details = predict_plant(uploaded_file)

    # Display prediction details
    st.write(f"Predicted plant: **{prediction_details['name']}**")
    st.write(f"Indian name: **{prediction_details['indian_name']}**")
    st.write(prediction_details["info"])

    # Save uploaded image
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
