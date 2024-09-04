import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

print("Stablishing connection with database...")
cred = credentials.Certificate('.conda/ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-lock-b0fb3-default-rtdb.firebaseio.com/'
})
print("Connection Stablished...")
ref = db.reference('Users')

data = {
    '123654':
        {
            "name" : "Swastik",
            "LastDetectedTime":"2023-09-23 00:00:00",
        },
    '123564':
        {
            "name": "Harshita",
            "LastDetectedTime" : "2023-09-23 00:00:00",
        },
    '123456':
        {
            "name": "Nihal",
            "LastDetectedTime" : "2023-09-23 00:00:00",
        },
    '123489':
        {
            "name": "Nitya",
            "LastDetectedTime" : "2023-09-23 00:00:00",
        },
    '123789':
        {
            "name": "Saksham",
            "LastDetectedTime" : "2023-09-23 00:00:00",
        },
}

# Uploading the data in firebase
print("Adding data to database...")
for key, value in data.items():
    ref.child(key).set(value)
else:
    print("Data added successfully!!")