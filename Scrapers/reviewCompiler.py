from googleReviews import googleReviews
from rottenTomatoes import CreatedRottenTomatoesScraper
from youtubeAPI import CreatedYoutubeAPI

class ReviewCompiler:
    def __init__(self, googleReviewer, tomatoesReviewer, youtubeReviewer):
        self.google = googleReviewer
        self.tomatoes = tomatoesReviewer
        self.youtube = youtubeReviewer

    def get_reviews(self, movie: str) -> dict:
        # google_reviews = self.google.get_google_reviews(movie, 5)
        # tomatoes_reviews = self.tomatoes.get_topCritic_reviews(movie)

        youtube_video_id = self.google.get_YoutubeTrailer_Id(movie)
        youtube_reviews = self.youtube.get_top_comments(youtube_video_id)
        print(youtube_reviews)

reviewCompiler = ReviewCompiler(googleReviews, CreatedRottenTomatoesScraper, CreatedYoutubeAPI)

reviewCompiler.get_reviews('the amazing spiderman 2')