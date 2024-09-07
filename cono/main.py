import os
import eel
from engine.features import *
from engine.command import *
from engine.auth.face_detect import faceDetect


def start():
    eel.init("www")
    playAssistantSound()
    speak("Ready for face authentication, booting camera")
    name = faceDetect()
    
    if name.lower() in ['swastik', 'nihal', 'varun', 'saksham', 'harshita', 'nitya']:
        speak("Face Verified SuccessFully, Welcome " + name)
        os.system('start msedge.exe --app="http://localhost:8000/index.html"')
        eel.start('index.html', mode=None, host='localhost', block=True)
    else:
        speak("Face Authentication Failed")
        os._exit(0)