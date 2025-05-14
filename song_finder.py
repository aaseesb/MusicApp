import requests
from fuzzywuzzy import fuzz
from langdetect import detect
from langdict import language_dictionary
import time
import yt_dlp
import os

initial = time.time()

class Song:
    def __init__(self, query):
        self.query = query
        self.title = ''
        self.artist  = ''
        self.album = ''
        self.date = ''
        self.language = 'eng'
        self.genres = []
        self.album_art = ''

        self.query_num = 0
        self.possible_titles = []
        
        self.headers = {
            "User-Agent":"CC-MusicApp"
        }

        self.url = ''
        self.video_id = ''

    def search_itunes(self):
        #api needs a header
        raw_data = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": self.query,
                "limit": 10,
                "media": "music",
                "entity": "musicTrack",
                "lang": "en_us",
                "country": "us"
            },
            headers=self.headers
        )
        
        json_data = raw_data.json()

        if not json_data['results']:
            self.title = "ERROR"
            return

        for i in range(len(json_data['results'])):
                print(i)
                result = json_data['results'][i]['trackName'] + ' by ' + json_data['results'][i]['artistName']
                self.possible_titles.append(result)  
                
                matching = fuzz.partial_ratio(self.query.lower(), json_data['results'][i]['trackName'].split(' ')[0].lower() )
                print(matching) 

                if matching > 90:
                    self.query_num = i
                    break
        else:
            self.title = 'ERROR'
            return
        
        data = json_data['results'][self.query_num]

        self.title = data['trackName']
        self.artist = data['artistName']
        self.album = data['collectionName']
        self.album_id = data['collectionId']
        self.date = data.get('releaseDate', '').split('T')[0]
        self.genre = data['primaryGenreName']
        self.language = language_dictionary.get(detect(self.title + self.artist + self.album), 'ERROR')
        self.album_art = data['artworkUrl100']
    
    # retrieve album image
    def get_album_cover(self):
        pass

    def retrieve_audio(self):
        query = f"{self.title} by {self.artist} song"
        search_query = f"ytsearch1:{query}"
        ydl_opts = {
            'format': 'bestaudio[ext=webm]/bestaudio',
            'quiet': True,
            'noplaylist': True,
            'extractaudio': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            
            if not info.get('entries'):
                raise Exception('No video found')
            video_info = info['entries'][0]
            self.url = video_info.get('url')
            self.video_id = video_info['id']


# functon to import song
def song_importer(query):
    song = Song(query)
    song.search_itunes()
    f1 = time.time() - initial
    if song.title != 'ERROR':
        song.get_album_cover()
        song.retrieve_audio()
        f2 = time.time() - initial
        # return(f2, song.title,song.artist,song.album_art,song.genre,song.date,song.language,song.album)
    # return(song.title,song.possible_titles)
    return(song)
