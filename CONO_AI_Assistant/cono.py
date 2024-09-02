import pyttsx3
import requests
from datetime import datetime
import speech_recognition as sr
from face_detect import faceDetect
from features import *
# Set verification state and other variables
verification_state = 'face'
max_attempts = 3
attempts = 0

def start_recognition():
    global verification_state

    # Face Lock
    while verification_state != 'done':
        if verification_state == 'face':
            try:
                userInfo = faceDetect()
                if userInfo.lower() in ['swastik', 'nihal', 'varun', 'saksham', 'harshita', 'nitya']:
                    speak(f"\nFace verified successfully, Hello {userInfo}.")
                    verification_state = 'done'
                    cono_will_wish()
                else:
                    speak("Face not recognized. Please try again.")
                    verification_state = 'face'
            except Exception as e:
                speak(f"An error occurred during face recognition: {str(e)}")
                break

def cono_will_wish():
    hour = datetime.now().hour
    if hour > 4 and hour < 12:
        greeting = "Good Morning."
    elif 12 <= hour < 18:
        greeting = "Good Afternoon."
    else:
        greeting = "Good Evening."
    speak(greeting)
    speak("I'm CONO, your AI assistant. How can I assist you today?")
    transcript = listen_and_understand()
    print(transcript)

def fetch_openai_response(prompt):
    try:
        response = requests.post('http://localhost:3000/api/openai', json={"prompt": prompt}, timeout=5)
        data = response.json()
        return data['choices'][0]['text'].strip()
    except requests.exceptions.RequestException:
        return "I'm having trouble connecting to the server right now."

def initiate_cono():
    # Initial prompt to start the interaction
    speak("  Hey, I'm CONO... i'm booting your devices camera please look into it for authentication...")
    start_recognition()

if __name__ == "__main__":
    initiate_cono()