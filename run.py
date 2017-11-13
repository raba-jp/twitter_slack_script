import json
import requests
from requests_oauthlib import OAuth1
import settings


def main():
    auth = OAuth1(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    stream = requests.get(
        'https://userstream.twitter.com/1.1/user.json',
        auth=auth,
        stream=True,
        timeout=(240.0, 240.0)
    )
    url = 'https://twitter.com/{}/status/{}'

    for line in stream.iter_lines():
        if len(line) <= 0:
            continue
        object = json.loads(line.decode('utf-8'))
        if 'text' in object:
            post(url.format(object['user']['screen_name'], object['id_str']))


def post(text):
    url = settings.SLACK_POST_URL
    payload = {
        'username': 'Twitter',
        "text": text
    }
    print(payload)
    payload_json = json.dumps(payload)
    requests.post(url, data=payload_json)


if __name__ == '__main__':
    main()
