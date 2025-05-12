import discogs_client
from releases import Song
import os
from dotenv import find_dotenv, load_dotenv
from discogs_client.models import Release

# initialize apis
discogs_token = os.getenv("DISCOGS_KEY")
d = discogs_client.Client('SampleMusicApp/0.1', user_token=discogs_token)

class Engine():
    # searching for a song through discogs api using title and artist
    def search(self, title, artist):
        try:
            search_results = d.search(release_title = title, artist = artist, type = 'single')
        # resolve error where too many requests occur - specific to discogs searches
        except discogs_client.exceptions.HTTPError:
            print('Too many requests. Please wait a minute to search again.')
            return
        
        # find song item to return
        for item in search_results.page(1):
            if isinstance(item, Release):
                try: 
                    return Song(item.tracklist[0].title, item.artists[0].name, item.images[0]['uri'], item.genres, item.year, item.country, item.styles)
                except (KeyError, AttributeError) as e:
                    continue
            else:
                continue