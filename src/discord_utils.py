import requests
from .config import DISCORD_TOKEN, GUILD_ID

headers = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "User-Agent": "DiscordBot (https://github.com/zeinestone/scorg-news, v0.1)",
    "Content-Type": "application/json",
}

def get_subscriptions_category_id(guild_id):
    response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers)
    if response.status_code == 200:
        for channel in response.json():
            if channel['type'] == 4 and channel['name'] == 'subscriptions':  # 4 is the type for category channels
                return channel['id']
    return None

def fetch_channels():
    channels = {}
    subscriptions_category_id = get_subscriptions_category_id(GUILD_ID)
    if subscriptions_category_id is None:
        print("Failed to find 'subscriptions' category.")
    else:
        response = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
        if response.status_code == 200:
            channel_data = response.json()
            for channel in channel_data:
                if channel['parent_id'] == subscriptions_category_id:
                    channels[channel['name']] = channel['id']
            print(channels)
        else:
            print(f"Failed to retrieve channels. Status code: {response.status_code}, Message: {response.text}")
    return channels