import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("./private/firebase-key.json")
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://property-analysis-dccc1.firebaseio.com'})
users_property = db.reference('users-property')
users_financial = db.reference('users-financial')

DEFAULT_USER_ID = "1"
