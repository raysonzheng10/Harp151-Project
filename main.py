from Scrapers.googleReviews import createdGoogleReviews
from Scrapers.youtubeAPI import CreatedYoutubeAPI
from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper

def get_google_reviews(movie_title):
    # the google reviews variable contains a list of google reviews
    google_reivews = createdGoogleReviews.get_google_reviews(movie_title,2)
    
    print(google_reivews)

def get_youtubeTrailer_id(movie_title):
    youtube_id = createdGoogleReviews.get_YoutubeTrailer_Id(movie_title)

    return youtube_id

def get_youtube_reviews(movie_title):
    youtube_id = get_youtubeTrailer_id(movie_title)

    youtube_reviews = CreatedYoutubeAPI.get_top_comments(youtube_id, 5)
    print(youtube_reviews)

def get_tomatoes_reviews(movie_title):
    tomatoes_reviews = CreatedRottenTomatoesScraper.get_topCritic_reviews(movie_title)

    print(tomatoes_reviews)
    
get_tomatoes_reviews('interstellar')