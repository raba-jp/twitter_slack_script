import requests
from json import dumps
from settings import SLACK_POST_URL


def post(username=None, usericon=None, text=None):
    url = SLACK_POST_URL
    payload = {
        'username': username,
        "icon_url": usericon,
        "text": text
    }
    payload_json = dumps(payload)
    requests.post(url, data=payload_json)
