from pipes import quote
import re
import struct
import subprocess
import time
from playsound import playsound
import eel
import os
import sqlite3 
import webbrowser
import pyaudio
import pyautogui
import pywhatkit as pk
from hugchat import hugchat
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words
import pvporcupine

con = sqlite3.connect('cono.db')
cursor = con.cursor()

@eel.expose
# Playing assistant sound
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()
    
    app_name = query.strip()
    
    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_commands WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_commands WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except Exception as e:
            print(e)
            speak("something went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    pk.playonyt(search_term)
    

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
    
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


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

# find contacts
def findContact(query):
    contacts = {"swastik": "7067115104", "nihal": "7050946916", "nitya": "8840420294", "harshita": "8210049063", "nishant": "7000825113"}
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)
    print(query)
    try:
        mobile_number_str = contacts[query]
        
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str
        
        print(mobile_number_str)

        return query, mobile_number_str
    except:
        speak('not exist in contacts')
        return 0, 0


# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path=".venv\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response