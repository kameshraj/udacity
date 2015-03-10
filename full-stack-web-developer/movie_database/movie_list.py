__author__ = 'kamesh'

"""This file contains list of movies defined. This also contains
the list movie_list which has all the movies we want to show on
the fresh tomato movie website"""

from movie import Movie

# define the movies
avatar = Movie("Avatar",
               "http://ia.media-imdb.com/images/M/MV5BMTYwOTEwNjAzMl5BMl5BanBnXkFtZTcwODc5MTUwMw@@._V1_SY317_CR0,0,214,317_AL_.jpg",
               "https://www.youtube.com/watch?v=cRdxXPV9GNQ",
               "Sam Worthington, Zoe Saldana, Sigourney Weaver",
               "2009")

schoolOfRock = Movie("The School Of Rock",
                     "http://ia.media-imdb.com/images/M/MV5BMjEwOTMzNjYzMl5BMl5BanBnXkFtZTcwNjczMTQyMQ@@._V1_SX214_AL_.jpg",
                     "https://www.youtube.com/watch?v=3PsUJFEBC74",
                     "Jack Black, Mike White, Joan Cusack",
                     "2003")

toyStory = Movie("Toy Story",
                 "http://ia.media-imdb.com/images/M/MV5BMTgwMjI4MzU5N15BMl5BanBnXkFtZTcwMTMyNTk3OA@@._V1_SY317_CR12,0,214,317_AL_.jpg",
                 "https://www.youtube.com/watch?v=KYz2wyBy3kc",
                 " Tom Hanks, Tim Allen, Don Rickles",
                 "1995")

findingNemo = Movie("Finding Nemo",
                    "http://ia.media-imdb.com/images/M/MV5BMTY1MTg1NDAxOV5BMl5BanBnXkFtZTcwMjg1MDI5Nw@@._V1_SY317_CR0,0,214,317_AL_.jpg",
                    "https://www.youtube.com/watch?v=SPHfeNgogVs",
                    "Albert Brooks, Ellen DeGeneres, Alexander Gould ",
                    "2003")

hermano = Movie("Hermano",
                "http://ia.media-imdb.com/images/M/MV5BMTQwNDEzNzg1N15BMl5BanBnXkFtZTcwMDgwODk1OA@@._V1_SY317_CR0,0,214,317_AL_.jpg",
                "https://www.youtube.com/watch?v=5vrrRJDN64U",
                "Fernando Moreno, Eliu Armas, Ali Rondon",
                "2010")

# create a list of movies to be displayed on the website
movie_list = [avatar, findingNemo, hermano, schoolOfRock, toyStory]