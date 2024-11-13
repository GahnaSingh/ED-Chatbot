# Real-Time Emotion-Based Voice Chatbot

## Project Overview

The Real-Time Emotion-Based Voice Chatbot is an interactive, adaptive chatbot application that combines voice recognition, text-to-speech, and real-time facial emotion detection. By analyzing the user’s emotions and voice inputs, the chatbot provides tailored responses, creating an engaging and personalized interaction experience.

## Features

- **Emotion Detection**: Real-time analysis of user emotions from webcam input.
- **Voice Interaction**: Captures voice queries and responds using text-to-speech.
- **Contextual Responses**: Adapts responses based on detected emotions and recent conversation history.
- **Persistent Conversation History**: Stores interactions in a SQLite database for future reference.

## Tech Stack

- **Backend**: Flask, OpenAI API, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Emotion Detection**: DeepFace, OpenCV
- **Voice Interaction**: SpeechRecognition, pyttsx3

## Project Structure

```plaintext
EM-chatbot/
├── app.py                     # Main Flask application
├── db_setup.py                # SQLAlchemy setup
├── models.py                  # Database model for storing conversations
├── static/
│   └── script.js              # JavaScript for frontend interaction
├── templates/
│   └── index.html             # Frontend HTML
├── conversation_history.json  # Temporary file for storing conversation history
└── requirements.txt           # Dependencies
