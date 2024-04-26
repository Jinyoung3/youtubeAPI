import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secrets.json'
# def get_service():
#   flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#   credentials = flow.run_local_server(port=0)
#   return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
def get_authenticated_service():
    credentials = None
    token_file = 'token.json'

    # Check if the token file exists
    if os.path.exists(token_file):
        # Load the saved credentials
        credentials = Credentials.from_authorized_user_file(token_file, scopes=SCOPES)
        
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
                with open(token_file, 'w') as token:
                    token.write(credentials.to_json())
    else:
        # No token file, need to login and create one
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
        credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(**kwargs).execute()
  with open('engage.json', 'w') as json_file:
    json.dump(response, json_file, indent=4)

def read_config_from_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data
if __name__ == '__main__':
  # Disable OAuthlib's HTTPs verification when running locally.
  # *DO NOT* leave this option enabled when running in production.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  config = read_config_from_json('youtubeInfo.json')
  youtubeAnalytics = get_authenticated_service()
  execute_api_request(
      youtubeAnalytics.reports().query,
      ids=f'channel=={config["channel_id"]}',
    #    ids='channel==UCVGFImKSR987wdDg1ib-QAw',
    #    startDate='2024-01-01',
    #    endDate='2024-03-03',
      startDate=config["start_date"],
      endDate=config["end_date"],
      metrics='estimatedMinutesWatched,views,likes,subscribersGained,shares,comments',
      dimensions='day',
      sort='day'
)