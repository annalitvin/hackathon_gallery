from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import PhotoEmotion

import flickrapi
import requests
import json
import time
import threading

from .config import *

# Create your views here.


def get_photos_by_description(flickr, user_id='144522605@N06', description='#int20h'):
    photos_resp = flickr.people_getPhotos(user_id=user_id, per_page=10,
                                          extras='url_c, description')
    return set([photo.get('url_c') for photo in photos_resp.findall('photos')[0]
                if photo.findall('description')[0].text == description])


def get_photos_from_photoset(flickr, photoset_id="72157674388093532"):
    return set([photo.get('url_c') for photo in flickr.walk_set(photoset_id=photoset_id, per_page=10, extras='url_c')])


def get_face_tokens(photp_url):
    data = {
        "api_key": face_api_key,
        "api_secret": face_api_secret,
        "image_url": photp_url
    }
    resp = requests.post(url=face_detect_url, data=data)
    resp_json = resp.json()
    face_tokens = ""
    if 'faces' in resp_json:
        face_tokens = ",".join([i['face_token'] for i in resp_json['faces']])
    return face_tokens


def get_emotions_by_tocken(face_tokens):
    data = {
        "api_key": face_api_key,
        "api_secret": face_api_secret,
        "face_tokens": face_tokens,
        "return_attributes": "emotion"
    }
    resp = requests.post(url=face_analyze_url, data=data)
    resp_json = resp.json()
    if 'faces' in resp_json:
        return [{face['face_token']: face["attributes"]['emotion']} for face in resp_json['faces']]
    else:
        return []


def detect_emotions_and_save(set_of_photos):
    counter = 0
    for photo in set_of_photos:
        emotions_list = get_emotions_by_tocken(get_face_tokens(photo))
        sum_emotions = {}
        for face in emotions_list:
            for face_token in face:
                for emotion_name in face[face_token]:
                    if emotion_name in sum_emotions:
                        sum_emotions[emotion_name] += face[face_token][emotion_name]
                    else:
                        sum_emotions[emotion_name] = face[face_token][emotion_name]
        result_emotion = "no emotions"
        if len(sum_emotions) > 0:
            result_emotion = max(sum_emotions.keys(), key=lambda n: sum_emotions[n])

        save_emption(photo, result_emotion)
        counter += 1


def save_emption(url, emotion):
    photo = PhotoEmotion()
    photo.photo_url = str(url)
    photo.emotion = str(emotion)
    photo.save()


def home_page(request):
    return TemplateResponse(request, 'gallery.html', {})


def update_photos():
    while True:
        flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret, cache=True)
        set_of_photos = get_photos_from_photoset(flickr, photoset_id=photoset_id)
        extra_photos = get_photos_by_description(flickr, user_id=user_id, description=description)
        for i in extra_photos:
            set_of_photos.add(i)

        photos = PhotoEmotion.objects.all()
        for photo in photos:
            if photo.photo_url in set_of_photos:
                set_of_photos.remove(photo.photo_url)

        detect_emotions_and_save(set_of_photos)
        time.sleep(50000)


def get_photos_from_db():
    photos = PhotoEmotion.objects.all()
    data = {}
    for photo in photos:
        if photo.emotion in data:
            data[photo.emotion].append(str(photo.photo_url))
        else:
            data[photo.emotion] = [str(photo.photo_url)]
    return json.dumps(data)


def update_page(request):
    data = get_photos_from_db()
    return HttpResponse(data, content_type='application/json')


t = threading.Thread(target=update_photos)
t.start()
