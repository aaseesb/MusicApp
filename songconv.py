import requests
from fuzzywuzzy import fuzz
from langdetect import detect
from langdict import language_dictionary
import time
import os

#the itunes search takes ~1.5 seconds and the image search takes ~1 second but this bastard youtube downloader bullshit takes 20 seconds
import yt_dlp

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

        self.itunes_data = ''
        self.query_num = 0
        self.possible_titles = []
        
        self.headers = {
            "User-Agent":"CC-MusicApp"
        }

    def search_itunes(self):
        raw_data = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": self.query,
                "limit": 5,
                "media": "music",
                "entity": "musicTrack",
                "lang": "en_us",
                "country": "us"
            },
            headers=self.headers
        )
        
        json_data = raw_data.json()
        
        b=time.time()
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
        try:
            self.title = self.title[:self.title.index('(')].strip() #remove brackets with versions
        except:
            pass

        self.artist = data['artistName']
        self.date = data.get('releaseDate', '').split('T')[0]
        self.genre = data['primaryGenreName']
        self.language = language_dictionary.get(detect(self.title + self.artist + self.album), 'ERROR')
        
        self.itunes_data = data
    
    # retrieve album image
    def get_album_cover(self):
        url = f'https://api.deezer.com/search/album?q={self.title} {self.artist}'
        response =  requests.get(url)
        data = response.json()
        if data['data']:
            self.album = data['data'][0]['title']
            self.album_art = data['data'][0]['cover_big']
            
        else:
            self.album = self.itunes_data['collectionName']
            self.album_art = self.itunes_data['artworkUrl100']

# function to import song
def song_importer(query):
    song = Song(query)
    song.search_itunes()
    if song.title != 'ERROR':
        song.get_album_cover()
        # song.retrieve_audio()
        #return(song.title,song.artist,song.album_art,song.album,song.url)
    #return(song.title,song.possible_titles)
    return(song)

def get_audio(title, artist):
    output_dir = 'static/downloads'
    os.makedirs(output_dir, exist_ok=True)

    # clear previous downloads
    for subdir, dirs, files in os.walk(output_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")

    query = f"{title} by {artist} song"
    search_query = f"ytsearch1:{query}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/{title}.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'extractaudio': True,
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'webm',
        #     'preferredquality': '192',
        # }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=True)
        
        if not info.get('entries'):
            raise Exception('No video found')
        video_info = info['entries'][0]
        video_url = video_info.get('url')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print('downloading')
            ydl.download([video_url])


# get_audio('i love you so', 'the walters')