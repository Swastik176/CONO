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
import threading

# Initialize Firebase
cred = credentials.Certificate('ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-lock-b0fb3-default-rtdb.firebaseio.com/',
    'storageBucket': 'face-lock-b0fb3.appspot.com'
})
bucket = storage.bucket()

def load_encodings():
    """Load face encodings from file."""
    print("Loading Encode File .....")
    with open('Encoding.p', 'rb') as file:
        encodelistKnownids = pickle.load(file)
    if len(encodelistKnownids) != 2:
        raise ValueError("The loaded data does not have the expected format.")
    return encodelistKnownids

def detect_face(encodelistKnown, userids):
    """Detect face and return the user name if matched."""
    cap = cv2.VideoCapture(0)
    cap.set(3, 740)
    cap.set(4, 480)

    # Load resources
    imgbackground = cv2.imread('gui_content/background.jpg')
    folderModePath = 'gui_content/Modes'
    modepath = os.listdir(folderModePath)
    imgmodeslist = [cv2.imread(os.path.join(folderModePath, path)) for path in modepath]

    # Initialize variables
    counter = 0
    counter2 = 0
    session = 0
    modechanger = 0
    found = False
    userInfo = {}

    while True:
        session += 1
        success, img = cap.read()

        # Process frame
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if counter <= 5:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodelistKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodelistKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    counter += 1
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 50 + x1, 143 + y1, x2 - x1, y2 - y1
                    imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)
                    modechanger = 1
                    
                    id = userids[matchIndex]
                    if not found:
                        found = True
                        userInfo = db.reference(f'Users/{id}').get()
                        blob = bucket.get_blob(f'person/{id}.jpeg')
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        imgUser = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                        detectedtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ref = db.reference(f'Users/{id}')
                        ref.child('LastDetectedTime').set(detectedtime)
                        userInfo['LastDetectedTime'] = detectedtime

        if found:
            (w,h),_ = cv2.getTextSize(userInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 0.8, 1)
            offset = (542-w)//2
            cv2.putText(imgbackground, str(userInfo['name']), (828 + offset, 362), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 1)
            cv2.putText(imgbackground, str(userInfo['LastDetectedTime']), (1003, 400), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1)
            imgUser = cv2.resize(imgUser, (160, 160))
            imgbackground[110:110+160, 958:958+160] = imgUser
            counter += 1

        if counter > 5:
            counter2 += 1
            modechanger = 2
            imgmodeslist[modechanger] = cv2.resize(imgmodeslist[modechanger], (483, 615))
            imgbackground[32:32 + 615, 785:785 + 483, :] = imgmodeslist[modechanger]

        if counter2 > 5:
            break

        if session > 200:
            print("Session Expired, please try again!!")
            break

        cv2.imshow("Face Lock", imgbackground)
        if cv2.waitKey(1) == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()
    return userInfo.get('name') if found else None

def faceDetect():
    """Wrapper function to handle face detection with preloading."""
    encodelistKnownids = load_encodings()
    encodelistKnown, userids = encodelistKnownids
    return detect_face(encodelistKnown, userids)

def start_face_detection():
    """Start face detection in a separate thread."""
    thread = threading.Thread(target=faceDetect)
    thread.start()
    return thread

if __name__ == "__main__":
    print("Starting face detection...")
    face_detection_thread = start_face_detection()
    face_detection_thread.join()  # Wait for the face detection to complete
    print("Face detection complete.")
