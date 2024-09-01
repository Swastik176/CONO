import pyttsx3
import requests
from datetime import datetime
import speech_recognition as sr
from face_detect import faceDetect

# Set verification state and other variables
verification_state = 'face'
max_attempts = 3
attempts = 0

# function to make her speak
def speak(text, display=True):
    if display:
        print("CONO: " + text)

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()


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
    speak("Do you wanna listen music, watch youtube or send a message to your friend....")
    listen()

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