# import os
# import json
# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# # scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
# SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
# API_SERVICE_NAME = "youtube"
# API_VERSION = "v3"
# CLIENT_SECRETS_FILE = "client_secrets.json"
# TOKEN_FILE = "tokenStat.json"
# def read_config_from_json(json_file_path):
#     with open(json_file_path, 'r') as json_file:
#         data = json.load(json_file)
#     return data
# def get_authenticated_service():
#     credentials = None
#     if os.path.exists(TOKEN_FILE):
#         credentials = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=SCOPES)
#         if not credentials.valid:
#             if credentials.expired and credentials.refresh_token:
#                 credentials.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#                 credentials = flow.run_local_server(port=0)
#                 with open(TOKEN_FILE, 'w') as token:
#                     token.write(credentials.to_json())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#         credentials = flow.run_local_server(port=0)
#         with open(TOKEN_FILE, 'w') as token:
#             token.write(credentials.to_json())
#     return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
# id = read_config_from_json('youtubeInfo.json')['channel_id']
# def main():
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#     api_service_name = "youtube"
#     api_version = "v3"
#     client_secrets_file = "client_secrets.json"
#     youtube = get_authenticated_service()
#     # Get credentials and create an API client
#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         client_secrets_file, SCOPES)
#     credentials = flow.run_local_server()
#     youtube = googleapiclient.discovery.build(
#         api_service_name, api_version, credentials=credentials)

#     request = youtube.channels().list(
#         part='snippet,contentDetails,statistics',
#         id=id
#     )
#     response = request.execute()
#     json_filename = "stats.json"  # This will create or overwrite youtube_response.json in the current directory
#     # Serialize response to JSON formatted string and write to the file
#     with open(json_filename, 'w') as json_file:
#         json.dump(response, json_file, indent=4)
#     print(f"Response has been saved to {json_filename}")

# if __name__ == "__main__":
#     main()
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Define your SCOPES and other constants
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "tokenStat.json"

def read_config_from_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=SCOPES)
        if not credentials.valid:
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                credentials = flow.run_local_server(port=0)
                with open(TOKEN_FILE, 'w') as token:
                    token.write(credentials.to_json())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    channel_id = read_config_from_json('youtubeInfo.json')['channel_id']
    youtube = get_authenticated_service()

    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    )
    response = request.execute()
    json_filename = "stats.json"
    with open(json_filename, 'w') as json_file:
        json.dump(response, json_file, indent=4)
    print(f"Response has been saved to {json_filename}")

if __name__ == "__main__":
    main()
