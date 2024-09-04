import os
import sqlite3
import subprocess
import time
import pyautogui
import pyttsx3
import webbrowser
from hugchat import hugchat
import pywhatkit as pk
import speech_recognition as sr
from helper import *
from pipes import quote
from config import ASSISTANT_NAME

# Stablishing connection with database
con = sqlite3.connect('cono.db')
cursor = con.cursor()

# function to make cono speak
def speak(text, display=True):
    text = str(text)
    if display:
        print("CONO:" + text)

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()

# funtion to open apps and websites
def open_app(transcript):

    transcript = transcript.replace(ASSISTANT_NAME, "")
    transcript = transcript.replace("open", "")
    transcript.lower()
    
    appName = transcript.strip()
    
    if appName != "":
        try:
            cursor.execute('SELECT path FROM sys_commands WHERE name IN (?)', (appName,))
            results = cursor.fetchall()
            
            if len(results) != 0:
                speak("Opening" + transcript)
                os.startfile(results[0][0])
            
            elif len(results) == 0:
                cursor.execute('SELECT url FROM web_commands WHERE name IN (?)', (appName,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening" + transcript)
                    webbrowser.open(results[0][0])
                    
                else:
                    speak("Opening" + transcript)
                    try:
                        os.system("strat" + transcript)
                    except:
                        speak("not found")
        except:
            speak("Something went wrong when trying to open")


# function to play videos on youtube
def play_yt(transcript):
    searchTerm = extract_search_term(transcript)
    speak("Playing " + searchTerm + " on youtube")
    # query = listen()
    pk.playonyt(searchTerm)

# fucntion to use whatsapp

def whatsapp(name, mobileNo, type, msg):
    if type == 'message':
        target_tab = 12
        conoMessage = "message send successfully to "+name

    elif type == 'phone call':
        target_tab = 7
        conoMessage = "calling to "+name

    elif type == 'video call':
        target_tab = 6
        conoMessage = "staring video call with "+name


    # Encode the message for URL
    encodedMessage = quote(msg)
    print(encodedMessage)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobileNo}&text={encodedMessage}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(conoMessage)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path=".conda\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    # print(response)
    speak(response)

if __name__ == "__main__":
    chatBot("Who is the president of india")