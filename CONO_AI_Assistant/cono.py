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

# starts face recognition and detects hot word
def start_recognition():
    global verification_state

    # Face Lock
    while verification_state != 'done':
        if verification_state == 'face':
            try:
                userInfo = faceDetect()
                if userInfo.lower() in ['swastik', 'nihal', 'varun', 'saksham', 'harshita', 'nitya']:
                    speak(f"Face verified successfully, Hello {userInfo}.")
                    verification_state = 'done'
                    cono_will_wish()
                else:
                    speak("Face not recognized. Please try again.")
                    verification_state = 'face'
            except Exception as e:
                speak(f"An error occurred during face recognition: {str(e)}")
                break
    else:
        # Initialize the recognizer
        recognizer = sr.Recognizer()
        hotword = None
        with sr.Microphone() as source:
            print("Waiting for hot word...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            try:
                hotword = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {hotword}")
                if "oh no" in hotword or "cono" in hotword or "kaun ho" in hotword:
                    print(f"Recognized: {hotword}")
                    print('Activated')
                    speak("Yes")
                    listen_and_understand()
            except sr.UnknownValueError:
                # speak("Sorry, I didn't catch that. Could you please repeat?", display=True)
                print("Not understood")
                start_recognition()
            except sr.RequestError:
                speak("There seems to be a network issue. Please try again later.", display=True)
            
# fucntion to listen and understand users query
def listen_and_understand():
    try:
        transcript = listen()
        if "open" in transcript:
            open_app(transcript)

        elif "on youtube" in transcript:
            play_yt(transcript)

        elif "send message" in transcript or "phone call" in transcript or "video call" in transcript:
            from helper import findContact
            type = ""
            msg = None
            contactName, mobileNo = findContact(transcript)
            if contactName != 0:
                if "send message" in transcript:
                    type = "message"
                    speak("what message you want to send")
                    msg = listen()
                elif "phone call" in transcript:
                    type = "phone call"
                else:
                    type = "video call"
                whatsapp(contactName, mobileNo, type, msg)

        elif "who are you" in transcript or 'hu r u' in transcript:
            speak("I'm an artificial intelligence model known as CONO. CONO stands for 'Command On New Operator.'")

        elif "what is your name" in transcript:
            speak("My name is CONO, your personal Ai assistant")

        elif "today's date" in transcript or "current date" in transcript:
            speak("Today's date is: " + str(datetime.today().strftime("%B %d, %Y")))

        elif "day is today" in transcript or "current day" in transcript:
            speak("Today's Day is: " + str(datetime.now().strftime('%A')))

        elif "current time" in transcript or "time right now" in transcript:
            speak("Current time is: " + str(datetime.now().strftime("%H:%M:%S")))

        elif "stop" in transcript or "exit" in transcript:
            os._exit(0)

        else:
            chatBot(transcript)

    except  Exception as e:
        print("Error Occurred, while listening")
        print(e)

    finally:
        start_recognition()

# helper function for listen_and_understand(), helps to listen
def listen():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    transcript = None
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            transcript = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {transcript}")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?", display=True)
            listen()
        except sr.RequestError:
            speak("There seems to be a network issue. Please try again later.", display=True)
    return transcript

# function to wish 
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
    listen_and_understand()

# initializer
def initiate_cono():
    # Initial prompt to start the interaction
    speak("Hey, I'm CONO... i'm booting your devices camera please look into it for authentication...")
    start_recognition()

if __name__ == "__main__":
    initiate_cono()