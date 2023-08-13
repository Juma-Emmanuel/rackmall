import json
import requests
from django.conf import settings
import firebase_admin
from firebase_admin import storage

def push_data(data):
    url = f"{settings.FIREBASE_CONFIG['databaseURL']}/data.json"
    response = requests.post(url, json=data)
    return response

def get_data():
    url = f"{settings.FIREBASE_CONFIG['databaseURL']}/data.json"
    response = requests.get(url)
    data = response.json()
    return data

def upload_image(image_bytes, filename):
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type='image/jpeg')  # Adjust content type as needed
    return blob.public_url
def upload_image1(image_bytes, filename):
    storage_url = f"https://firebasestorage.googleapis.com/v0/b/{settings.FIREBASE_CONFIG['storageBucket']}/o/{filename}"
    response = requests.post(storage_url, data=image_bytes)
    return response
