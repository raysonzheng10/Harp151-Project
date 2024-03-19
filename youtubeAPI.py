import requests
import json

YOUTUBE_APIKEY = 'AIzaSyBEzevk5Am8U4xhlgdTmMmuFRB7FtbIDQw'
baseURL = 'https://www.googleapis.com/youtube/v3'

video_id = 'cqGjhVJWtEg'
url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_APIKEY}'

response = requests.get(url)
data = json.loads(response.text)

items = data["items"]
print(items)
for comment in items:
    print(comment['snippet']['topLevelComment']['snippet']['textDisplay'])