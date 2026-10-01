import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

youtube=build(
    'youtube',
    'v3',
    developerKey=os.getenv('YOUTUBE_DATA_API_KEY')
)



def get_video_details(video_id):

    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )

    response = request.execute()

    if not response["items"]:
        return None

    item = response["items"][0]

    snippet = item["snippet"]
    statistics = item["statistics"]
    content = item["contentDetails"]

    return {

        "title": snippet["title"],

        "channel": snippet["channelTitle"],

        "published": snippet["publishedAt"],

        "thumbnail": snippet["thumbnails"]["high"]["url"],

        "views": statistics.get("viewCount", 0),

        "likes": statistics.get("likeCount", 0),

        "duration": content["duration"]

    }