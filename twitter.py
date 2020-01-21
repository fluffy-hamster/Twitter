from twython import Twython
from typing import List

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

MAX_TWEET_LENGTH = 280

"""
https://projects.raspberrypi.org/en/projects/getting-started-with-the-twitter-api
"""

class TwythonWrapper():

    def __init__(self):
        self.api_handle = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

    def upload_media(self, media) -> List[str]:
        response = self.api_handle.upload_media(media=media)
        media_id = [response['media_id']]
        return media_id

    def send_tweet(self, message: str, media: List[str] = None) -> None:
        self.api_handle.update_status(status=message, media_ids=media)
