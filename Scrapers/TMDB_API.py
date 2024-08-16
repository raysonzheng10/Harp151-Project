# Not being used right now, opting for rottentomatoes instead
import requests
import json
import urllib.request 
import time
# Make a class to handle all TMDB API interactions
class TMDB_API:
    # initialize with apikey
    def __init__(self, APIKEY):
        self.APIKEY = APIKEY
        self.baseURL = 'https://api.themoviedb.org/3'
        self.baseImageURL = 'https://image.tmdb.org/t/p/original'

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

    # makes a method that returns similar movie titles, returns a list of lists
    def get_similar_movies(self, movie_title:str) -> list[list[str]]:
        # make api call
        url = f'{self.baseURL}/search/movie?api_key={self.APIKEY}&query={movie_title}'
        res = requests.get(url)
        data = res.json()

        titles = []
        try:
            all_movies = data['results']

            for movie in all_movies:
                # grab title and release date
                title = movie['original_title']
                release_date = movie['release_date']

                # if no release date, movie hasn't come out yet so ignore
                if release_date == '':
                    continue
                
                release_year = release_date.split('-')[0] #use splicing to grab just the year
                # store the title and release year as a list inside the titles list
                titles.append([title,release_year])
            
            titles.pop(0)
        except KeyError:
            print("Invalid movie title.")

        # if it didn't work, we return empty list
        return titles
    
    # define a method to grab the review based off a movie id, limiting to a default number of 10 reviews
    def get_reviews(self, movie_title:str, number_limit: int = 20) -> list[str]:
        reviews = []

        movie_id = self.get_movie_id(movie_title)
        if movie_id == "":
            return False # if invalid id, return False

        # make the api call
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
    
    # This method grabs the youtube video id based on a movie title, can be used later in youtube API
    def get_YoutubeTrailer_ids(self, movie_title: str) -> str:
        # get the corresponding TMDB movie id from the title
        movie_id = self.get_movie_id(movie_title)
        if movie_id == "":
            return False # if the movie_id is invalid, return False

        # make the api call
        url = f'{self.baseURL}/movie/{movie_id}/videos?api_key={self.APIKEY}&append_to_response=videos'
        res = requests.get(url)
        data = res.json()

        video_ids = []
        # parse through the data
        results = data['results']
        for video in results:
            if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                # only grab id for trailer and Yt videos
                video_ids.append(video.get('key'))
            
        return video_ids

    # this method saves a png of a given image path from the TMDB API
    def save_image(self, image_path: str) -> None:
        url = f'{self.baseImageURL}/{image_path}'

        urllib.request.urlretrieve( 
        f'{url}', 
        r"images\poster.png") 
        # no return value
    
    # This method prints out a dictionary that contains basic information about a movie (title, description, genres)
    def get_movie_info(self, movie_title: str) -> dict:
        # get the corresponding TMDB movie id from the title
        movie_id = self.get_movie_id(movie_title)
        if movie_id == "":
            return False # if bad movie_id, return False
        
        # make the api call
        url = f'{self.baseURL}/movie/{movie_id}?api_key={self.APIKEY}'
        res = requests.get(url)
        data = res.json()

        # grab the information and put it all in the info dictionary
        info = {}
        genres = []
        for genre in data['genres']:
            genres.append(genre['name'])
        info['title'] = data['original_title']
        info['overview'] = data['overview']
        info['release_date'] = data['release_date'].split("-")[0]
        info['genres'] = genres

        # if we were able to get a poster, save it as True, else save it as False
        if data['poster_path'] == None:
            info['poster'] = False
        else:
            # if the poster path is valid, save that poster to our repo
            info['poster'] = True
            self.save_image(data['poster_path'])


        return info

    def get_average_rating(self, movie_title: str) -> str:
        # get the corresponding TMDB movie id from the title
        movie_id = self.get_movie_id(movie_title)
        if movie_id == "":
            return False # if bad movie_id, return False
        
        # make the api call
        url = f'{self.baseURL}/movie/{movie_id}?api_key={self.APIKEY}'
        res = requests.get(url)
        data = res.json()

        # grab the rating from the json
        rating = data['vote_average']
        return rating


TMDB_APIKEY = '' # ! <- ADD YOUR OWN API KEY HERE!
CreatedTMDBAPI = TMDB_API(TMDB_APIKEY)
