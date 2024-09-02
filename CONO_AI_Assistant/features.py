import os
import pyttsx3
import requests
from datetime import datetime
import speech_recognition as sr
from config import ASSISTANT_NAME

# function to make her speak
def speak(text, display=True):
    if display:
        print("CONO:" + text)

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()

def listen():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            transcript = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {transcript}")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?", display=True)
        except sr.RequestError:
            speak("There seems to be a network issue. Please try again later.", display=True)
    return transcript

def listen_and_understand():
    
    transcript = listen()
    
    if "open" in transcript:
        open_app(transcript)
    else:
        print("not run")
    
    return transcript

def open_app(transcript):

    transcript = transcript.replace(ASSISTANT_NAME, "")
    transcript = transcript.replace("open", "")
    
    if transcript != "":
        speak("opening" + transcript)
        os.system('start' + transcript)
    else:
        print("not found")