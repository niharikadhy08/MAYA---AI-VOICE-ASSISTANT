import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import feedparser
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content


def processCommand(c):
    print(f"\nYou said: {c}\n")

    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c.lower():
        speak("Fetching top news from Google...")
        news_feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
        if news_feed.entries:
            for entry in news_feed.entries[:5]:
                speak(entry.title)
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Maya....")
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening for wake word...")
            try:
                audio = r.listen(source, timeout=4, phrase_time_limit=2)
                word = r.recognize_google(audio)
                print(f"You said (wake word): {word}")

                if "maya" in word.lower():
                    speak("Ya")
                    print("Maya Active. Listening for command...")
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.3)
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        processCommand(command)

            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
