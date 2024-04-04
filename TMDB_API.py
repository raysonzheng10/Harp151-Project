import requests
import json

# Make a class to handle all TMDB API interactions
class TMDB_API:
    # initialize with apikey
    def __init__(self, APIKEY):
        self.APIKEY = APIKEY
        self.baseURL = 'https://api.themoviedb.org/3'

    # define a method to get the movie id based off a movie title
    def get_movie_id(self, movie_title:str ) -> str:
        # create url and make requets
        url = f'{self.baseURL}/search/movie?api_key={self.APIKEY}&query={movie_title}'

        res = requests.get(url)
        data = res.json()

        # parse through the data, if index/key error, means movie title was bad
        try:
            movie_id = data['results'][0]['id']
        except IndexError or KeyError:
            print("Unable to find movie id.")
            return ""

        return movie_id
        # returns a empty string if unable to find the movie id
    
    # define a method to grab the review based off a movie id, limiting to a default number of 10 reviews
    def get_reviews_from_ID(self, movie_id:str, number_limit: int = 10) -> list[str]:
        reviews = []
        url = f'{self.baseURL}/movie/{movie_id}/reviews?api_key={self.APIKEY}'
        
        res = requests.get(url)
        data = res.json()

        try:
            results = data['results']

            # each entry has data on each user review, on what they wrote, their name, the date of posting, etc.
            for entry in results:
                # check if the number of reviews exceeded the number limit
                if len(reviews) >= number_limit:
                    break
                review = entry['content']
                reviews.append(review)
        except KeyError:
            print("Unable to retrieve user reviews.")
        
        return reviews
        # returns an empty list if unable to retrieve user reviews
    
    # this method just combines getting the movie id and getting the reviews, might be obsolete?
    def get_reviews_from_title(self, movie:str, number_limit: int = 10) -> list[str]:
        movie_id = self.get_movie_id(movie)
        reviews = self.get_reviews_from_ID(movie_id, number_limit)

        return reviews
    
    # TODO: create a method to grab the yt trailer video link and get the video id


TMDB_APIKEY = 'ccf9c9b2f8cdb6869ab8953b3eff620f'

tmdb_API = TMDB_API(TMDB_APIKEY)

reviews = tmdb_API.get_reviews_from_title('the dark knight', 5)
print(reviews)