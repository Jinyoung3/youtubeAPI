import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# Replace these with your own credentials and channel ID
CLIENT_SECRETS_FILE = 'client_secrets.json'
#CHANNEL_ID = 'UCVGFImKSR987wdDg1ib-QAw'

# API information
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME_YT = 'youtube'
API_SERVICE_NAME_YTA = 'youtubeAnalytics'
API_VERSION_YT = 'v3'
API_VERSION_YTA = 'v2'
TOKEN_FILE = 'TOKEN_FILE.json'
def read_config_from_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

CHANNEL_ID = read_config_from_json('youtubeInfo.json')['channel_id']
# def get_authenticated_service():
#     flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#     credentials = flow.run_local_server(port=0)
#     youtube = build(API_SERVICE_NAME_YT, API_VERSION_YT, credentials=credentials)
#     youtube_analytics = build(API_SERVICE_NAME_YTA, API_VERSION_YTA, credentials=credentials)
#     return youtube, youtube_analytics
def get_authenticated_service():
    credentials = None
    # Check if the token file exists
    if os.path.exists(TOKEN_FILE):
        # Load the saved credentials
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=SCOPES)
        
        # Check if the credentials are expired or invalid
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                # Refresh the credentials
                credentials.refresh(Request())
            else:
                # Credentials are not valid and can't be refreshed, need to login again
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
                credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(TOKEN_FILE, 'w') as token:
                    token.write(credentials.to_json())
    else:
        # No token file, need to login and create one
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
        credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())

    youtube = build(API_SERVICE_NAME_YT, API_VERSION_YT, credentials=credentials)
    youtube_analytics = build(API_SERVICE_NAME_YTA, API_VERSION_YTA, credentials=credentials)
    return youtube, youtube_analytics
def get_youtube_data(youtube):
    # Fetch subscribers and total views from the YouTube Data API
    request = youtube.channels().list(
        part="statistics",
        id=CHANNEL_ID
    )
    response = request.execute()
    stats = response['items'][0]['statistics']
    return {
        'subscribers': int(stats['subscriberCount']),
        'total_views': int(stats['viewCount'])
    }

def get_youtube_analytics_data(youtube_analytics):
    # Fetch likes, comments, shares from the YouTube Analytics API
    request = youtube_analytics.reports().query(
        ids='channel==%s' % CHANNEL_ID,
        startDate='2024-03-02',
        endDate='2024-03-03',
        metrics='likes,comments,shares',
        dimensions='day',
        sort='day'
    )
    response = request.execute()
    # Simplify the response for demonstration purposes
    return response

def main():
    youtube, youtube_analytics = get_authenticated_service()
    
    yt_data = get_youtube_data(youtube)
    subscribers = yt_data['subscribers']
    total_views = yt_data['total_views']
    yta_data = get_youtube_analytics_data(youtube_analytics)
    last_row = yta_data['rows'][-1]  # Get the last row
    date, likes, comments, shares = last_row 
    print("Subscribers:", subscribers)
    print("Total Views:", total_views)
    print("Date:", date)
    print("Likes:", likes)
    print("Comments:", comments)
    print("Shares:", shares)
    print("engagement_rate", (likes + comments + shares+subscribers) / total_views*100)

if __name__ == '__main__':
    main()
