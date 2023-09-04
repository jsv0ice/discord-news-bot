import requests
import sqlite3
from .. import config
from datetime import datetime
from ..discord_utils import headers
from googleapiclient.errors import HttpError


YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

async def check_new_video():
    print('video checking initialized')
    params = {
        "key": config.YOUTUBE_API_KEY,
        "channelId": config.YOUTUBE_CHANNEL_ID,
        "part": "snippet",
        "order": "date",
        "maxResults": 1
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    print(response.json())
    video_id_data = response.json().get('items', [{}])[0].get('id', {})
    video_data = response.json().get('items', [{}])[0].get('snippet', {})
    
    video_name = video_data.get('title')
    channel_name = video_data.get('channelTitle')
    video_date = datetime.strptime(video_data.get('publishedAt'), '%Y-%m-%dT%H:%M:%SZ')
    video_id = video_id_data.get('videoId')
    print(video_id_data)
    print(video_id)
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    #try:
    #    transcript = get_transcript(video_id)  # Placeholder function to retrieve transcript
    #except Exception as e:
    #    transcript = None
    #    print('Error getting transcript')
    transcript = video_data.get('description')

    with sqlite3.connect(config.DB_STRING) as conn:
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS video_data
                          (video_name TEXT, channel_name TEXT, video_date DATETIME, video_url TEXT, transcript TEXT)''')

        # Check if 'video_url' column exists and add it if it doesn't
        cursor.execute("PRAGMA table_info(video_data)")
        columns = [column[1] for column in cursor.fetchall()]
        if "video_url" not in columns:
            cursor.execute("ALTER TABLE video_data ADD COLUMN video_url TEXT")
        
        cursor.execute("PRAGMA table_info(video_data)")
        columns = [column[1] for column in cursor.fetchall()]
        if "transcript" not in columns:
            cursor.execute("ALTER TABLE video_data ADD COLUMN video_url TEXT")

        
        cursor.execute("SELECT * FROM video_data WHERE video_name=?", (video_name,))
        existing_video = cursor.fetchone()

        if existing_video:
            cursor.execute("UPDATE video_data SET video_date=?, video_url=?, transcript=? WHERE video_name=?",
                           (video_date, video_url, transcript, video_name))
            conn.commit()
            return {video_url, video_name, transcript, channel_name}
        else:
            cursor.execute("INSERT INTO video_data (video_name, channel_name, video_date, video_url, transcript) VALUES (?, ?, ?, ?, ?)",
                           (video_name, channel_name, video_date, video_url, transcript))
            conn.commit()
            return None

    

def get_transcript(video_id):
    #doesn't work for now, need to work with individual content providers to get access to captions
    print(video_id)
    print(config.youtube_client)
    try:
        # List the captions available for the video
        captions_list = config.youtube_client.captions().list(
            part="snippet",
            videoId=video_id
        ).execute()
        print(captions_list)

        # Check if there are any captions available
        if not captions_list["items"]:
            return "No captions available for video " + video_id

        # Get the first caption track ID (you can modify this to select a specific language if needed)
        caption_id = captions_list["items"][0]["id"]

        # Download the caption track
        caption = config.youtube_client.captions().download(
            id=caption_id
        ).execute()

        caption_decode = caption.decode('utf-8')
        print(caption_decode)

        return caption_decode  # Convert bytes to string

    except Exception as e:
        print(e)
        return "Error fetching transcript for video " + video_id


{'kind': 'youtube#searchListResponse', 'etag': 'n0o2de5s07xU36aoyZhtQASjA_g', 'nextPageToken': 'CAEQAA', 'regionCode': 'US', 'pageInfo': {'totalResults': 291, 'resultsPerPage': 1}, 'items': [{'kind': 'youtube#searchResult', 'etag': 'BCQtuILQSsz-yjIPKyKvY9Oac0Q', 'id': {'kind': 'youtube#video', 'videoId': 'bR6kHdFx9ss'}, 'snippet': {'publishedAt': '2023-08-31T17:31:45Z', 'channelId': 'UCRiVHK_3XpMqXkkZsW4g8Tg', 'title': 'Will GPT AI obsolete all the new RPGs including Starfield?', 'description': 'GPT may make how characters have been in RPGs for three decades become obsolete. Go to my sponsor ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/bR6kHdFx9ss/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/bR6kHdFx9ss/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/bR6kHdFx9ss/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': "Ray's Guide", 'liveBroadcastContent': 'none', 'publishTime': '2023-08-31T17:31:45Z'}}]}