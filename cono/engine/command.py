from datetime import datetime
import eel
import time
import pyttsx3
import speech_recognition as sr
from engine.features import *

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
        
    
    try:
        
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query or "send a message" in query:
            from engine.features import findContact, whatsapp
            type = ""
            msg = None
            contactName, mobileNo = findContact(query)
            if contactName != 0:
                if "send message" in query or "send a message" in query:
                    type = "message"
                    speak("what message you want to send")
                    msg = takecommand()
                elif "phone call" in query:
                    type = "phone call"
                else:
                    type = "video call"
                whatsapp(contactName, mobileNo, type, msg)
        
        elif "who are you" in query or 'hu r u' in query or "tell me about yourself" in query:
            speak("I'm an artificial intelligence model known as CONO. CONO stands for 'Command On New Operator.'")

        elif "what is your name" in query:
            speak("My name is CONO, your personal Ai assistant")

        elif "today's date" in query or "current date" in query:
            speak("Today's date is: " + str(datetime.today().strftime("%B %d, %Y")))

        elif "day is today" in query or "current day" in query:
            speak("Today's Day is: " + str(datetime.now().strftime('%A')))

        elif "current time" in query or "time right now" in query:
            speak("Current time is: " + str(datetime.now().strftime("%H:%M:%S")))

        elif "stop" in query or "exit" in query:
            os._exit(0)

        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print(e)

    eel.ShowHood()