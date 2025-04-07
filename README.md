

# 🌾 Crop Recommend

A smart crop recommendation system powered by machine learning and Google Generative AI. This tool helps farmers and agricultural professionals determine the best crops to plant based on various input parameters.

## 🚀 Live Demo

> 🔗https://crop-recommend-wb46.onrender.com

---

## 📂 Project Structure

```
crop_recommend/
├── app.py                 # Main Flask application
├── model.joblib           # Trained crop recommendation model
├── templates/
│   └── index.html         # Frontend interface
├── static/                # Static assets (if any)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 🧠 Features

- 📊 ML-based crop prediction
- 🌐 Google Generative AI integration
- 🔄 Real-time streaming responses with Flask
- 🖥️ Simple and user-friendly web interface

---

## 🔧 Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🛠️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/kunal472/crop_recommend.git
cd crop_recommend
```

2. Create a `.env` file in the root directory and add your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

3. Start the Flask server:

```bash
python app.py
```

4. Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 🧪 Example Inputs

Provide inputs like:
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH level
- Rainfall

Get real-time crop recommendations based on your environment.

---

## 📦 Dependencies

- Flask
- NumPy
- Joblib
- Python-dotenv
- Google Generative AI

---

## 🙌 Contributing

Feel free to fork the repo and submit pull requests. Contributions are welcome!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## ✨ Author

**Kunal Patil**  
🔗 [GitHub](https://github.com/kunal472)

---

Let me know if you want badges, images, or setup instructions for Docker, Streamlit, or cloud hosting platforms!
