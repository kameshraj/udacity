__author__ = 'kamesh'

"""Movie class which defines the template for movies"""

class Movie():
    def __init__(self, title, poster, trailer, actors, year):
        self.title = title
        self.poster_image_url = poster
        self.trailer_youtube_url = trailer
        self.actors = actors
        self.year = year

