import os
import json
import requests
from requests_oauthlib import OAuth1

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


def main():
    auth = OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                  TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    stream = requests.get(
        'https://userstream.twitter.com/1.1/user.json',
        auth=auth,
        stream=True
    )

    for line in stream.iter_lines():
        if len(line) <= 0:
            continue
        object = json.loads(line.decode('utf-8'))
        if 'text' in object:
            _user_name = user_name(object['user'])
            _user_icon = user_icon(object['user'])
            _text = object['text']
            post_to_slack(_user_name, _user_icon, _text)


def user_name(user):
    user_name = user['name']
    screen_name = user['screen_name']
    return '{}@{}'.format(user_name, screen_name)


def user_icon(user):
    return user['profile_image_url_https']


def post_to_slack(username=None, usericon=None, text=None):
    url = os.getenv('SLACK_POST_URL')
    payload = {
        'username': username,
        "icon_url": usericon,
        "text": text
    }
    payload_json = json.dump(payload)
    requests.post(url, data=payload_json)


if __name__ == '__main__':
    main()
