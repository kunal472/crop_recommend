from flask import Response, request, stream_with_context, jsonify,Flask, render_template
import time
import joblib  # Changed from pickle to joblib for loading model
import numpy as np  # For data processing
import google.generativeai as genai  # For AI API
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
# 🔹 Load ML Model for Crop Prediction
MODEL_PATH = "smart-agriculture.joblib"  # Ensure this file exists
crop_model = joblib.load(MODEL_PATH)  # Load the joblib model

# 🔹 Configure AI API (Gemini for Chatbot & Image Analysis)
genai.configure(api_key=os.getenv("GENAI")) # Replace with your API Key
chatbot_model = genai.GenerativeModel('gemini-2.0-flash')  # Text AI for Chatbot


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

@app.route('/chatbot-response', methods=['POST'])
def chatbot_response():
    """Streams chatbot response like it's typing."""
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return Response("Please enter a valid question.", status=400)

    try:
        # Assign a role to the chatbot
        prompt = f"""
        You are an AI Crop Consultant. Your job is to provide expert advice on farming, 
        crop selection, soil health, pest control, and sustainable agricultural practices.
        Answer the following question in a clear and professional manner:
        
        Question: {user_message}
        """

        def generate():
            response = chatbot_model.generate_content(prompt)
            bot_reply = response.text.strip() if response.text else "Sorry, I couldn't understand."

            # You can stream word-by-word instead of character-by-character
            for word in bot_reply.split():
                yield word + " "
                time.sleep(0.03)  # simulate typing delay

        return Response(stream_with_context(generate()), content_type='text/plain')

    except Exception as e:
        return Response(f"Error processing request: {str(e)}", status=500)


if __name__ == '__main__':
    app.run(debug=False)

