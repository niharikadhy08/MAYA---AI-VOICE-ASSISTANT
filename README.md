# MAYA – AI Voice Assistant

MAYA is a Python-based AI voice assistant that listens to voice commands, responds intelligently using an LLM, speaks replies aloud, plays music, opens websites, and fetches the latest news — all running locally from the terminal with a Streamlit UI.

---

## Features
- Voice Input using SpeechRecognition
- AI Responses powered by Groq (LLaMA models)
- Text-to-Speech Output using gTTS + pygame
- Open Websites (Google, YouTube, etc.)
- Play Music from a predefined music library
- Fetch Top 5 News Headlines (Google News RSS)
- Stop Speaking Command (“stop”, “shut up”, etc.)
- Chat History Display in Streamlit UI

---

## Project Structure
maya-ai-voice-assistant/
├── app.py              # Main Streamlit app
├── voice.py            # Voice input & output logic
├── ai_engine.py        # AI processing (Groq API)
├── musicLibrary.py     # Music name → URL mapping
├── main.py             # (Optional) terminal-only voice loop
├── client.py           # API test file
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Ignored files (env, temp files, etc.)
└── .env                # API keys (NOT pushed to GitHub)

---

## Tech Stack :
- Python
- Streamlit
- SpeechRecognition
- gTTS
- pygame
- Groq API (LLaMA models)
- feedparser

---

## Prerequisites 
Before running the project, make sure you have:
    Python 3.9+
    A working microphone
    A Groq API key

---

## How to Run the Project 
Run the Streamlit voice assistant - streamlit run app.py
A browser window will open automatically
Click 🎤 Talk to Maya
Speak commands like:
    “Open Google”
    “Play Counting Stars”
    “Tell me the news”
    “Stop speaking”

