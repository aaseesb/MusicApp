import discogs_client
from releases import Song, Album
import os
from dotenv import find_dotenv, load_dotenv

# initialize apis
discogs_token = os.getenv("DISCOGS_KEY")
d = discogs_client.Client('SampleMusicApp/0.1', user_token=discogs_token)

class Engine():
    # searching for a song through discogs api using title and artist
    def search(self, title, artist):
        try:
            search_results = d.search(title = title, artist = artist, type = 'release')
        # resolve error where too many requests occur - specific to discogs searches
        except discogs_client.exceptions.HTTPError:
            print('Too many requests. Please wait a minute to search again.')
            return []
        
        # checking for duplicates
        results = []
        seen = set()

        for item in search_results.page(1):
            # limit the amount of results retrieved to 5 to reduce the chance of errors due to too many requests
            if len(results) >5: 
                break
            
            try:
                item_type = item.formats[0]['descriptions'][0] # e.g. 'single' or 'album'
                identifier = (item.title, item_type)

                # if a result with the same title and type already exists, the loop will skip to the next result
                if identifier in seen:
                    continue
                else:
                    seen.add(identifier);

                # append items to results while differentiating between singles and albums
                if item_type == 'Single':
                    # songs have the attributes title, artist, and image
                    results.append(Song(
                        item.title, 
                        item.artists[0].name, 
                        item.images[0]['uri']
                    ))
                else:
                    # albums have one additional attribute of a tracklist
                    results.append(Album(
                        item.title, 
                        item.artists[0].name, 
                        item.images[0]['uri'],
                        item.tracklist
                    ))
            except (KeyError, IndexError):
                continue
        
        # return the list of albums and songs to display
        return results
    
# e = Engine()
# list = e.search("shake it off", "taylor swift")
# print(list[0].title, "  ", list[0].artist, list[0].image)