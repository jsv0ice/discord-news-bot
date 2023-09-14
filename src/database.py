import sqlite3
from .config import DB_STRING

def initialize_db():
    with sqlite3.connect(DB_STRING) as conn:
        cursor = conn.cursor()
        
        # Existing tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                          (channel TEXT NOT NULL, sub TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS video_data
                          (video_name TEXT, channel_name TEXT, video_date DATETIME, video_url TEXT, transcript TEXT, thumbnail_url TEXT)''')
        
        # New table
        cursor.execute('''CREATE TABLE IF NOT EXISTS watch_channel
                          (youtube_channel_id TEXT NOT NULL, youtube_channel_name TEXT NOT NULL, discord_channel_id TEXT NOT NULL)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS message_tracking
                  (message_id TEXT PRIMARY KEY NOT NULL, content TEXT NOT NULL, sent_status INTEGER NOT NULL, target_channels TEXT)''')
        
        conn.commit()

