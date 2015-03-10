__author__ = 'kamesh'

"""The Main file which will source the needed modules and
call the function to generate the movie website"""

# Import the modules
import fresh_tomatoes
import movie_list

# call the function to generate the movie page and open the page in a browser
fresh_tomatoes.open_movies_page(movie_list.movie_list)
