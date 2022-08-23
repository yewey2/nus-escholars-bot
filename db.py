import firebase_admin
from firebase_admin import (
    credentials,
    firestore
)

import os
from dotenv import load_dotenv
load_dotenv()
import datetime
import json

# Use a service account
cred = credentials.Certificate('./serviceAccountKey.json')
# d = json.loads(os.environ.get('DB_CREDENTIALS'))
# cred = credentials.Certificate(d)
firebase_admin.initialize_app(cred)

client = firestore.client()

db = client.collection('angelmortal')

def new_user(username, name="John Doe", chat_id=-1):
    print('make new user')
    doc_ref = db.document(username)
    doc_ref.set({
        # data here
        'name':name,
        'chat_id':chat_id,
        'username':'johndoe123',
        'chat_with': 0
    })
    return db.document(username).get()

def get_user(username):
    user = db.document(username).get()
    if not user.exists:
        print('user not found')
        user = new_user(username)
    else:
        print('user found')
    return user

def get_chat_id(username):
    user = db.document(username).get()
    if not user.exists:
        return None
    return user.get('chat_id')

def update_chat_id(username,chat_id):
    user = get_user(username)
    user.reference.update({'chat_id':chat_id})
