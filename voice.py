import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time
import uuid

recognizer = sr.Recognizer()

pygame.mixer.init()  

is_speaking = False


def listen():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            return recognizer.recognize_google(audio)
    except:
        return ""


def speak(text: str):
    global is_speaking
    if not text:
        return

    is_speaking = True
    filename = f"temp_{uuid.uuid4().hex}.mp3"

    try:
        tts = gTTS(text)
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if not is_speaking:
                pygame.mixer.music.stop()
                break
            time.sleep(0.1)

    finally:
        is_speaking = False
        try:
            pygame.mixer.music.unload()  
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass


def stop_speaking():
    global is_speaking
    is_speaking = False
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()  
    except:
        pass
