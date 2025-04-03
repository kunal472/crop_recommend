from flask import Flask, render_template, request, jsonify
import joblib  # Changed from pickle to joblib for loading model
import numpy as np  # For data processing
import google.generativeai as genai  # For AI API
import os
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__)

# 🔹 Load ML Model for Crop Prediction
MODEL_PATH = "smart-agriculture.joblib"  # Ensure this file exists
crop_model = joblib.load(MODEL_PATH)  # Load the joblib model

# 🔹 Configure AI API (Gemini for Chatbot & Image Analysis)
genai.configure(api_key="")  # Replace with your API Key
chatbot_model = genai.GenerativeModel('gemini-2.0-flash')  # Text AI for Chatbot
vision_model = genai.GenerativeModel('gemini-2.0-flash')  # Image AI for Analysis

# 🔹 Configure Upload Folder for Images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

# 🔹 Crop Prediction API (ML Model)
@app.route('/predict', methods=['POST'])
def predict_crop():
    """Predicts the best crop based on soil and climate data."""
    try:
        data = request.json
        required_fields = ['N', 'K', 'P', 'temperature', 'humidity', 'ph', 'rainfall']

        # Validate Inputs
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required parameters"}), 400

        # Convert Inputs to Model Format
        input_values = np.array([[data['N'], data['P'], data['K'], data['temperature'], data['humidity'], data['ph'], data['rainfall']]])
        predicted_crop = crop_model.predict(input_values)[0]  # Predict Crop

        return jsonify({"crop": predicted_crop})

    except Exception as e:
        return jsonify({"error": f"Error processing crop prediction: {str(e)}"}), 500

# 🔹 Chatbot API (AI-Powered)
@app.route('/chatbot-response', methods=['POST'])
def chatbot_response():
    """Handles chatbot queries with an AI agricultural expert role."""
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a valid question."}), 400

    try:
        # Assign a role to the chatbot
        prompt = f"""
        You are an AI Crop Consultant. Your job is to provide expert advice on farming, 
        crop selection, soil health, pest control, and sustainable agricultural practices.
        Answer the following question in a clear and professional manner:
        
        Question: {user_message}
        """

        response = chatbot_model.generate_content(prompt)
        bot_reply = response.text.strip() if response.text else "Sorry, I couldn't understand."

        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"Error processing request: {str(e)}"}), 500

# 🔹 Image Analysis API (AI-Powered)
@app.route('/upload-image', methods=['POST'])
def upload_image():
    """Handles image uploads for plant health analysis and disease detection."""
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Secure and Save Image
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        # Process Image using AI API
        img = Image.open(file_path)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')  # Convert to JPEG
        img_byte_arr = img_byte_arr.getvalue()

        response = vision_model.generate_content([
            "Analyze this plant image and provide plant name and any diseases present and its possible solution.",
            genai.Part.from_data(mime_type='image/jpeg', data=img_byte_arr)
        ])
        
        diagnosis = response.text.strip() if response.text else "No diagnosis available."

        return jsonify({"response": diagnosis, "image_url": f"/{file_path}"})

    except Exception as e:
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
