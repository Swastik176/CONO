import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate('ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-lock-b0fb3-default-rtdb.firebaseio.com/'
})

ref = db.reference('Users')

data = {
    '123654':
        {
            "name" : "Swastik",
            "LastDetectedTime":"2023-09-23 00:00:00",
        }
}

# Uploading the data in firebase
for key, value in data.items():
    ref.child(key).set(value)
