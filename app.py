from flask import Flask, jsonify, request, render_template, session
import openai
import speech_recognition as sr
import pyttsx3
import json
from deepface import DeepFace
import cv2
import threading
import base64
import numpy as np
import time
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
db = SQLAlchemy(app)

# Set your OpenAI API key
openai.api_key = "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"

# Initialize recognizer, text-to-speech engine, and other variables
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
conversation_history = []

# Define UserQuery model
class UserQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    emotion = db.Column(db.String(50), nullable=False)

db.create_all()

# Function to listen to user input
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Sorry, I can't connect to the service."

# Detect emotion from image data when responding
def detect_emotion(base64_image_data):
    try:
        image_data = base64.b64decode(base64_image_data.split(",")[1])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
        if isinstance(result, list) and len(result) > 0:
            result = result[0]
        dominant_emotion = result.get("dominant_emotion", "neutral")
        print(f"Detected Emotion: {dominant_emotion}")
        return dominant_emotion
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return "neutral"

# Generate a response based on user input and detected emotion
def generate_response(user_input, detected_emotion):
    conversation_history.append({"role": "user", "content": user_input})
    history_subset = conversation_history[-10:]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a therapist named Lulli Loda. The user currently seems {detected_emotion}. Personalize the response and suggest exercises if stress is detected."}
        ] + history_subset
    )
    bot_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": bot_response})
    
    # Save the conversation to the database
    new_entry = UserQuery(question=user_input, response=bot_response, emotion=detected_emotion)
    db.session.add(new_entry)
    db.session.commit()
    
    return bot_response

# Speak function to vocalize chatbot responses
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Save conversation history to a JSON file
def save_history():
    with open("conversation_history.json", "w") as file:
        json.dump(conversation_history, file)

# Flask route for rendering the main HTML page
@app.route("/")
def home():
    return render_template("index.html")

# Flask route for chatbot responses
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    
    # Get user name and age if not set
    if "name" not in session or "age" not in session:
        session["name"] = data.get("name", "User")
        session["age"] = data.get("age", "unknown")
    
    # Get emotion only at response time
    detected_emotion = detect_emotion(data.get("image_data"))
    bot_response = generate_response(user_input, detected_emotion)
    
    return jsonify({"response": bot_response})

# Flask route for analyzing emotion from an uploaded image
@app.route("/analyze-emotion", methods=["POST"])
def analyze_emotion():
    data = request.json
    image_data = data.get("image_data")
    
    if not image_data:
        return jsonify({"error": "No image data provided"}), 400
    
    try:
        emotion = detect_emotion(image_data)
        return jsonify({"emotion": emotion})
    except Exception as e:
        print(f"Error in emotion analysis: {e}")
        return jsonify({"error": "Emotion analysis failed"}), 500

# Flask route to start the conversation and request user info
@app.route("/start", methods=["POST"])
def start():
    data = request.json
    session["name"] = data.get("name", "User")
    session["age"] = data.get("age", "unknown")
    return jsonify({"message": f"Hello, {session['name']}! How can I assist you today?"})

# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)
