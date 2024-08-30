import cv2
from ffpyplayer.player import MediaPlayer as mp

def playMovie():

    choice = int(input("Currently you have rented:\n1) Kung fu panda 4\n2) How to train your dragon 3\n3) The Marvels\n4) Exit\nEnter your choice: "))

    path = None
    match choice:
        case 1:
            path = "D:\Movies\Kung.Fu.Panda.4.mkv"
        case 2:
            path = "D:\Movies\How.To.Train.Your.Dragon.3.mkv"
        case 3:
            path = "D:\Movies\The.Marvels.mkv"
        case 4:
            exit()
        case _:
            print("\nInvalid choice! Please select a valid option.")
    cap = cv2.VideoCapture(path)
    cap.set(3, 740)
    cap.set(4, 480)

    # making object for audio capture
    audio = mp(path)

    # reading background image
    imgbackground = cv2.imread('gui_content/background.jpg')
    while True:
        success, frame = cap.read()
        audio_success, val = audio.get_frame()
        # Space for Gui integration
        frame = cv2.resize(frame, (687, 335))
        imgbackground[143:143+335, 50:50+687] = frame  # Adding webcam part to background
        
        cv2.imshow("Face Lock", imgbackground)
        if cv2.waitKey(1) == 27: break

if __name__ == "__main__":
    playMovie()