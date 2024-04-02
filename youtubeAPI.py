import requests
import json

# Make a class that handles all of our interactions with the Youtube API
class YouTubeAPI:
    # initialize it with the api key
    def __init__(self, APIKEY):
        self.APIKEY = APIKEY
        self.baseURL = 'https://www.googleapis.com/youtube/v3'

    # define a method to grab the top comments from a specific video
    # takes in video id (string) and an optional number_limit (integer) which specifies the max number of comments we grab
    # TODO: consider adding feature to grab replies to comments as well
    def get_top_comments(self, video_id: str, number_limit: int = 20) -> list[str]:
        top_comments = []
        url = f'{self.baseURL}/commentThreads?part=snippet&videoId={video_id}&key={self.APIKEY}&maxResults={number_limit}'
        
        # make the request and store the data
        response = requests.get(url)
        data = json.loads(response.text)

        # parse through the json and grab the actual comment itself
        items = data["items"]
        for item in items:
            # grab each comment and append it to our return value
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            top_comments.append(comment)

        return top_comments


# Youtube APIKey was created from the YT app
YOUTUBE_APIKEY = 'AIzaSyBEzevk5Am8U4xhlgdTmMmuFRB7FtbIDQw'
video_id = 'pBk4NYhWNMM' 

# create an instance of the YouTubeAPI Class
YoutubeAPI = YouTubeAPI(YOUTUBE_APIKEY)

print(YoutubeAPI.get_top_comments(video_id, number_limit=50))

