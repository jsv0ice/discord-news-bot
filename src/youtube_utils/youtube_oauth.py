import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
import google.auth.transport.requests


# OAuth 2.0 setup
CLIENT_SECRETS_FILE = "src/youtube_utils/client_secret.json"
TOKEN_FILE = "src/youtube_utils/oauth_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate():
    credentials = None

    # Check if we have saved token file
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token:
            credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no valid credentials available, prompt the user to log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for future runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())

    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    
    return youtube

if __name__ == "__main__":
    authenticate()
