class Song():
    def __init__(self, title, artist, image, genres, year, country, subgenres):
        self.type = 'Song'
        self.title = title
        self.artist = artist
        self.image = image
        self.genres = ", ".join(genres)
        self.year = year
        self.country = country
        self.subgenres = ", ".join(subgenres)

    def play(self):
        search_result = self.search()
    

# # parent for both song and album to inherit from
# class Release():
#     def __init__(self, title, artist, image):
#         self.type = 'Release'
#         self.title = title
#         self.artist = artist
#         self.image = image

# class Album(Release):
#     def __init__(self, title, artist, image, tracklist) :
#         super().__init__(title = title, artist = artist, image = image)
#         self.type = 'Album'
#         self.tracklist = tracklist

# class Song(Release):
#     def __init__(self, title, artist, image):
#         super().__init__(title = title, artist = artist, image = image)
#         self.type = 'Song'