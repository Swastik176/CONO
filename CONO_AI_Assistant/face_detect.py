import cv2
import os
import cvzone
import pickle
import numpy as np
import face_recognition
import firebase_admin
from datetime import datetime
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials

# Connecting database to upload images
cred = credentials.Certificate('.conda\ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-lock-b0fb3-default-rtdb.firebaseio.com/',
    'storageBucket': 'face-lock-b0fb3.appspot.com'
})
bucket = storage.bucket()

def faceDetect():
    cap = cv2.VideoCapture(0)
    cap.set(3, 740)
    cap.set(4, 480)

    # reading background image
    imgbackground = cv2.imread('gui_content/background.jpg')

    # importing the mode images
    folderModePath = 'gui_content/Modes'
    modepath = os.listdir(folderModePath)
    imgmodeslist = []
    for path in modepath:
        imgmodeslist.append(cv2.imread(os.path.join(folderModePath, path)))

    # Load the encoding file
    print("Loading Encode File .....")
    with open('Encoding.p', 'rb') as file:
        encodelistKnownids = pickle.load(file)

    # Check the structure of the loaded data
    if len(encodelistKnownids) != 2:
        raise ValueError("The loaded data does not have the expected format. Expected 2 items, got {}".format(len(encodelistKnownids)))

    # Unpack the loaded data
    encodelistKnown, userids = encodelistKnownids
    print("Encode File Loaded.....")

    id = -1
    cnt = 0 # to download the image from the database in first iteration 
    imgUser = []
    counter = 0 
    counter2 = 0
    session = 0
    matched = False
    modechanger = 0

    while True:
        session += 1
        success, img = cap.read()
        # Face Recognition
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Space for Gui integration
        img = cv2.resize(img, (687, 335))
        imgbackground[143:143+335, 50:50+687] = img  # Adding webcam part to background
        imgmodeslist[modechanger] = cv2.resize(imgmodeslist[modechanger], (483, 615))
        imgbackground[32:32 + 615, 785:785 + 483, :] = imgmodeslist[modechanger]  # Adding mode to the project


        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        # Comparing current frame from our database
        if(counter <= 5):
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodelistKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodelistKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    matched = True
                    counter += 1
                    # y1, x2, y2, x1 = faceLoc
                    # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    # bbox = 50 + x1, 143 + y1, x2 - x1, y2 - y1
                    # imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)
                    modechanger = 1
                    
                    id = userids[matchIndex]
                    if(cnt == 0): cnt = 1
            

        if(cnt != 0):
            if(cnt == 1):
                # Getting textual data
                userInfo = db.reference(f'Users/{id}').get()
                print(userInfo)
                
                # Getting the image
                blob = bucket.get_blob(f'person/{id}.jpeg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgUser = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                
                # update data of the last time detected
                detectedtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(detectedtime)
                ref = db.reference(f'Users/{id}')
                ref.child('LastDetectedTime').set(detectedtime)
                print(userInfo)
            
            # Putting content in output window
            # Name
            (w,h),_=cv2.getTextSize(userInfo['name'],cv2.FONT_HERSHEY_COMPLEX,0.8,1)
            offset = (542-w)//2
            cv2.putText(imgbackground,str(userInfo['name']),(828 + offset, 362),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
            
            # Last Detected Time
            cv2.putText(imgbackground,str(userInfo['LastDetectedTime']),(1003,400),cv2.FONT_HERSHEY_DUPLEX,0.6,(255,255,255),1)
            
            # Image
            imgUser = cv2.resize(imgUser, (160, 160))
            imgbackground[110:110+160,958:958+160] = imgUser
            cnt += 1

        if(counter > 5):
            counter2 += 1
            modechanger = 2
            imgmodeslist[modechanger] = cv2.resize(imgmodeslist[modechanger], (483, 615))
            imgbackground[32:32 + 615, 785:785 + 483, :] = imgmodeslist[modechanger]  # Adding mode to the project

        found = False
        if(counter2 > 5):
            found = True
            break

        if(session > 200):
            print("Session Expired, please try again!!")
            break
        cv2.imshow("Face Lock", imgbackground)
        if cv2.waitKey(1) == 27: break

    cap.release()
    cv2.destroyAllWindows()
    if(found):
        return userInfo['name']
    return -1

if __name__ == "__main__":
    name = faceDetect()
    print(name)
