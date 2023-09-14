import requests
import sqlite3
from .. import config
from datetime import datetime
from ..discord_utils import headers
from googleapiclient.errors import HttpError


YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

async def check_new_video(channel_id):
    print('video checking initialized')
    params = {
            "key": config.YOUTUBE_API_KEY,
            "channelId": channel_id,  # Use the channel ID from the database
            "part": "snippet",
            "order": "date",
            "maxResults": 1
        }
    response = requests.get(YOUTUBE_API_URL, params=params)
    print(response.json())
    video_id_data = response.json().get('items', [{}])[0].get('id', {})
    video_data = response.json().get('items', [{}])[0].get('snippet', {})
    thumbnail_url = video_data.get('thumbnails', {}).get('high', {}).get('url')

    print(thumbnail_url)
    
    video_name = video_data.get('title')
    channel_name = video_data.get('channelTitle')
    video_date = datetime.strptime(video_data.get('publishedAt'), '%Y-%m-%dT%H:%M:%SZ')
    video_id = video_id_data.get('videoId')
    print(f"Fetched video: {video_name} published on {video_date}")

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    transcript = str(video_data.get('description'))

    with sqlite3.connect(config.DB_STRING) as conn:
        cursor = conn.cursor()

        # Check if 'video_url' column exists and add it if it doesn't
        cursor.execute("PRAGMA table_info(video_data)")
        columns = [column[1] for column in cursor.fetchall()]
        if "video_url" not in columns:
            cursor.execute("ALTER TABLE video_data ADD COLUMN video_url TEXT")
        
        if "thumbnail_url" not in columns:
            cursor.execute("ALTER TABLE video_data ADD COLUMN thumbnail_url TEXT")
        
        cursor.execute("PRAGMA table_info(video_data)")
        columns = [column[1] for column in cursor.fetchall()]
        if "transcript" not in columns:
            cursor.execute("ALTER TABLE video_data ADD COLUMN transcript TEXT")
        
        cursor.execute("SELECT * FROM video_data WHERE video_name=?", (video_name,))
        existing_video = cursor.fetchone()

        if existing_video:
            print(f"Video: {video_name} already exists in the database")
            cursor.execute("UPDATE video_data SET video_date=?, video_url=?, transcript=?, thumbnail_url=? WHERE video_name=?",
                        (video_date, video_url, transcript, thumbnail_url, video_name))
            conn.commit()
            return None
        else:
            cursor.execute("INSERT INTO video_data (video_name, channel_name, video_date, video_url, transcript, thumbnail_url) VALUES (?, ?, ?, ?, ?, ?)",
               (video_name, channel_name, video_date, video_url, transcript, thumbnail_url))
            print(f"Inserted video: {video_name} into the database")
            conn.commit()
            return {
                "video_url": video_url,
                "video_name": video_name,
                "transcript": transcript,
                "channel_name": channel_name,
                "thumbnail_url": thumbnail_url
            }