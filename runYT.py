import pywhatkit as pk
from datetime import datetime as dt
from cono import speak


# while True:
#     choice = int(input("\nWhat do you want to do?\n1) Search for a Song\n2) Search a Query\n3) Send WhatsApp Message\n4) Exit\nEnter corresponding number: "))

#     match choice:
#         case 1:
#             song = input("Enter the song name: ")
#             pk.playonyt(song + " song")
#         case 2:
#             query = input("Enter your query: ")
#             pk.playonyt(query)
#         case 3:
#             name = input("Enter the name of the contact: ").lower()
#             if name in contacts:
#                 msg = input("Enter your message: ")
#                 cur_time = dt.now()

#                 # Handling the case if current time is near 59 minutes
#                 hour, minute = cur_time.hour, cur_time.minute + 1
#                 if minute >= 60:
#                     minute -= 60
#                     hour += 1
#                     if hour >= 24:
#                         hour = 0  # Roll back to 0 if hour goes past 23

#                 try:
#                     pk.sendwhatmsg(f"+91{contacts[name]}", msg, hour, minute, 20, True, 5)
#                     print(f"Message scheduled for {name} at {hour:02}:{minute:02}.")
#                 except Exception as e:
#                     print(f"Failed to send the message: {e}")
#             else:
#                 print("Name not found in contact list.")
#         case 4:
#             print("Exiting program. Have a great day!")
#             break
#         case _:
#             print("\nInvalid choice! Please select a valid option.")

def play_music():
    speak("Tell me the name of the song u wanna hear first.")
    # song_name = listen()
    pk.playonyt(song_name + " song")

def play_yt():
    speak("What would u like to watch on youtube.")
    # query = listen()
    pk.playonyt(query)

def send_wsp_msg():
    contacts = {"swastik": "7067115104", "nihal": "7050946916", "nitya": "8840420294", "harshita": "8210049063", "nishant": "7000825113"}
    speak("Whom you wanna send message...")
    # name = listen()
    
    if name in contacts:
        speak("What is the message...")
        # msg = listen()
        cur_time = dt.now()
        
        # Handling the case if current time is near 59 minutes
        hour, minute = cur_time.hour, cur_time.minute + 1
        if minute >= 60:
            minute -= 60
            hour += 1
            if hour >= 24:
                hour = 0  # Roll back to 0 if hour goes past 23
                
            try:
                pk.sendwhatmsg(f"+91{contacts[name]}", msg, hour, minute, 20, True, 5)
                print(f"Message scheduled for {name} at {hour:02}:{minute:02}.")
            except Exception as e:
                print(f"Failed to send the message: {e}")
        else:
            speak("Contact not found.")
    
    
    speak(f"Okay sending the message to {name} within 1 minute....")
