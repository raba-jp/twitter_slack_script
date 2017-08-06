import json
import requests
from requests_oauthlib import OAuth1
import settings
import slack


class Tweet:
    def __init__(self, json):
        self.user_name = '{}@{}'.format(
            json['user']['name'],
            json['user']['screen_name']
        )
        self.user_icon = json['user']['profile_image_url_https']
        self.text = json['text']


def run():
    auth = OAuth1(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
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
            tweet = Tweet(object)
            slack.post(tweet.user_name, tweet.user_icon, tweet.text)


if __name__ == '__main__':
    run()
