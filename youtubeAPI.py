import requests
import json

# Youtube APIKey was created from the YT app
YOUTUBE_APIKEY = 'AIzaSyBEzevk5Am8U4xhlgdTmMmuFRB7FtbIDQw'

# we create the request url using the apikey and we can get the video_id the youtube video url
baseURL = 'https://www.googleapis.com/youtube/v3'
video_id = 'cqGjhVJWtEg' # 
url = f'{baseURL}/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_APIKEY}&order=relevance'

# make the request and store the data
response = requests.get(url)
data = json.loads(response.text)

# parse through the json and grab the actual comment itself
items = data["items"]
for item in items:
    print(item['snippet']['topLevelComment']['snippet']['textDisplay']) 