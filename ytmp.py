import yt_dlp
import os
import time


def download_webm(title, artist, output_path = './'):
    query = f"{title} by {artist} song"
    search_query = f"ytsearch1:{query}"
    ydl_opts = {
        'format': 'bestaudio[ext=webm]/bestaudio',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'extractaudio': True,
    }

    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
        info = ydl.extract_info(search_query, download=False)
        
        global f1
        f1 = time.time()
        
        if not info.get('entries'):
            raise Exception('No video found')
        video_info = info['entries'][0]
        video_url = video_info['url']

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        
        global f2
        f2 = time.time()

# Example usage:
initial = time.time()
download_webm('i love you so', 'the walters')

print(f2-initial, f1-initial)
