import os
import cv2
import pickle
import face_recognition
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials

# Connecting database to upload images
cred = credentials.Certificate('.conda/ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-lock-b0fb3-default-rtdb.firebaseio.com/',
    'storageBucket': 'face-lock-b0fb3.appspot.com'
})

folderpath = 'person'
pathlist = os.listdir(folderpath)

imglist = []
userids = []

# Fetching all the images
for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath, path)))
    userids.append(os.path.splitext(path)[0])

    # Uploading the images to the database
    fileName = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName) 

def findencodings(imageList):
    encodelist = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

print("Encoding Started....")
encodelistKnown = findencodings(imglist)
encodelistKnownids = [encodelistKnown, userids]  # Combine encodings and user IDs
print("Encoding Completed....")

# Save both encodings and user IDs
with open('Encoding.p', 'wb') as file:
    pickle.dump(encodelistKnownids, file)
print("File Saved.")
