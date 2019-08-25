import json

import firebase_admin
from firebase_admin import credentials, db
from pyrebase import pyrebase

cred = credentials.Certificate("./private/firebase-key.json")
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://property-analysis-dccc1.firebaseio.com'})
users_property = db.reference('users-property')
users_financial = db.reference('users-financial')

DEFAULT_USER_ID = "1"

with open("./private/firebase-webapp.json") as json_file:
    pyrebase_config = json.load(json_file)

pyrebase_app = pyrebase.initialize_app(pyrebase_config)
pyrebase_auth = pyrebase_app.auth()
