import requests
import json

# Make a class that handles all of our interactions with the Youtube API
class YouTubeAPI:
    # initialize it with the api key
    def __init__(self, APIKEY):
        self.APIKEY = APIKEY
        self.baseURL = 'https://www.googleapis.com/youtube/v3'

    # define a method to grab the top comments from a specific video
    def get_top_comments(self, video_id: str, number_limit: int = 30) -> list[str]:
        top_comments = []
        url = f'{self.baseURL}/commentThreads?part=snippet&videoId={video_id}&key={self.APIKEY}&order=relevance&maxResults={number_limit}'
        
        # make the request and store the data
        res = requests.get(url)
        data = res.json()

        try:
            # parse through the json and grab the actual comment itself
            items = data["items"]
            for item in items:
                # grab each comment and append it to our return value
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                top_comments.append(comment)
        except KeyError:
            print('Unable to grab comments from Youtube')

        # returns empty list if failed
        return top_comments
    
    # function to get a percent of likes to views
    def get_ratio(self, likes:str, views:str) -> str:
        # make them into ints to do math
        likes = int(likes)
        views = int(views)

        # convert decimal to percent to string
        ratio_decimal = likes / views
        ratio_percentage = round(ratio_decimal * 100, 1)
        ratio = f'{ratio_percentage}%'

        # return that string value
        return ratio

    # function to get the likes, viewCount, and ratio of likes to views from a video
    def get_likes_views_ratio(self, video_id: str) -> tuple[str, str, str]:
        # make api call
        url = f'{self.baseURL}/videos?part=statistics&id={video_id}&key={self.APIKEY}'
        res = requests.get(url)
        data = res.json()

        try:
            # grab statistics from the video
            video_data = data['items'][0]['statistics']
            likes = video_data['likeCount']
            views = video_data['viewCount']
            ratio = self.get_ratio(likes, views)

        except IndexError or KeyError:
            print("Invalid Video Id.")
            return
        # returns None value if unsuccessful
        return likes, views, ratio


# Youtube APIKey was created from the YT app
YOUTUBE_APIKEY = 'AIzaSyBEzevk5Am8U4xhlgdTmMmuFRB7FtbIDQw'
video_id = 'cqGjhVJdasdsaWtEg' 

# create an instance of the YouTubeAPI Class
CreatedYoutubeAPI = YouTubeAPI(YOUTUBE_APIKEY)

# print(CreatedYoutubeAPI.get_top_comments('asd'))
# print(CreatedYoutubeAPI.get_likes_views_ratio(video_id))