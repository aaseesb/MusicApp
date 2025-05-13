import requests
# from fuzzywuzzy import fuzz

#import time
#initial = time.time()

class Song:
    def __init__(self, query):
        self.query = query
        self.title = ''
        self.artist  = ''
        self.album = ''
        self.date = ''
        self.language = ''
        self.genres = []
        self.country = ''
        self.album_art = ''

        self.query_num = 0
        self.possible_titles = []
        self.release_id = ''
        self.artist_id = ''
        
        self.headers = {
            "User-Agent":"CC-MusicApp"
        }

    def search_recording_musicbrainz(self):
        #api needs a header
        raw_data = requests.get('https://musicbrainz.org/ws/2/recording/',
                                    params={
                                        "query":f"recording:{self.query}",
                                        "fmt": "json",
                                        "limit": 10, 
                                        "inc": "artist-credits+releases"
                                    },
                                    headers=self.headers)
        
        json_data = raw_data.json()
        if not json_data['recordings']:
            self.title = "ERROR"
            return

        for i in range(9):
            result = json_data['recordings'][i]['title'] + ' by ' + json_data['recordings'][i]['artist-credit'][0]['name']
            self.possible_titles.append(result)
            

            matching = fuzz.partial_ratio(self.query.lower(), json_data['recordings'][i]['title'].split(' ')[0].lower() )
            print(matching)

            if matching >=80:
                self.query_num = i
                break
        else:
            self.title = 'ERROR'
            return

        
        data = json_data['recordings'][self.query_num]
        self.title = data['title']
        self.artist = data['artist-credit'][0]['name']
        
        self.artist_id = data['artist-credit'][0]['artist']['id']
        release = data['releases'][0]

        if release != None:
            self.album = release['title']
            self.date = release.get('date')
            self.country = release.get('country')
            self.release_id = release['id']
            
        
        
    def search_release_musicbrainz(self):

        raw_data = requests.get(
                f"https://musicbrainz.org/ws/2/release/{self.release_id}",
                params={"inc": "genres+labels", 
                        "fmt": "json"},
                headers=self.headers
            )
        
        json_data = raw_data.json()
        self.language = json_data.get("text-representation", {}).get("language", "Unknown")
        self.genres = [g["name"] for g in json_data.get("genres", [])]
        
        if not self.genres:
            raw_data = requests.get(
            f"https://musicbrainz.org/ws/2/artist/{self.artist_id}",
            params={"inc": "genres", "fmt": "json"},
            headers=self.headers
        )
        json_data = raw_data.json()
        self.genres = [g["name"] for g in json_data.get("genres", [])]
    
    def get_album_cover(self):
        self.album_art = f"https://coverartarchive.org/release/{self.release_id}/front"

def SongImporter(query):
    song = Song(query)
    song.search_recording_musicbrainz()
    #f1 = time.time() - initial
    if song.title != 'ERROR':
        song.search_release_musicbrainz()
        #f2 = time.time() - initial
        song.get_album_cover()
        #f3 = time.time() - initial
        #return(f1,f2,f3,song.title,song.artist,song.album_art,song.country,song.date,song.language,song.album)
    #return(song.title,song.possible_titles)
