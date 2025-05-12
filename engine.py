import discogs_client
from releases import Song
import os
from dotenv import find_dotenv, load_dotenv

# initialize apis
discogs_token = os.getenv("DISCOGS_KEY")
d = discogs_client.Client('SampleMusicApp/0.1', user_token=discogs_token)

class Engine():
    # searching for a song through discogs api using title and artist
    def search(self, title, artist):
        try:
            search_results = d.search(title = title, artist = artist, type = 'single')
        # resolve error where too many requests occur - specific to discogs searches
        except discogs_client.exceptions.HTTPError:
            print('Too many requests. Please wait a minute to search again.')
            return
        
        # find song item to return
        for item in search_results.page(1):
            try: 
                return Song(item.title, item.artists[0].name, item.images[0]['uri'])
            except (KeyError, AttributeError):
                continue