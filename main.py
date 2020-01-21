import pandas as pd
import pause
import os
import validators
from datetime import datetime
from typing import Union

from twitter import TwythonWrapper, MAX_TWEET_LENGTH
from images import load_image_from_url, get_logo, merge_images


## path to edited spreadsheet (Removed api keys).
EXCEL_FILE_PATH = r".\tmp\GrowthAnalytics_python test_EDITED.xlsx"

tweet_index = 0 ## keeps track of where we are in the database.

def get_tweet_from_dataframe(dataframe: pd.DataFrame, index: int) -> Union[None, pd.Series]:
    """
        simple wrapper for the iloc command.
    """

    try:
        i = dataframe.iloc[index]
    except IndexError:
        return None
    
    text  = i.post_text
    image = i.post_img
    date = i.name

    return (date, text, image)


if __name__ == "__main__":

    ## Connect to twitter
    twitter_api = TwythonWrapper()

    ## load excel sheet
    tweet_data = df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="data_table")

    ## Remove rows where the date has already expired.
    ## Note that these two lines will remove everything given the current dataset.
    #mask = tweet_data["post_datetime"] > datetime.now()
    #tweet_data = tweet_data[mask]

    ## Sort and index by date (earliest first)
    tweet_data = tweet_data.sort_values(by='post_datetime')
    tweet_data = tweet_data.set_index("post_datetime")

    while tweet_index < len(tweet_data):

        next_tweet = get_tweet_from_dataframe(tweet_data, tweet_index)
        tweet_index += 1
        
        if next_tweet is None:
            break

        date, text, image_url = next_tweet

        if len(text) > MAX_TWEET_LENGTH:
            print(f"Error: Text was too long, not sending tweet {tweet_index}.")
            continue

        if not validators.url(str(image_url)):
            image_url = None

        ## Setup images, so that we are ready for posting.
        ## Saved to disk to reduce memory useage while we sleep.
        if image_url is not None:

            ## Add logo overlay to image.
            background = load_image_from_url(image_url)
            foreground = get_logo() # load up the image fresh each time to avoid possible mutation/side effects.

            filepath = os.path.join(os.path.dirname(__file__), "tmp", f"index_{tweet_index}")
            image_path = merge_images(background, foreground, filepath)

            img = open(image_path, "rb")
            media = twitter_api.upload_media(img)

        else:
            media = None

        ## sleep until post time.
        ## If we are past post time, pause wont pause.
        pause.until(date)
        #pause.minutes(0.1)

        try:
            twitter_api.send_tweet(text, media=media)
            print(f"tweet {tweet_index} sent")

        except Exception as e:
            print(f"Error: tweet {tweet_index} was not sent. message was {e}")