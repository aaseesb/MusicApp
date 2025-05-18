# 🎶 MusicApp
A web app built using Flask, Python, HTML, CSS, and Javascript that allows users to search for songs. The app uses the ITunes and Deezer APIs to retrieve and display song data, including the title, artist, publication year, and genre. Users may also listen to the song using audios fetched via yt-dlp.  
*This project exists solely as a proof of concept and is not designed for commercial or production use.*

## Documentation

1. **Clone the repository** `git clone https://github.com/aaseesb/MusicApp`

2. **Install dependencies** `pip install -r requirements.txt`

3. **Run the application** `app.py`

4. **Open your browser and visit** `http://127.0.0.1:5000`

## Features
- Search for songs by title
- Displays:
  - Title
  - Artist
  - Year of release
  - Genre
  - Language
  - Album cover
- Plays audio streams
- Uses:
  - [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/)
  - [Deezer API](https://developers.deezer.com/api)
  - [yt-dlp](https://github.com/yt-dlp/yt-dlp)

##  Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** iTunes, Deezer
- **Audio Retrieval::** yt-dlp (Python module)
