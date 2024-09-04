import re
import pyttsx3
import speech_recognition as sr

# function to make cono speak
def speak(text, display=True):
    if display:
        print("CONO:" + text)

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()

# helper function for play_yt(), if helps in extracting the search query
def extract_search_term(transcript):
    
    # Regular expression pattern to find what to search
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    
    match = re.search(pattern, transcript, re.IGNORECASE)
    
    return match.group(1) if match else None

# fucntion to remove additonal words from transcript
def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

# helper function to get name and mobile number of the contact
def findContact(transcript):
    contacts = {"swastik": "7067115104", "nihal": "7050946916", "nitya": "8840420294", "harshita": "8210049063", "nishant": "7000825113"}
    wordsToRemove = ['make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    transcript = remove_words(transcript, wordsToRemove)

    try:
        mobileNoStr = contacts[transcript]
        if not mobileNoStr.startswith('+91'):
            mobileNoStr = '+91' + mobileNoStr

        return transcript, mobileNoStr
    except:
        speak("not exist in contacts")
        return 0,0



# if __name__ == "__main__":
